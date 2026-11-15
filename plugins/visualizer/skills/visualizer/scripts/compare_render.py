#!/usr/bin/env python3
"""Compare a page screenshot with a reference render of the same camera. By Lex from SigmaStudioz.

Answers one question with numbers: does the real-time picture match the offline one?
Brightness is compared in linear light, region by region, because a single average hides a
floor that is too dark behind a wall that is too bright. NumPy and Pillow only; no network.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw

LUMA = np.array([.2126, .7152, .0722])
# Below this linear luminance (about 14/255 on screen) a ratio is mostly noise.
DARK_FLOOR = .004


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    """8-bit sRGB pixels as floats 0–1. Transparency is refused: it hides what was drawn."""
    with Image.open(path) as image:
        if image.mode in ('RGBA', 'LA', 'PA') or 'transparency' in image.info:
            alpha = np.asarray(image.convert('RGBA'))[..., 3]
            require(int(alpha.min()) == 255, f'{path} has transparent pixels; capture it on an opaque background')
        return np.asarray(image.convert('RGB'), dtype=np.float64) / 255


def to_linear(srgb):
    """Display-encoded sRGB to linear light (IEC 61966-2-1)."""
    return np.where(srgb <= .04045, srgb / 12.92, ((srgb + .055) / 1.055) ** 2.4)


def parse_grid(text):
    parts = str(text).lower().split('x')
    require(len(parts) == 2 and all(p.isdigit() for p in parts), 'Grid must be COLUMNSxROWS, e.g. 4x3')
    columns, rows = (int(p) for p in parts)
    require(1 <= columns <= 16 and 1 <= rows <= 16, 'Grid is limited to 16 columns and 16 rows')
    return columns, rows


def grid_regions(columns, rows):
    return [{'name': f'r{row + 1}c{column + 1}', 'x': column / columns, 'y': row / rows,
             'w': 1 / columns, 'h': 1 / rows} for row in range(rows) for column in range(columns)]


def named_regions(data):
    """Regions are fractions of the picture, top-left origin: {"name", "x", "y", "w", "h"}."""
    require(isinstance(data, list) and 0 < len(data) <= 64, 'Regions must be a list of 1–64 rectangles')
    names = set()
    for region in data:
        require(isinstance(region, dict) and isinstance(region.get('name'), str) and region['name'], 'Each region needs a name')
        require(region['name'] not in names, f'Duplicate region name: {region["name"]}')
        names.add(region['name'])
        values = [region.get(key) for key in ('x', 'y', 'w', 'h')]
        require(all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values),
                f'Region {region["name"]} needs numeric x, y, w, h')
        x, y, w, h = values
        require(0 <= x < 1 and 0 <= y < 1 and w > 0 and h > 0 and x + w <= 1 + 1e-9 and y + h <= 1 + 1e-9,
                f'Region {region["name"]} must lie inside the picture (fractions 0–1)')
    return data


def box(region, width, height):
    left, top = math.floor(region['x'] * width), math.floor(region['y'] * height)
    right = max(left + 1, min(width, math.ceil((region['x'] + region['w']) * width)))
    bottom = max(top + 1, min(height, math.ceil((region['y'] + region['h']) * height)))
    return left, top, right, bottom


def compare(candidate, reference, regions, tolerance=.10):
    """Both arrays are sRGB floats of the same shape. Returns the report dictionary."""
    require(candidate.shape == reference.shape and candidate.ndim == 3, 'Pictures must have the same size')
    require(0 < tolerance < 1, 'Tolerance must be between 0 and 1')
    height, width = reference.shape[:2]
    difference = np.abs(candidate - reference) * 255
    candidate_light, reference_light = to_linear(candidate) @ LUMA, to_linear(reference) @ LUMA
    rows = []
    for region in regions:
        left, top, right, bottom = box(region, width, height)
        ours = float(candidate_light[top:bottom, left:right].mean())
        theirs = float(reference_light[top:bottom, left:right].mean())
        row = {'name': region['name'], 'box_px': [left, top, right, bottom],
               'reference_luminance': round(theirs, 5), 'candidate_luminance': round(ours, 5),
               'mean_abs_difference_of_255': round(float(difference[top:bottom, left:right].mean()), 2)}
        if theirs < DARK_FLOOR:
            # Too dark for a ratio: judge by how far apart the two are on screen instead.
            row.update(ratio=None, judged_by='difference', passed=row['mean_abs_difference_of_255'] <= 255 * tolerance / 4)
        else:
            ratio = ours / theirs
            row.update(ratio=round(ratio, 3), judged_by='ratio', passed=abs(ratio - 1) <= tolerance)
        rows.append(row)
    judged = [row for row in rows if row['ratio'] is not None]
    worst = max(judged, key=lambda row: abs(row['ratio'] - 1)) if judged else None
    return {
        'size': [width, height], 'tolerance': tolerance,
        'mean_abs_difference_of_255': round(float(difference.mean()), 2),
        'pixels_over_16_of_255': round(float((difference.max(axis=2) > 16).mean()), 4),
        'overall_luminance_ratio': (round(float(candidate_light.mean() / reference_light.mean()), 3)
                                    if reference_light.mean() >= DARK_FLOOR else None),
        'regions': rows, 'failed_regions': [row['name'] for row in rows if not row['passed']],
        'worst_region': worst['name'] if worst else None,
        'passed': all(row['passed'] for row in rows),
        'meaning': 'Ratios are candidate ÷ reference mean luminance in linear light per region. '
                   'A pass says brightness agrees region by region; it does not judge colour, sharpness or taste.',
    }


def sheet(candidate, reference, report, path):
    """Candidate | reference | difference ×4, with each region outlined green (pass) or red (fail)."""
    height, width = reference.shape[:2]
    scale = min(1, 640 / width)
    size = (max(1, round(width * scale)), max(1, round(height * scale)))
    heat = np.clip(np.abs(candidate - reference).max(axis=2) * 4, 0, 1)
    panels = [Image.fromarray((candidate * 255).round().astype(np.uint8)),
              Image.fromarray((reference * 255).round().astype(np.uint8)),
              Image.fromarray((np.stack([heat, heat * .45, heat * .1], axis=2) * 255).round().astype(np.uint8))]
    out = Image.new('RGB', (size[0] * 3 + 16, size[1]), '#101216')
    for index, panel in enumerate(panels):
        panel = panel.resize(size, Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(panel)
        for row in report['regions']:
            left, top, right, bottom = (round(v * scale) for v in row['box_px'])
            draw.rectangle((left, top, right - 1, bottom - 1), outline='#89E5C1' if row['passed'] else '#FF6B5A')
        out.paste(panel, (index * (size[0] + 8), 0))
    out.save(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path, help='Screenshot of the page at the reference camera')
    parser.add_argument('reference', type=Path, help='Offline render of the same camera (for example Cycles)')
    parser.add_argument('--regions', type=Path, help='JSON list of named rectangles as fractions: name, x, y, w, h')
    parser.add_argument('--grid', default='4x3', help='Automatic regions when --regions is not given. Default 4x3')
    parser.add_argument('--tolerance', type=float, default=.10, help='Allowed luminance difference per region. Default 0.10')
    parser.add_argument('--report', type=Path, help='Write the JSON report here')
    parser.add_argument('--sheet', type=Path, help='Write a side-by-side picture with the difference here')
    args = parser.parse_args(argv)
    for path in (args.candidate, args.reference):
        require(path.is_file(), f'Missing picture: {path}')
    outputs = [p for p in (args.report, args.sheet) if p]
    require(all(not p.exists() for p in outputs), 'An output already exists; choose a new path')
    require(len({p.resolve() for p in outputs + [args.candidate, args.reference]}) == len(outputs) + 2, 'Paths must differ')
    candidate, reference = load(args.candidate), load(args.reference)
    # Never resample silently: a resized screenshot is a different picture.
    require(candidate.shape == reference.shape,
            f'Sizes differ: candidate {candidate.shape[1]}x{candidate.shape[0]}, reference '
            f'{reference.shape[1]}x{reference.shape[0]}. Capture the page at the reference size and device scale 1')
    regions = named_regions(json.loads(args.regions.read_text(encoding='utf-8'))) if args.regions else grid_regions(*parse_grid(args.grid))
    report = compare(candidate, reference, regions, args.tolerance)
    report.update(candidate=str(args.candidate), candidate_sha256=sha(args.candidate),
                  reference=str(args.reference), reference_sha256=sha(args.reference),
                  regions_source=str(args.regions) if args.regions else f'grid {args.grid}')
    for path in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    if args.sheet:
        sheet(candidate, reference, report, args.sheet)
    print(json.dumps({key: report[key] for key in ('passed', 'mean_abs_difference_of_255', 'overall_luminance_ratio',
                                                    'worst_region', 'failed_regions')}))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f'compare-render: {error}', file=sys.stderr)
        sys.exit(2)
