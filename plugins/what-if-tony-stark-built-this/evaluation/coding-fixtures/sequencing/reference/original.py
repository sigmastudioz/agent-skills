"""Album proposals preserve authored order separately and never rename source files."""
import math


def propose_sequence(tracks, opener=None, closer=None, keep_together=None):
    ids = [t['id'] for t in tracks]
    if not ids or any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('Provide distinct, nonempty track IDs.')
    if any(x is not None and x not in ids for x in [opener, closer]):
        raise ValueError('Opener/closer must identify supplied tracks.')
    if opener == closer and opener is not None and len(ids) > 1:
        raise ValueError('Different opener and closer required for multiple tracks.')
    groups = [] if keep_together is None else keep_together
    if not isinstance(groups, list):
        raise ValueError('keep_together must be a list of ordered ID blocks.')
    seen = set()
    for group in groups:
        if not isinstance(group, list) or not group:
            raise ValueError('Each keep_together block must be a nonempty ordered list.')
        for value in group:
            if value not in ids or value in seen:
                raise ValueError('Blocks must contain known IDs without overlap or repetition.')
            seen.add(value)
    units = [list(g) for g in groups] + [[i] for i in ids if i not in seen]
    units.sort(key=lambda g: ids.index(g[0]))
    first = next((g for g in units if opener in g), None) if opener else None
    last = next((g for g in units if closer in g), None) if closer else None
    if first and first[0] != opener or last and last[-1] != closer:
        raise ValueError('Pinned tracks conflict with the order inside a kept-together block.')
    if first is last and first is not None and len(units) > 1:
        raise ValueError('A block containing both pinned endpoints excludes remaining tracks.')
    by_id = {t['id']: t for t in tracks}

    def jump(a, b):
        tail, head = by_id[a].get('tail_rms_dbfs'), by_id[b].get('head_rms_dbfs')
        if tail is None or head is None:
            return None
        value = abs(tail - head)
        return round(value, 2) if math.isfinite(value) else None

    remaining = [g for g in units if g is not first and g is not last]
    if first:
        chosen = list(first)
    elif remaining:
        chosen = list(remaining.pop(0))
    else:
        chosen = []
    while remaining:
        # Technical continuity only: deterministic tie-breaking retains source order.
        unit = min(remaining, key=lambda g: (
            jump(chosen[-1], g[0]) if chosen and jump(chosen[-1], g[0]) is not None else math.inf,
            ids.index(g[0])))
        chosen.extend(unit)
        remaining.remove(unit)
    if last and last is not first:
        chosen.extend(last)
    edges = [{'from': a, 'to': b, 'rms_jump_db': jump(a, b),
              'review': 'Audition musical resolution, lyric/story continuity, gaps and intentional contrast.'}
             for a, b in zip(chosen, chosen[1:])]
    return {'original_order': ids, 'technical_flow_proposal': chosen,
            'basis': 'Greedy endpoint-level continuity; unmastered gain differences can mislead. Not an optimal or artistic tracklist.',
            'constraints': {'opener': opener, 'closer': closer, 'keep_together': groups},
            'transitions': edges, 'artistic_sequence_status': 'needs_artist_and_music_review'}


def validate_album_order(order, tracks, constraints):
    """Validate an editorial proposal through the same constraint owner as technical flow."""
    if not isinstance(constraints, dict) or set(constraints) - {'opener', 'closer', 'keep_together'}:
        raise ValueError('Invalid album constraints.')
    propose_sequence(tracks, **constraints)
    ids = [t['id'] for t in tracks]
    if not isinstance(order, list) or any(not isinstance(i, str) for i in order) or len(order) != len(ids) or set(order) != set(ids):
        raise ValueError('Album order must contain every supplied track exactly once.')
    if constraints.get('opener') is not None and order[0] != constraints['opener']:
        raise ValueError('Album order changed the pinned opener.')
    if constraints.get('closer') is not None and order[-1] != constraints['closer']:
        raise ValueError('Album order changed the pinned closer.')
    for block in constraints.get('keep_together') or []:
        start = order.index(block[0])
        if order[start:start + len(block)] != block:
            raise ValueError('Album order broke an ordered interlude/segue block.')
