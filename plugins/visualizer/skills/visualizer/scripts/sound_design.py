#!/usr/bin/env python3
"""Optional Openverse -> Earshot -> Real SFX bridge. No installs or model downloads."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_CONFIG = Path.home() / '.local/share/sigmastudioz/visualization-sound-tools/config.json'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def number(value, name, low, high):
    require(isinstance(value, (float, int)) and not isinstance(value, bool)
            and math.isfinite(value) and low <= value <= high, f'Invalid {name}')
    return float(value)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def fresh(path):
    path = Path(path).resolve()
    require(not path.exists(), f'Output already exists: {path}; choose a new path')
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def mix_output(path):
    """Reserve the upstream filename namespace before its -y commands can write."""
    out = fresh(path)
    require(out.suffix.lower() == '.mp4', 'Mix output must use the .mp4 extension')
    collisions = [p for p in out.parent.iterdir()
                  if p.name.startswith(out.stem + '_')
                  or p.name in (out.stem + '.sound-work', out.stem + '.sound-report.json')]
    require(not collisions, 'Existing mix sidecar/work output: ' + ', '.join(str(p) for p in collisions))
    return out


def runtime(path):
    c = load(path)
    for key in ('python', 'ffmpeg', 'ffprobe', 'real_sfx_root', 'earshot_root'):
        require(Path(c[key]).exists(), f'Missing runtime {key}: {c[key]}')
    env = dict(os.environ, EARSHOT_OFFLINE='1', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
    env['PATH'] = str(Path(c['ffmpeg']).parent) + os.pathsep + env.get('PATH', '')
    for name, root in (('earshot', Path(c['earshot_root'])), ('real_sfx', Path(c['real_sfx_root']).parents[1])):
        head = run(['git', '-C', root, 'rev-parse', 'HEAD'], env).strip()
        require(head == c['revisions'][name], f'{name} revision differs from the runtime config')
        run(['git', '-C', root, 'diff', '--exit-code', '--quiet', 'HEAD'], env)
    return c, env


def run(args, env=None, timeout=180):
    p = subprocess.run([str(x) for x in args], env=env, capture_output=True,
                       text=True, timeout=timeout)
    require(p.returncode == 0, f'Command failed ({p.returncode}): {args[0]}\n{p.stderr[-2000:]}\n{p.stdout[-1000:]}')
    return p.stdout


def probe(path, c, env):
    return json.loads(run([c['ffprobe'], '-v', 'error', '-show_format', '-show_streams',
                           '-of', 'json', path], env))


def get(url, limit=4 * 1024 * 1024, attempts=2):
    require(urllib.parse.urlparse(url).scheme == 'https', 'Only HTTPS downloads are supported')
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'SigmaStudioz-Visualization/1.0',
                                                       'Accept': '*/*'})
            with urllib.request.urlopen(req, timeout=25) as response:
                if response.headers.get('Content-Length'):
                    require(int(response.headers['Content-Length']) <= limit, 'Download too large')
                data = response.read(limit + 1)
                require(len(data) <= limit, 'Download too large')
                return data
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt + 1 == attempts:
                raise
            delay = e.headers.get('Retry-After', '1')
            require(delay.isdigit() and int(delay) <= 5, 'Service requests a longer wait; retry later')
            time.sleep(int(delay))
        except (TimeoutError, urllib.error.URLError):
            if attempt + 1 == attempts:
                raise
            time.sleep(1)


def search(query, output, license_name='cc0', browse=False, source='freesound'):
    require((browse and not query) or (isinstance(query, str) and 0 < len(query) <= 200 and not browse),
            'Supply a 1-200 character query OR --browse without a query')
    out = fresh(output)
    params = {'license': license_name, 'source': source, 'page_size': 5}
    if not browse:
        params['q'] = query
    params = urllib.parse.urlencode(params)
    url = 'https://api.openverse.org/v1/audio/?' + params
    result = json.loads(get(url))
    require(isinstance(result, dict) and isinstance(result.get('results'), list), 'Not an Openverse results response')
    save(out, {'request_url': url, 'strategy': 'filtered-browse' if browse else 'keyword',
               'retrieved_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'response': result})
    return {'output': str(out), 'results': [{k: r.get(k) for k in
             ('id', 'title', 'creator', 'license', 'foreign_landing_url', 'url')}
             for r in result['results']]}


def fetch(results, item_id, output, rights_note, c, env):
    require(bool(rights_note.strip()), 'Record the original-item rights review in --rights-note')
    data = load(results)
    item = next((r for r in data['response']['results'] if r['id'] == item_id), None)
    require(item is not None, 'Item ID is absent from these search results')
    require(all(item.get(k) for k in ('foreign_landing_url', 'url', 'license', 'license_url')),
            'Source item lacks required rights fields')
    out = fresh(output)
    prov = fresh(str(out) + '.provenance.json')
    try:
        out.write_bytes(get(item['url'], limit=50 * 1024 * 1024))
        require(any(s['codec_type'] == 'audio' for s in probe(out, c, env)['streams']), 'Downloaded file has no audio')
    except Exception:
        out.unlink(missing_ok=True)
        raise
    save(prov, {'kind': 'download', 'sha256': sha(out), 'rights_status': 'reviewed',
                'rights_note': rights_note, 'source': item, 'search_request': data['request_url'],
                'retrieved_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    return {'output': str(out), 'provenance': str(prov), 'sha256': sha(out)}


def generate(sound, output, duration, apex, seed, c, env):
    number(duration, 'duration', .05, 30)
    if apex is not None:
        number(apex, 'apex', 0, duration)
    out = fresh(output)
    prov = fresh(str(out) + '.provenance.json')
    cmd = [c['python'], '-m', 'earshot', 'sfx', 'render', sound, '-o', out,
           '--dur', str(duration), '--seed', str(seed), '--json']
    if apex is not None:
        cmd += ['--apex', str(apex)]
    report = json.loads(run(cmd, env))
    require(out.is_file(), 'Earshot did not write the requested WAV')
    save(prov, {'kind': 'generated', 'sha256': sha(out), 'rights_status': 'reviewed',
                'rights_note': 'Original DSP bank recipe; no user recording supplied. Tool code MIT.',
                'tool': 'https://github.com/Leonxlnx/earshot',
                'revision': c['revisions']['earshot'], 'recipe': sound, 'seed': seed,
                'duration': duration, 'apex': apex, 'earshot': report})
    return {'output': str(out), 'provenance': str(prov), 'earshot': report}


def prepare(plan_path, c, env):
    plan_path = Path(plan_path).resolve()
    p = load(plan_path)
    base = plan_path.parent
    resolve = lambda value: (base / value).resolve()
    video = resolve(p['video'])
    require(video.is_file() and sha(video) == p['picture_sha256'], 'Picture missing or revision hash is stale')
    meta = probe(video, c, env)
    duration = float(meta['format']['duration'])
    require(any(s['codec_type'] == 'video' for s in meta['streams']), 'Picture has no video stream')
    require(p.get('mode') in ('voice', 'music', 'effects'), 'Choose mode: voice, music, effects')
    require(type(p.get('preserve_original')) is bool, 'Declare preserve_original explicitly as true or false')
    stems = [str(resolve(x)) for x in p.get('base_audio', [])]
    require(all(Path(x).is_file() for x in stems), 'A base audio stem is missing')
    require(not (stems and p['preserve_original']), 'Choose clean base stems OR original audio, not both')
    if p['mode'] == 'voice':
        require(stems or (p['preserve_original'] and any(s['codec_type'] == 'audio' for s in meta['streams'])),
                'Voice mode needs base audio or the original audio track')
    if 'target_lufs' in p:
        number(p['target_lufs'], 'target_lufs', -40, -9)
    cues, silence, ids, provenance = [], [], set(), []
    for cue in p['cues']:
        require(isinstance(cue.get('id'), str) and cue['id'] and cue['id'] not in ids, 'Duplicate/empty cue ID')
        ids.add(cue['id'])
        require(bool(cue.get('purpose')), 'Each cue, including silence, needs a purpose')
        t = number(cue['time'], 'cue time', 0, duration)
        if cue.get('silence'):
            silence.append(cue)
            continue
        offset = number(cue.get('intentional_offset', 0), 'offset', -2, 2)
        t += offset
        require(0 <= t <= duration, 'Offset moves cue outside picture')
        file = resolve(cue['file'])
        proof = load(resolve(cue['provenance']))
        require(proof.get('kind') in ('download', 'generated', 'local'), 'Provenance needs download, generated or local kind')
        require(proof.get('rights_status') == 'reviewed' and proof.get('rights_note'), 'Asset rights are not reviewed')
        require(sha(file) == proof['sha256'], 'Asset hash differs from its provenance')
        require(cue['anchor'] in ('start', 'peak', 'end'), 'Anchor must be start (audible onset), peak or end')
        require(cue['role'] in ('click', 'whoosh', 'hit', 'pop', 'chime', 'paper', 'foley', 'ambience'), 'Unsupported role')
        row = {'t': t, 'label': cue['id'], 'file': str(file), 'role': cue['role'], 'anchor': cue['anchor'],
               'gain_db': number(cue.get('gain_db', 0), 'gain_db', -60, 12)}
        for key, low, high in (('fade_in', 0, 5), ('fade_out', 0, 5), ('pan', -1, 1)):
            if key in cue:
                row[key] = number(cue[key], key, low, high)
        cues.append(row)
        provenance.append({'cue_id': cue['id'], 'provenance': proof})
    require(cues, 'No sounded cues; retain the silent/original edit instead of invoking the SFX mixer')
    sheet = {'video': str(video), 'duration': duration, 'keep_audio': 'yes' if p['preserve_original'] or stems else 'no',
             'base_audio': stems, 'cues': cues}
    return p, sheet, provenance, silence, meta


def mix(plan_path, output, c, env):
    p, sheet, provenance, silence, meta = prepare(plan_path, c, env)
    out = mix_output(output)
    work = out.parent / (out.stem + '.sound-work')
    require(not work.exists(), f'Work directory already exists: {work}')
    work.mkdir()
    save(work / 'real-sfx-cues.json', sheet)
    save(work / 'real-sfx-config.json', {'libraries': [], 'index_path': str(work / 'index.json'),
                                      'uisfx': {'path': str(work / 'unused-ui-pack')}})
    save(work / 'index.json', {'sounds': [], 'count': 0})
    env = dict(env, REAL_SFX_CONFIG=str(work / 'real-sfx-config.json'), REAL_SFX_INDEX=str(work / 'index.json'))
    cmd = [c['python'], str(Path(c['real_sfx_root']) / 'scripts/mix.py'), str(work / 'real-sfx-cues.json'),
           '--out', str(out), '--stems', '--no-tonal-fit']
    if p['mode'] == 'voice':
        cmd += ['--voice-safe']
    elif p['mode'] == 'music':
        cmd += ['--duck']
    if 'target_lufs' in p:
        cmd += ['--target-lufs', str(p['target_lufs'])]
    else:
        cmd += ['--no-loudnorm']
    (work / 'plan.txt').write_text(run(cmd + ['--plan'], env, timeout=600))
    (work / 'mix.txt').write_text(run(cmd, env, timeout=600))
    resolved_path = out.with_name(out.stem + '_resolved_cues.json')
    resolved = load(resolved_path)
    require({x['label'] for x in resolved['cues']} == {x['label'] for x in sheet['cues']}, 'Mixer dropped/changed cue identities')
    for r in resolved['cues']:
        require(abs(r['t'] - next(x['t'] for x in sheet['cues'] if x['label'] == r['label'])) < .001,
                'Mixer moved an authored cue')
        require(r['start'] + r['seg'] <= sheet['duration'] + .002, 'Sound tail exceeds picture; extend picture or choose a shorter sound')
        anchor = {'start': r['onset_shift_ms'] / 1000, 'peak': r['peak_time'], 'end': r['seg']}[r['anchor']]
        require(r['start'] > 0 or r['t'] - anchor >= -.002, 'Cue needs pre-roll; do not silently truncate it')
    run([c['ffmpeg'], '-v', 'error', '-i', out, '-f', 'null', '-'], env)
    final_meta = probe(out, c, env)
    require(any(s['codec_type'] == 'audio' for s in final_meta['streams']), 'Export is missing audio')
    require(abs(float(final_meta['format']['duration']) - sheet['duration']) < .1, 'Export duration changed')
    meters = resolved['loudness']['final']
    number(meters['lufs'], 'measured LUFS', -100, 0)
    require(number(meters['true_peak'], 'measured true peak', -100, 20) <= -.95,
            'Encoded true peak exceeds the -1 dBTP ceiling')
    report = {'output': str(out), 'sha256': sha(out), 'plan_sha256': sha(plan_path),
              'adapter_sha256': sha(__file__),
              'picture_sha256': p['picture_sha256'], 'tools': c['revisions'],
              'decode': 'passed', 'duration': final_meta['format']['duration'],
              'resolved_cues': str(resolved_path), 'loudness': resolved['loudness'],
              'voice_safe': resolved['flags']['voice_safe'], 'voice_key': resolved['voice_key'],
              'intentional_silence': silence, 'assets': provenance,
              'cue_sources': {a['cue_id']: a['provenance']['kind'] for a in provenance},
              'listening_review': 'required; file/measurement checks do not establish taste'}
    save(out.with_suffix('.sound-report.json'), report)
    return report


def doctor(c, env):
    run([c['python'], str(Path(c['real_sfx_root']) / 'scripts/mix.py'), '--help'], env)
    earshot = json.loads(run([c['python'], '-m', 'earshot', 'sfx', 'list', '--kind', 'whoosh', '--json'], env))
    filters = run([c['ffmpeg'], '-hide_banner', '-filters'], env)
    return {'core_ready': True, 'revisions': c['revisions'], 'earshot_bank': earshot,
            'real_sfx_mixer': str(Path(c['real_sfx_root']) / 'scripts/mix.py'),
            'optional_filters': {x: x in filters for x in ('drawtext', 'rubberband')},
            'network_search': 'not checked by doctor', 'model_downloads': 'disabled'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    s = sub.add_parser('search'); s.add_argument('query', nargs='?'); s.add_argument('--output', required=True)
    s.add_argument('--license', default='cc0')
    s.add_argument('--source', default='freesound'); s.add_argument('--browse', action='store_true')
    f = sub.add_parser('fetch'); f.add_argument('results'); f.add_argument('--id', required=True)
    f.add_argument('--output', required=True); f.add_argument('--rights-note', required=True)
    g = sub.add_parser('generate'); g.add_argument('sound'); g.add_argument('--output', required=True)
    g.add_argument('--duration', type=float, required=True); g.add_argument('--apex', type=float)
    g.add_argument('--seed', type=int, default=42)
    m = sub.add_parser('mix'); m.add_argument('plan'); m.add_argument('--output', required=True)
    a = ap.parse_args()
    try:
        if a.command == 'search':
            result = search(a.query, a.output, a.license, a.browse, a.source)
        else:
            c, env = runtime(a.config)
            if a.command == 'doctor': result = doctor(c, env)
            elif a.command == 'fetch': result = fetch(a.results, a.id, a.output, a.rights_note, c, env)
            elif a.command == 'generate': result = generate(a.sound, a.output, a.duration, a.apex, a.seed, c, env)
            else: result = mix(a.plan, a.output, c, env)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, KeyError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as e:
        ap.exit(1, f'sound-design: {e}\n')


if __name__ == '__main__':
    main()
