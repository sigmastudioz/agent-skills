#!/usr/bin/env python3
"""Stream deterministic explanation scenes to FFmpeg. By Lex from SigmaStudioz."""
import argparse
from array import array
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import wave
from PIL import Image, ImageDraw, ImageFont

BG, FG, MUTED = '#101216', '#F3F0E8', '#ABB0BB'
COLORS = {'accent': '#B59AFF', 'good': '#89E5C1', 'gap': '#FFAA97'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate(data):
    require(isinstance(data, dict), 'Storyboard must be an object')
    for key in ('brand', 'author'):
        require(isinstance(data.get(key), str) and 0 < len(data[key]) <= 80, f'Invalid {key}')
    scenes = data.get('scenes')
    require(isinstance(scenes, list) and 0 < len(scenes) <= 60, 'Expected 1–60 scenes')
    ids = set()
    for s in scenes:
        require(isinstance(s, dict), 'Scene must be an object')
        for key in ('id', 'eyebrow', 'title', 'body', 'caption', 'kind'):
            require(isinstance(s.get(key), str) and 0 < len(s[key]) <= 400, f'Invalid scene {key}')
        require(s['id'] not in ids, 'Duplicate scene ID'); ids.add(s['id'])
        require(finite(s.get('duration')) and 2 <= s['duration'] <= 30, 'Duration must be 2–30s')
        require(s['kind'] in ('graph', 'code', 'metrics', 'end'), 'Unknown scene kind')
        if s['kind'] == 'graph':
            nodes, edges = s.get('nodes'), s.get('edges', [])
            require(isinstance(nodes, list) and 0 < len(nodes) <= 8, 'Expected 1–8 nodes')
            require(isinstance(edges, list) and len(edges) <= 20, 'Expected at most 20 edges')
            node_ids = set()
            for n in nodes:
                require(isinstance(n, dict) and isinstance(n.get('id'), str), 'Invalid node')
                require(n['id'] and n['id'] not in node_ids, 'Duplicate/empty node ID'); node_ids.add(n['id'])
                require(isinstance(n.get('label'), str) and 0 < len(n['label']) <= 60, 'Invalid node label')
                require(all(finite(n.get(k)) and .1 <= n[k] <= .9 for k in ('x', 'y')), 'Invalid node coordinates')
                require(n.get('tone', 'accent') in COLORS, 'Invalid node tone')
            for e in edges:
                require(isinstance(e, dict) and e.get('from') in node_ids and e.get('to') in node_ids, 'Undefined edge endpoint')
                require(e.get('tone', 'accent') in COLORS and e['from'] != e['to'], 'Invalid edge')
        elif s['kind'] == 'metrics':
            items = s.get('items')
            require(isinstance(items, list) and 0 < len(items) <= 3, 'Expected 1–3 metrics')
            require(all(isinstance(i, dict) and all(isinstance(i.get(k), str) and i[k] for k in ('value', 'label')) for i in items), 'Invalid metric')
        else:
            require(isinstance(s.get('lines'), list) and 0 < len(s['lines']) <= 10, 'Expected 1–10 code lines')
            require(all(isinstance(line, str) for line in s['lines']), 'Code lines must be strings')
            require(isinstance(s.get('label', ''), str), 'Invalid code label')
            h = s.get('highlight', [])
            require(isinstance(h, list) and all(type(i) is int and 0 <= i < len(s['lines']) for i in h), 'Invalid highlight indices')
    require(sum(s['duration'] for s in scenes) <= 300, 'Maximum runtime is 300 seconds')


def ease(x):
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3


class Renderer:
    def __init__(self, data, size, font, mono):
        self.data, self.w, self.h = data, *size
        self.portrait = self.h > self.w
        self.scale = self.w / 1080 if self.portrait else self.h / 1080
        self.font_path, self.mono_path = font, mono
        self.fonts = {}
        self.total = sum(s['duration'] for s in data['scenes'])

    def font(self, size, mono=False):
        key = (size, mono)
        if key not in self.fonts:
            self.fonts[key] = ImageFont.truetype(str(self.mono_path if mono else self.font_path), round(size * self.scale))
        return self.fonts[key]

    def text(self, draw, content, xy, size, color=FG, width=None, max_lines=1, mono=False):
        font, lines = self.font(size, mono), []
        for paragraph in content.split('\n'):
            line = ''
            for word in paragraph.split(' '):
                require(width is None or draw.textlength(word, font=font) <= width, f'Unbreakable text overflows: {word}')
                candidate = (line + ' ' + word).strip()
                if width and draw.textlength(candidate, font=font) > width and line:
                    lines.append(line); line = word
                else:
                    line = candidate
            lines.append(line)
        require(len(lines) <= max_lines, f'Text needs {len(lines)} lines, allowed {max_lines}: {content}')
        for i, line in enumerate(lines):
            draw.text((xy[0], xy[1] + i * size * 1.18 * self.scale), line, font=font, fill=color)
        return len(lines) * size * 1.18 * self.scale

    def frame(self, t):
        w, h, z, p = self.w, self.h, self.scale, self.portrait
        offset = 0
        for index, s in enumerate(self.data['scenes']):
            if t < offset + s['duration'] or index == len(self.data['scenes']) - 1:
                local = max(0, t - offset); break
            offset += s['duration']
        im = Image.new('RGB', (w, h), BG); d = ImageDraw.Draw(im)
        margin = w * .065 if p else w * .045
        d.line((margin, h * .105, w - margin, h * .105), fill='#34373F', width=max(1, round(z)))
        self.text(d, self.data['brand'], (margin, h * .055), 30, COLORS['accent'], w * .62)
        self.text(d, f'{index+1:02d} / {len(self.data["scenes"]):02d}', (w - margin - 140*z, h*.055), 28, MUTED)
        tx, ty, tw = margin, h * (.145 if p else .20), w * (.87 if p else .39)
        self.text(d, s['eyebrow'], (tx, ty), 23, COLORS['good'], tw)
        self.text(d, s['title'], (tx, ty + 50*z), 86 if p else 82, width=tw, max_lines=3 if p else 5)
        self.text(d, s['body'], (tx, h * (.335 if p else .65)), 38 if p else 32, MUTED, tw, 3)
        gx, gy, gw, gh = (margin, h*.46, w*.87, h*.30) if p else (w*.49, h*.23, w*.455, h*.48)
        if s['kind'] == 'graph':
            nodes = {n['id']: n for n in s['nodes']}
            pos = lambda n: (gx + n['x']*gw, gy + n['y']*gh)
            for e_index, e in enumerate(s.get('edges', [])):
                a, b = pos(nodes[e['from']]), pos(nodes[e['to']])
                progress = ease((local - .65 - e_index*.13)/1.2)
                end = (a[0]+(b[0]-a[0])*progress, a[1]+(b[1]-a[1])*progress)
                color = COLORS[e.get('tone', 'accent')]
                d.line((*a, *b), fill='#333640', width=round(3*z))
                if e.get('tone') == 'gap':
                    for j in range(0, 20, 2):
                        q, r = j/20, min((j+1)/20, progress)
                        if q < progress:
                            d.line((a[0]+(b[0]-a[0])*q, a[1]+(b[1]-a[1])*q, a[0]+(b[0]-a[0])*r, a[1]+(b[1]-a[1])*r), fill=color, width=round(4*z))
                else:
                    d.line((*a, *end), fill=color, width=round(4*z))
                q = ((local*.28 + e_index*.22) % 1) * progress
                cx, cy = a[0]+(b[0]-a[0])*q, a[1]+(b[1]-a[1])*q
                d.ellipse((cx-6*z, cy-6*z, cx+6*z, cy+6*z), fill=color)
            for ni, n in enumerate(s['nodes']):
                x, y = pos(n); r = (22+9*ease((local-ni*.15)/.7))*z
                color = COLORS[n.get('tone', 'accent')]
                d.ellipse((x-r, y-r, x+r, y+r), fill=BG, outline=color, width=round(3*z))
                d.ellipse((x-5*z, y-5*z, x+5*z, y+5*z), fill=color)
                label_width = min(250*z, gw*.36)
                self.text(d, n['label'], (x-label_width/2, y+42*z), 36 if p else 32, FG, label_width, 2)
        elif s['kind'] == 'metrics':
            for i, item in enumerate(s['items']):
                y = gy + i*gh/len(s['items'])
                self.text(d, item['value'], (gx, y), 100 if p else 90, COLORS['good'], gw*.43)
                self.text(d, item['label'], (gx+gw*.48, y+15*z), 36 if p else 32, FG, gw*.52, 2)
        else:
            self.text(d, s.get('label', 'TERMINAL' if s['kind']=='end' else 'CODE EXCERPT'), (gx, gy-50*z), 23, COLORS['accent'], gw)
            line_size = 38 if p else 33
            line_height = min(54*z, gh/max(1, len(s['lines'])))
            require(line_height >= line_size*1.15*z, 'Code block too tall')
            for li, line in enumerate(s['lines']):
                y = gy + li*line_height
                require(d.textlength(line, font=self.font(line_size, True)) <= gw, f'Code line overflows: {line}')
                if li in s.get('highlight', []):
                    d.rectangle((gx-10*z, y-3*z, gx+gw, y+line_height-3*z), fill='#26372F')
                self.text(d, line, (gx, y), line_size, COLORS['good'] if li in s.get('highlight', []) else FG, mono=True)
        self.text(d, s['caption'], (margin, h*.84), 40 if p else 36, FG, w-2*margin, 3 if p else 2)
        self.text(d, self.data['author'], (margin, h*.945), 32 if p else 28, MUTED, w-2*margin)
        d.rectangle((margin, h*.925, w-margin, h*.927), fill='#34373F')
        d.rectangle((margin, h*.925, margin+(w-2*margin)*min(1, t/self.total), h*.927), fill=COLORS['accent'])
        return im


def score(path, scenes, rate=48000):
    starts, clock = [], 0
    for s in scenes:
        starts.append(clock); clock += s['duration']
    frequencies = (130.81, 164.81, 196.00, 246.94)
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(rate)
        for second in range(math.ceil(clock)):
            samples = array('h')
            for j in range(min(rate, round(clock*rate)-second*rate)):
                t = second+j/rate; beat = t % .5
                envelope = min(1, t/2, (clock-t)/2)
                hz = frequencies[int(t*2) % len(frequencies)]
                tone = .055*math.exp(-beat*9)*math.sin(2*math.pi*hz*t)
                tone += .018*math.sin(2*math.pi*65.405*t)
                for start in starts:
                    dt = t-start
                    if 0 <= dt < .15:
                        tone += .07*math.exp(-dt*36)*math.sin(2*math.pi*880*dt)
                samples.append(round(32767*tone*max(0, envelope)))
            if sys.byteorder != 'little': samples.byteswap()
            out.writeframes(samples.tobytes())


def captions(data, path):
    def stamp(seconds):
        ms = round(seconds*1000)
        return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    rows, t = [], 0
    for i, s in enumerate(data['scenes']):
        rows.append(f'{i+1}\n{stamp(t)} --> {stamp(t+s["duration"])}\n{s["caption"]}\n')
        t += s['duration']
    path.write_text('\n'.join(rows), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('storyboard', type=Path); ap.add_argument('--output', type=Path)
    ap.add_argument('--font', type=Path, required=True); ap.add_argument('--mono-font', type=Path, required=True)
    ap.add_argument('--size', default='1080x1920'); ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--score', action='store_true'); ap.add_argument('--poster', type=Path)
    ap.add_argument('--still', type=float); ap.add_argument('--validate-only', action='store_true')
    ap.add_argument('--overwrite', action='store_true'); args = ap.parse_args()
    data = json.loads(args.storyboard.read_text(encoding='utf-8')); validate(data)
    size = tuple(map(int, args.size.split('x')))
    require(len(size)==2 and all(640 <= n <= 3840 and n%2==0 for n in size), 'Invalid even output dimensions')
    require(args.fps in (24, 25, 30, 60), 'Unsupported frame rate')
    renderer = Renderer(data, size, args.font, args.mono_font)
    require(all(abs(s['duration']*args.fps-round(s['duration']*args.fps)) < 1e-6 for s in data['scenes']), 'Scene durations must align to frames')
    elapsed = 0
    for s in data['scenes']:
        renderer.frame(elapsed+min(2, s['duration']/2)); elapsed += s['duration']
    if args.validate_only:
        print(json.dumps({'scenes': len(data['scenes']), 'seconds': elapsed, 'layout': args.size})); return
    require(args.still is None or finite(args.still) and 0 <= args.still < elapsed, 'Still time outside timeline')
    require(args.still is None or args.poster, '--still requires --poster')
    require(args.still is not None or args.output, '--output is required for video')
    targets = [args.poster] if args.still is not None else [args.output, args.output.with_suffix('.srt'), args.poster]
    targets = [p for p in targets if p]
    require(len(set(p.resolve() for p in targets)) == len(targets), 'Output paths must differ')
    require(all(p.resolve() not in (args.storyboard.resolve(), args.font.resolve(), args.mono_font.resolve()) for p in targets), 'Cannot overwrite source inputs')
    require(args.overwrite or not any(p.exists() for p in targets), 'Output exists; use --overwrite intentionally')
    for path in targets: path.parent.mkdir(parents=True, exist_ok=True)
    if args.still is not None:
        renderer.frame(args.still).save(args.poster); return
    require(shutil.which('ffmpeg'), 'FFmpeg is required')
    with tempfile.TemporaryDirectory(prefix='viz-', dir=args.output.parent) as tmp:
        tmp = Path(tmp); audio, video = tmp/'score.wav', tmp/'render.mp4'
        command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', args.size, '-r', str(args.fps), '-i', 'pipe:0']
        if args.score:
            score(audio, data['scenes']); command += ['-i', str(audio), '-af', 'loudnorm=I=-20:TP=-2:LRA=9', '-c:a', 'aac', '-b:a', '128k']
        command += ['-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-t', str(elapsed), str(video)]
        with (tmp/'encoder.log').open('w+') as log:
            proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=log)
            try:
                for i in range(round(elapsed*args.fps)): proc.stdin.write(renderer.frame(i/args.fps).tobytes())
                proc.stdin.close(); require(proc.wait()==0, 'FFmpeg failed')
            except BaseException:
                proc.kill(); proc.wait(); log.seek(0); print(log.read(), file=sys.stderr); raise
        video.replace(args.output)
    captions(data, args.output.with_suffix('.srt'))
    if args.poster: renderer.frame(min(2, elapsed/2)).save(args.poster)
    print(json.dumps({'output': str(args.output), 'seconds': elapsed, 'frames': round(elapsed*args.fps)}))


if __name__ == '__main__':
    try: main()
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f'Render failed: {error}', file=sys.stderr); sys.exit(1)
