#!/usr/bin/env python3
"""Bounded local media evidence sampler. By Lex from SigmaStudioz; MIT."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise ValueError(message)


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def packet_end(probe, source, stream, timeout):
    """Demux to a bounded-on-disk log; container duration can truncate VFR presentation."""
    maximum = None
    with tempfile.TemporaryFile(mode='w+') as log:
        command = [
            probe, '-v', 'error', '-protocol_whitelist', 'file,pipe',
            '-select_streams', str(stream), '-show_entries',
            'packet=pts_time,duration_time', '-of', 'csv=p=0', str(source),
        ]
        subprocess.run(command, stdout=log, stderr=subprocess.PIPE, text=True, check=True, timeout=timeout)
        log.seek(0)
        for line in log:
            fields = line.strip().split(',')
            pts = number(fields[0]) if fields else None
            duration = number(fields[1]) if len(fields) > 1 else None
            if pts is not None:
                end = pts + max(0, duration or 0)
                maximum = end if maximum is None else max(maximum, end)
    return maximum


def sample(source, output, frames=24, start=0, end=None, stream=None, side=1280, timeout=180):
    source, output = Path(source).resolve(), Path(output).resolve()
    require(source.is_file(), 'Source must be a regular file')
    require(not output.exists(), 'Output already exists; choose a new evidence directory')
    require(type(frames) is int and 1 <= frames <= 64, 'Frame budget must be 1–64')
    require(type(side) is int and 320 <= side <= 2560, 'Maximum side must be 320–2560')
    require(number(timeout) is not None and 0 < timeout <= 3600, 'Timeout must be greater than 0 and at most 3600s')
    require(number(start) is not None and start >= 0, 'Invalid start time')
    require(end is None or number(end) is not None and end > start, 'Invalid end time')
    probe, encoder = shutil.which('ffprobe'), shutil.which('ffmpeg')
    require(probe is not None, 'ffprobe is required; no automatic installation')
    before = source.stat()
    identity = digest(source)
    fields = (
        'format=format_name,duration,start_time,size:'
        'stream=index,codec_type,codec_name,width,height,duration,start_time,'
        'time_base,avg_frame_rate,r_frame_rate:stream_disposition:stream_side_data'
    )
    command = [probe, '-v', 'error', '-protocol_whitelist', 'file,pipe', '-show_entries', fields, '-of', 'json', str(source)]
    result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=timeout)
    info = json.loads(result.stdout)
    allowed = {'mov', 'mp4', 'm4a', '3gp', '3g2', 'mj2', 'matroska', 'webm', 'avi', 'mpegts', 'mpeg', 'mp3', 'wav', 'flac', 'ogg', 'aac'}
    require(bool(set(info.get('format', {}).get('format_name', '').split(',')) & allowed), 'Unsupported media container')
    videos = [
        s for s in info.get('streams', [])
        if s.get('codec_type') == 'video'
        and not s.get('disposition', {}).get('attached_pic')
    ]
    if stream is not None:
        chosen = next((s for s in videos if s['index'] == stream), None)
    else:
        chosen = next(
            (s for s in videos if s.get('disposition', {}).get('default')),
            videos[0] if videos else None,
        )
    require(stream is None or chosen is not None, 'Requested video stream is unavailable')
    origin = number((chosen or {}).get('start_time'))
    if origin is None:
        origin = number(info.get('format', {}).get('start_time')) or 0
    reported_duration = number((chosen or {}).get('duration')) or number(info.get('format', {}).get('duration'))
    packet_time = packet_end(probe, source, chosen['index'], timeout) if chosen else None
    duration = packet_time - origin if packet_time is not None else reported_duration
    require(duration is None or duration > 0, 'Invalid media duration')
    require(end is not None or duration is not None, 'Unknown duration; provide an explicit end')
    end = end if end is not None else duration
    require(end > start and (duration is None or end <= duration + 0.001), 'Window lies outside media duration')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='media-evidence-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'result'
        stage.mkdir()
        samples = []
        if chosen:
            require(encoder is not None, 'FFmpeg is required for frames; no automatic installation')
            step = (end - start) / max(1, frames - 1)
            select = (
                f"select='between(t,{origin+start:.9f},{origin+end:.9f})"
                f"*(isnan(prev_selected_t)+gte(t-prev_selected_t,{step:.9f}))'"
            )
            scale = f"scale=w='min({side},iw)':h='min({side},ih)':force_original_aspect_ratio=decrease"
            command = [
                encoder, '-hide_banner', '-nostdin', '-nostats', '-loglevel', 'info',
                '-protocol_whitelist', 'file,pipe', '-ss', str(start),
                '-t', str(end-start), '-copyts', '-i', str(source),
                '-map', f"0:{chosen['index']}", '-vf', f'{select},{scale},showinfo',
                '-frames:v', str(frames), '-fps_mode', 'vfr', '-an', '-q:v', '3',
                str(stage / 'frame-%03d.jpg'),
            ]
            with (Path(temporary) / 'decoder.log').open('w+') as log:
                subprocess.run(command, stdout=subprocess.DEVNULL, stderr=log, check=True, timeout=timeout)
                log.seek(0)
                pattern = r'Parsed_showinfo.*?\bn:\s*\d+.*?\bpts_time:([-+\deE.]+)'
                times = [float(m.group(1)) for line in log if (m := re.search(pattern, line))]
            files = sorted(stage.glob('frame-*.jpg'))
            require(files and len(times) >= len(files), 'No timestamped frames decoded in the requested window')
            for image, pts in zip(files, times):
                relative = pts - origin
                require(start - .05 <= relative <= end + .05, 'Decoded timestamp outside requested window')
                samples.append({'file': image.name, 'pts_seconds': pts, 'source_seconds': relative})
        require((before.st_size, before.st_mtime_ns) == (source.stat().st_size, source.stat().st_mtime_ns), 'Source changed during inspection')
        inventory = {
            'source_name': source.name,
            'sha256': identity,
            'metadata': info,
            'selected_video_stream': chosen['index'] if chosen else None,
            'time_origin_seconds': origin,
            'reported_duration_seconds': reported_duration,
            'packet_duration_seconds': packet_time-origin if packet_time is not None else None,
            'requested_window': [start, end],
            'frame_budget': frames,
            'samples': samples,
            'coverage': (
                'Sparse samples only; packet timeline is not proof every frame decodes; '
                'inspect gaps and ending/detail windows separately'
            ),
            'audio_review': 'Not performed; metadata only',
        }
        (stage / 'inventory.json').write_text(json.dumps(inventory, indent=2) + '\n', encoding='utf-8')
        stage.rename(output)
    return inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--frames', type=int, default=24)
    parser.add_argument('--start', type=float, default=0)
    parser.add_argument('--end', type=float)
    parser.add_argument('--stream', type=int)
    parser.add_argument('--side', type=int, default=1280)
    parser.add_argument('--timeout', type=float, default=180)
    args = parser.parse_args()
    inventory = sample(args.source, args.output, args.frames, args.start, args.end, args.stream, args.side, args.timeout)
    print(json.dumps({'output': str(args.output), 'samples': len(inventory['samples']), 'sha256': inventory['sha256']}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f'Media sampling failed: {error}', file=sys.stderr)
        sys.exit(1)
