#!/usr/bin/env python3
"""Offline media-relief/time-stack study, driven by measured PCM audio.

NumPy/Pillow and local FFmpeg/ffprobe; no model, browser, account or download.
Depth is authored/aligned when supplied; fallback luminance relief remains illustrative.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import wave

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from tool_runtime import tool_environment


def run(args):
    return subprocess.run(args, check=True, capture_output=True,
                          env=tool_environment(shutil.which(str(args[0])))).stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                           '-of', 'json', str(path)]))


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def smooth(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


def audio_signals(pcm, sample_rate, fps, count):
    """Causal band envelopes and onset from the unsmoothed normalized low band."""
    pcm = np.asarray(pcm, dtype=np.float64)
    if pcm.ndim == 2:
        pcm = pcm.mean(axis=1)
    if not np.isfinite(pcm).all() or len(pcm) < math.ceil(count / fps * sample_rate):
        raise ValueError('Audio must be finite and cover the complete output')
    window = max(32, round(sample_rate * .04))
    frequencies = np.fft.rfftfreq(window, 1 / sample_rate)
    bands = [(40, 180), (180, 1500), (3000, min(10000, sample_rate / 2))]
    raw = []
    for frame in range(count):
        end = min(len(pcm), round(frame / fps * sample_rate))
        values = pcm[max(0, end - window):end]
        values = np.pad(values, (window - len(values), 0))
        power = np.abs(np.fft.rfft(values * np.hanning(window))) ** 2
        raw.append([float(np.sqrt(np.mean(power[(frequencies >= lo) & (frequencies < hi)])))
                    for lo, hi in bands])
    raw = np.asarray(raw)
    ceiling = np.percentile(raw, 95, axis=0)
    # Do not normalize numerical leakage in an otherwise silent frequency band into motion.
    floor = max(1e-10, float(ceiling.max()) * .003)
    raw[raw < floor] = 0
    normalized = np.divide(raw, ceiling, out=np.zeros_like(raw), where=ceiling > floor)
    normalized = np.clip(normalized, 0, 1)
    result = np.zeros_like(raw)
    for i in range(1, count):
        tau = np.where(normalized[i] > result[i - 1], .04, .18)
        result[i] = result[i - 1] + (normalized[i] - result[i - 1]) * (1 - np.exp(-1 / fps / tau))
    return result, audio_onsets(normalized, fps)


def audio_features(pcm, sample_rate, fps, count):
    """Compatible three-band envelope API; onset extraction shares its measured raw bands."""
    return audio_signals(pcm, sample_rate, fps, count)[0]


def read_audio(path, duration):
    with wave.open(str(path)) as stream:
        if stream.getsampwidth() != 2 or stream.getcomptype() != 'NONE':
            raise ValueError('Use an uncompressed 16-bit PCM WAV for measured audio binding')
        rate, channels = stream.getframerate(), stream.getnchannels()
        if rate < 22050 or channels not in (1, 2):
            raise ValueError('Use mono/stereo PCM WAV at 22050Hz or higher')
        if stream.getnframes() / rate < duration:
            raise ValueError('Audio is shorter than the requested film; no padding or loop')
        samples = np.frombuffer(stream.readframes(math.ceil(duration * rate)), '<i2')
    return samples.reshape(-1, channels).astype(np.float64) / 32768, rate


def audio_onsets(features, fps=30):
    """Positive low-band change with an 80 ms release; never anticipate a beat."""
    delta = np.maximum(0, np.diff(features[:, 0], prepend=features[0, 0]))
    result = np.zeros(len(features))
    for n in range(1, len(features)):
        result[n] = max(min(1., 3.5 * delta[n]), result[n-1] * math.exp(-1 / fps / .08))
    return result


def load_frames(path, start, duration, gray=False):
    # 24 fps bounds memory at about 359 MB for a 15 s RGB source; no full-resolution cache.
    filters = ('fps=24,scale=432:768:force_original_aspect_ratio=decrease,'
               'pad=432:768:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1')
    raw = run(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(path), '-t', str(duration),
               '-an', '-vf', filters, '-f', 'rawvideo', '-pix_fmt', 'gray' if gray else 'rgb24', 'pipe:1'])
    channels = 1 if gray else 3
    count = len(raw) // (432 * 768 * channels)
    if count < 2 or len(raw) != count * 432 * 768 * channels:
        raise ValueError('Source did not decode to complete aligned frames')
    shape = (count, 768, 432) if gray else (count, 768, 432, 3)
    return np.frombuffer(raw, np.uint8).reshape(shape)


def load_fields(matte_path, depth_path, frames, duration):
    matte = depth = None
    if matte_path:
        video = next(x for x in probe(matte_path)['streams'] if x['codec_type'] == 'video')
        if (int(video['width']), int(video['height'])) != (432, 768):
            raise ValueError('Matte must match the 432×768 padded source derivative exactly')
        matte = load_frames(matte_path, 0, duration, gray=True)
        if len(matte) != len(frames):
            raise ValueError('Matte must cover the complete selected source interval, starting at its own 0')
    if depth_path:
        with Image.open(depth_path) as field:
            if field.size != (432, 768) or field.mode != 'L':
                raise ValueError('Depth must be a normalized 8-bit grayscale 432×768 image, near=white')
            depth = np.asarray(field).copy() / 255.
    return matte, depth


class MediaStudy:
    def __init__(self, frames, features, size, duration, font, source_start=0, matte=None, depth=None, onsets=None):
        self.frames, self.features = frames, features
        self.width, self.height = size
        self.duration, self.factor = duration, self.width / 720
        self.font_path, self.fonts = str(font), {}
        self.source_start, self.matte, self.depth = source_start, matte, depth
        self.onsets = audio_onsets(features) if onsets is None else np.asarray(onsets)
        if self.onsets.shape != (len(features),) or not np.isfinite(self.onsets).all():
            raise ValueError("Onset envelope must be finite and match the output frame count")
        self.grid = (128, 228)
        xx, yy = np.meshgrid(np.linspace(-.8, .8, self.grid[0]), np.linspace(1.4226, -1.4226, self.grid[1]))
        self.xy = np.column_stack((xx.ravel(), yy.ravel()))
        # One sampled cache per source frame; never re-estimate geometry from a lighting change.
        self.colors = [np.asarray(Image.fromarray(f).resize(self.grid, Image.Resampling.LANCZOS)).reshape(-1,3) for f in frames]
        self.masks = [np.asarray(Image.fromarray(f).resize(self.grid, Image.Resampling.BILINEAR)).ravel()/255 for f in matte] if matte is not None else None
        self.depth_grid = np.asarray(Image.fromarray((depth*255).astype(np.uint8)).resize(self.grid, Image.Resampling.BILINEAR)).ravel()/255 if depth is not None else None

        # A fixed contact plane follows the lowest supported matte row,not the padded canvas.
        contacts = [float(self.xy[m > .5,1].min()) for m in self.masks if np.any(m > .5)] if self.masks is not None else [-1.4226]
        if not contacts:
            raise ValueError('Aligned matte contains no visible subject')
        self.ground_y = min(contacts)

    def scene_state(self, frame):
        u = frame / 30 / self.duration
        lift = smooth((u-.13)/.15)
        phase = float(np.clip((u-.55)/.20,0,1))
        spread = smooth(phase)
        index = min(len(self.frames)-1,round(min(u/.69,1)*(len(self.frames)-1)))
        layers = []
        for n in range(7):
            age = (7-n)/7
            delay = n/7*.24
            peel = smooth((phase-delay)/(1-delay))
            # Fixed sampled source times; clamp unavailable moments rather than showing the future.
            chosen = min(index,round(n/7*(len(self.frames)-1)))
            layers.append((chosen, -age*peel, lift*peel*(.14+.34*(1-age))))
        return lift, spread, index, layers

    def text(self, draw, xy, value, size, color, anchor='la'):
        size = round(size * self.factor)
        if size not in self.fonts:
            self.fonts[size] = ImageFont.truetype(self.font_path, size)
        draw.text(tuple(round(v * self.factor) for v in xy), value, font=self.fonts[size], fill=color, anchor=anchor)

    def project(self, points, yaw, camera_scale=1, center_shift=0):
        c, s = math.cos(yaw), math.sin(yaw)
        rotated = np.asarray(points) @ np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
        z = rotated[:, 2]
        # Fixed focal length: never re-fit each beat's expanded bounds back into the same box.
        focal = self.width * (478 / (720*1.6)) * camera_scale / (1 - z / 7)
        return np.column_stack((self.width * (.5+center_shift) + rotated[:, 0] * focal,
                                630*self.factor - rotated[:, 1] * focal, z))

    def cloud(self, target, index, yaw, relief, offset, opacity, low, mid, high, onset, scale, shift=0):
        colors = self.colors[index]
        alpha = self.masks[index] if self.masks is not None else np.ones(len(colors))
        depth = self.depth_grid if self.depth_grid is not None else colors @ np.array([.2126,.7152,.0722])/255
        keep = alpha > .06
        colors, alpha, depth, xy = colors[keep], alpha[keep], depth[keep], self.xy[keep].copy()
        if self.masks is not None and np.any(alpha > .5):
            # This standing-subject study anchors each pose's visible support to the fixed floor.
            xy[:,1] += relief*(self.ground_y-float(xy[alpha>.5,1].min()))
        # Stable subject depth; bass adds bounded physical displacement rather than global camera zoom.
        z = relief * (depth * (.95 + .22*low) + .08*onset) + offset
        xy[:,0] += offset*.13
        points = self.project(np.column_stack((xy, z)), yaw, scale, shift)
        layer = Image.new('RGBA', target.size)
        draw = ImageDraw.Draw(layer)
        radius = self.factor * (1.52 + .58*high + .22*onset)
        intensity = 1 + .06*mid
        rgba = np.column_stack((np.clip(colors.astype(float)*intensity,0,255).astype(np.uint8),
                                np.round(255*opacity*alpha).astype(np.uint8))).tolist()
        for n in np.argsort(points[:,2]):
            x,y,_ = points[n]
            draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=tuple(rgba[n]))
        target.alpha_composite(layer)

    def composite_field(self, image, field, mid, onset):
        # Premultiply before blurring: faint historical poses must not emit opaque halos.
        energy = .14*mid + .48*onset
        if energy > .001:
            emission = ImageChops.multiply(field.convert('RGB'),field.getchannel('A').convert('RGB'))
            emission = ImageEnhance.Brightness(emission.filter(ImageFilter.GaussianBlur(4*self.factor))).enhance(energy)
            image = ImageChops.add(image.convert('RGB'),emission).convert('RGBA')
        image.alpha_composite(field)
        return image

    def render(self, frame):
        t = frame / 30
        u = t / self.duration
        low, mid, high = self.features[frame]
        onset = self.onsets[frame]
        lift, spread, index, layers = self.scene_state(frame)
        source = Image.fromarray(self.frames[index])
        image = Image.new('RGBA',(self.width,self.height),'#07191f')
        texture = source.resize((round(478*self.factor),round(850*self.factor)),Image.Resampling.LANCZOS).convert('RGBA')
        # Source and points share the same source index and initial framing throughout the dissolve.
        texture.putalpha(round(255*(1-lift)))
        image.alpha_composite(texture,(round(121*self.factor),round(205*self.factor)))
        yaw = lift*(-.34 + .79*smooth((u-.38)/.45))
        scale = 1-.08*lift-.22*spread
        shift = .08*spread
        if lift > 0:
            grid_layer=Image.new("RGBA",image.size)
            draw=ImageDraw.Draw(grid_layer)
            grid_opacity=round(45*lift)
            # A quiet projected floor supplies perspective evidence without an application UI replica.
            for x in np.linspace(-2.6,2.6,12):
                pp=self.project([[x,self.ground_y,-3],[x,self.ground_y,.8]],yaw,scale,shift)
                draw.line([tuple(pp[0,:2]),tuple(pp[1,:2])],fill=(75,127,133,grid_opacity),width=max(1,round(self.factor)))
            for z in np.linspace(-3,.8,12):
                pp=self.project([[-2.6,self.ground_y,z],[2.6,self.ground_y,z]],yaw,scale,shift)
                draw.line([tuple(pp[0,:2]),tuple(pp[1,:2])],fill=(75,127,133,grid_opacity),width=max(1,round(self.factor)))
            # Clip the floor to the protected artwork rectangle.
            image.alpha_composite(grid_layer.crop((0,round(185*self.factor),self.width,round(1080*self.factor))),(0,round(185*self.factor)))
            field = Image.new('RGBA',image.size)
            for chosen, extent, opacity in layers:
                if opacity > 0:
                    self.cloud(field,chosen,yaw,lift,extent*(2.65+.45*low+.28*onset),opacity,low,mid,high,onset,scale,shift)
            self.cloud(field,index,yaw,lift,0,lift,low,mid,high,onset,scale,shift)
            image = self.composite_field(image,field,mid,onset)
        image=image.convert('RGB')
        draw=ImageDraw.Draw(image)
        if u < .28:
            label,title,note='01 / IMAGE TO VOLUME','Let the image breathe.','Same source frame / a continuous depth reveal'
        elif u < .75:
            label,title='02 / DEPTH TO TIME','Give motion a memory.'
            note='Aligned subject relief / measured beat response' if self.depth is not None else 'Illustrative luminance relief / measured beat response'
        else:
            label,title,note='03 / TIME TRAILS','One moment, unfolding.','Eight historical poses / time moves through depth'
        self.text(draw,(42,40),'SIGMA STUDIOZ  /  VISUAL STUDY',13,'#7fa5a8')
        self.text(draw,(42,89),title,38,'#f4e6c8')
        self.text(draw,(42,149),label,13,'#d6a86a')
        if spread > .98:
            self.text(draw,(92,1070),f'PAST  ~{self.source_start:.1f}s',11,'#6f999d')
            self.text(draw,(628,1070),f'NOW  ~{self.source_start+(len(self.frames)-1)/24:.1f}s',11,'#b1c6c4','ra')
        self.text(draw,(42,1120),note,16,'#b1c6c4')
        for n,(name,value) in enumerate(zip(['LOW / DEPTH','MID / BLOOM','HIGH / MARKS'],[low,mid,high])):
            x,y=(42+n*224)*self.factor,1184*self.factor
            draw.rectangle((x,y,x+188*self.factor,y+3*self.factor),fill='#27464b')
            draw.rectangle((x,y,x+188*self.factor*value,y+3*self.factor),fill='#d6a86a')
            self.text(draw,(42+n*224,1201),name,10,'#7fa5a8')
        self.text(draw,(678,1245),f'{t:04.1f} / {self.duration:04.1f}',11,'#7fa5a8','ra')
        return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--audio', type=Path, required=True)
    parser.add_argument('--font', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='New private output folder')
    parser.add_argument('--matte', type=Path, help='Aligned 432×768 grayscale video of the selected source interval, starting at 0')
    parser.add_argument('--depth', type=Path, help='Aligned 432×768 8-bit grayscale static depth, near=white')
    parser.add_argument('--depth-kind', choices=['authored','estimated','measured'])
    parser.add_argument('--source-in', type=float, default=0)
    parser.add_argument('--source-duration', type=float, default=5)
    parser.add_argument('--duration', type=float, default=15)
    parser.add_argument('--width', type=int, default=1080)
    parser.add_argument('--height', type=int, default=1920)
    args = parser.parse_args()
    if not (all(math.isfinite(x) for x in [args.source_in, args.source_duration, args.duration])
            and args.source_in >= 0 and .5 <= args.source_duration <= 15
            and 6 <= args.duration <= 30 and abs(args.duration * 30 - round(args.duration * 30)) < 1e-6
            and (args.width, args.height) in [(720, 1280), (1080, 1920)]):
        raise ValueError('Use a valid source interval, 6–30 s on the 30 fps grid and 720×1280 or 1080×1920')
    if bool(args.depth) != bool(args.depth_kind):
        raise ValueError("Declare --depth-kind with --depth; never imply recovered geometry")
    for path in [args.source, args.audio, args.font] + [p for p in [args.matte,args.depth] if p]:
        if not path.is_file():
            raise ValueError(f'Missing input: {path}')
    if args.output.exists():
        raise ValueError('Preserve existing outputs; choose a fresh revision folder')
    info = probe(args.source)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    if args.source_in + args.source_duration > float(video.get('duration', info['format']['duration'])) + .001:
        raise ValueError('Source interval exceeds the available video')
    pcm, rate = read_audio(args.audio, args.duration)
    count = round(args.duration * 30)
    features, onsets = audio_signals(pcm, rate, 30, count)
    frames = load_frames(args.source, args.source_in, args.source_duration)
    matte, depth = load_fields(args.matte, args.depth, frames, args.source_duration)
    study = MediaStudy(frames, features, (args.width, args.height), args.duration, args.font, args.source_in, matte, depth, onsets)
    args.output.mkdir(parents=True)
    final = args.output / 'media-in-3d.mp4'
    process = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                                '-s', f'{args.width}x{args.height}', '-r', '30', '-i', 'pipe:0', '-i', str(args.audio),
                                '-map', '0:v', '-map', '1:a', '-t', str(args.duration), '-c:v', 'libx264', '-preset', 'medium',
                                '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(final)],
                               stdin=subprocess.PIPE, env=tool_environment(shutil.which('ffmpeg')))
    try:
        for n in range(count):
            picture = study.render(n)
            if n in [0, round(count * .34), round(count * .53), round(count * .78), count - 1]:
                picture.save(args.output / f'frame-{n:04d}.jpg', quality=94)
            process.stdin.write(picture.tobytes())
            if n % 90 == 0:
                print(f'frame {n}/{count}', flush=True)
    finally:
        process.stdin.close()
        code = process.wait()
    if code:
        raise RuntimeError('Encoder failed; preserve partial output for diagnosis')
    run(['ffmpeg', '-v', 'error', '-i', str(final), '-f', 'null', '-'])
    result = probe(final)
    streams = result['streams']
    v = next(s for s in streams if s['codec_type'] == 'video')
    a = next(s for s in streams if s['codec_type'] == 'audio')
    if int(v['nb_frames']) != count or abs(float(v['duration']) - args.duration) > .001 or abs(float(a['duration']) - args.duration) > .05:
        raise RuntimeError('Incomplete picture or audio export')
    report = {'output':str(final.resolve()), 'sha256':sha(final), 'duration':args.duration, 'fps':30, 'frames':count,
              'size':[args.width,args.height], 'source':str(args.source.resolve()), 'source_sha256':sha(args.source),
              'source_range':[args.source_in,args.source_in + args.source_duration], 'source_decode_fps':24,
              'source_sampling_time_precision':'24fps derivative grid; labels are approximate,not native PTS',
              'source_map':'Source progresses once over the first 69%; fixed historical source anchors peel with staggered opacity from 55–75%; no rewind or future frame',
              'audio':str(args.audio.resolve()), 'audio_sha256':sha(args.audio), 'audio_sample_rate':rate,
              'font_sha256':sha(args.font), 'depth':(args.depth_kind+' normalized static relief' if args.depth else 'Illustrative luminance relief')+'; no unseen geometry',
              'matte_sha256':sha(args.matte) if args.matte else None, 'depth_sha256':sha(args.depth) if args.depth else None,
              'alignment':'Fields reference the selected 432×768 padded source derivative; matte begins at its own 0',
              'feature_timing':'40ms FFT window ends at frame/fps; no lookahead;40ms attack/180ms release',
              'onsets':study.onsets.tolist(), 'onset_timing':'Positive change of unsmoothed normalized low-band FFT energy;80ms release',
              'ground_y':study.ground_y,'grounding':'Standing-subject template: each matte support edge settles to the fixed contact plane during lift','history_anchors':[round(n/7*(len(frames)-1)) for n in range(8)],
              'framing':'Fixed focal length; authored pullback follows chapter time only,no per-beat auto-fit',
              'features':features.tolist(), 'bands_hz':[[40,180],[180,1500],[3000,min(10000,rate/2)]],
              'binding':{'relief_depth':'.95+.22*low plus.08*onset','point_radius_working_px':'1.52+.58*high+.22*onset','trail_extent':'2.65+.45*low+.28*onset','local_bloom':'.14*mid+.48*onset; alpha-premultiplied field,one additive pass'},
              'full_decode':'pass', 'visual_review':'pending', 'playback':'pending', 'listening':'not performed',
              'implementation_sha256':sha(__file__)}
    (args.output / 'render.json').write_text(json.dumps(report, indent=2) + '\n')
    print(str(final), flush=True)


if __name__ == '__main__':
    main()
