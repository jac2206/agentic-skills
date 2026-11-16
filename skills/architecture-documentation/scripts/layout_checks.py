"""Heuristic checks of Draw.io boundary titles and explicit orthogonal routes."""

import html
import re


def _lines(value):
    text = html.unescape(value or "")
    text = re.sub(r"(?i)<br\s*/?>|</?(?:div|p)[^>]*>", "\n", text)
    return [s for s in re.sub(r"<[^>]+>", "", text).splitlines() if s.strip()]


def _overlap(a, b):
    return min(a[2], b[2]) - max(a[0], b[0]) > 4 and min(a[3], b[3]) - max(a[1], b[1]) > 4


def _title_box(c):
    s, (x, y, w, h) = c['style'], c['geo']
    lines = _lines(c['value'])
    fs = float(s.get('fontSize', 12))
    width = min(w, max(len(line) for line in lines) * fs * 0.56 + 8)
    height = len(lines) * fs * 1.25 + 4
    align, valign = s.get('align', 'center'), s.get('verticalAlign', 'middle')
    spacing_x = float(s.get('spacing', 0)) + float(s.get('spacingLeft', 0))
    spacing_y = float(s.get('spacing', 0)) + float(s.get('spacingTop', 0))
    left = x + spacing_x if align == 'left' else x + w - width - spacing_x if align == 'right' else x + (w - width) / 2
    top = y + spacing_y if valign == 'top' else y + h - height if valign == 'bottom' else y + (h - height) / 2
    return left, top, left + width, top + height


def _intersects_segment(box, a, b):
    x1, y1, x2, y2 = box
    if abs(a[1] - b[1]) < .5:
        return y1 < a[1] < y2 and min(a[0], b[0]) < x2 and max(a[0], b[0]) > x1
    if abs(a[0] - b[0]) < .5:
        return x1 < a[0] < x2 and min(a[1], b[1]) < y2 and max(a[1], b[1]) > y1
    return False


def _relationship(a, b, c, d):
    if (abs(a[0]-b[0]) < .5 and abs(a[1]-b[1]) < .5) or (abs(c[0]-d[0]) < .5 and abs(c[1]-d[1]) < .5):
        return None
    ah, bh = abs(a[1]-b[1]) < .5, abs(c[1]-d[1]) < .5
    av, bv = abs(a[0]-b[0]) < .5, abs(c[0]-d[0]) < .5
    if ah and bh and abs(a[1]-c[1]) < .5 and min(max(a[0], b[0]), max(c[0], d[0])) - max(min(a[0], b[0]), min(c[0], d[0])) > 8:
        return 'share a segment'
    if av and bv and abs(a[0]-c[0]) < .5 and min(max(a[1], b[1]), max(c[1], d[1])) - max(min(a[1], b[1]), min(c[1], d[1])) > 8:
        return 'share a segment'
    if ah and bv and min(a[0], b[0]) + 1 < c[0] < max(a[0], b[0]) - 1 and min(c[1], d[1]) + 1 < a[1] < max(c[1], d[1]) - 1:
        return 'cross'
    if av and bh:
        return _relationship(c, d, a, b)
    return None


def check_layout(name, cells, warnings, edge_label_box):
    """Warn on estimated collisions only; auto-routed paths remain unverified."""
    parents = {c['parent'] for c in cells.values()}
    frames = []
    for c in cells.values():
        if c['geo'] is None or c['edge'] or not _lines(c['value']):
            continue
        s = c['style']
        if (c['el'].get('data-role') == 'boundary' or c['id'] in parents or
                'swimlane' in s or s.get('shape') == 'swimlane' or
                (s.get('fillColor') == 'none' and s.get('dashed') == '1' and s.get('verticalAlign') == 'top')):
            frames.append((c['id'], _title_box(c)))
    routes, labels = [], []
    for c in cells.values():
        if not c['edge']:
            continue
        el, s = c['el'], c['style']
        source, target = cells.get(el.get('source')), cells.get(el.get('target'))
        if not source or not target or source['geo'] is None or target['geo'] is None:
            continue
        if not all(k in s for k in ('exitX', 'exitY', 'entryX', 'entryY')):
            continue
        if not (s.get('edgeStyle') == 'none' and str(s.get('noEdgeStyle')) == '1'):
            warnings.append(f"[{name}] edge {c['id']} uses a router; estimated path may differ from rendered path")
        def anchor(node, x, y):
            gx, gy, w, h = node['geo']
            return gx + w * float(s[x]), gy + h * float(s[y])
        parent = cells.get(c['parent'])
        px, py = parent['geo'][:2] if parent and parent['geo'] else (0, 0)
        points = [(float(p.get('x', 0)) + px, float(p.get('y', 0)) + py)
                  for p in el.findall("./mxGeometry/Array[@as='points']/mxPoint")]
        path = [anchor(source, 'exitX', 'exitY')] + points + [anchor(target, 'entryX', 'entryY')]
        if any(abs(a[0]-b[0]) > .5 and abs(a[1]-b[1]) > .5 for a, b in zip(path, path[1:])):
            continue
        # An endpoint is allowed to touch its shape at the attachment point, but
        # the route must not travel through its interior, including after a turn.
        # Center anchors, custom perimeters and nonrectangular shapes are only
        # approximated by their bounding boxes and require manual review.
        for role, node in (('source', source), ('target', target)):
            x, y, w, h = node['geo']
            inset = min(2.0, w / 4, h / 4)
            box = (x + inset, y + inset, x + w - inset, y + h - inset)
            if any(_intersects_segment(box, a, b) for a, b in zip(path, path[1:])):
                warnings.append(f"[{name}] edge {c['id']} crosses {role} component interior {node['id']}; check anchor and label")
        routes.append((c['id'], path))
        geometry = el.find('mxGeometry')
        if _lines(c['value']) and geometry is not None and float(geometry.get('y', 0)) == 0:
            box = edge_label_box(path, c['value'], float(s.get('fontSize', 12)), geometry)
            if box:
                labels.append((c['id'], box))
    for title_id, title in frames:
        for cell in cells.values():
            if cell['geo'] is None or cell['edge'] or 'text' not in cell['style'] or not _lines(cell['value']):
                continue
            x, y, w, h = cell['geo']
            if _overlap(title, (x, y, x + w, y + h)):
                warnings.append(f"[{name}] estimated boundary title {title_id} overlaps text {cell['id']}")
        for edge_id, box in labels:
            if _overlap(title, box):
                warnings.append(f'[{name}] estimated boundary title {title_id} overlaps edge label {edge_id}')
        for edge_id, path in routes:
            if any(_intersects_segment(title, a, b) for a, b in zip(path, path[1:])):
                warnings.append(f'[{name}] edge {edge_id} crosses estimated boundary title {title_id}')
    for i, (first, path) in enumerate(routes):
        for second, other in routes[i+1:]:
            relations = {_relationship(a, b, c, d) for a, b in zip(path, path[1:]) for c, d in zip(other, other[1:])}
            for relation in sorted(relations - {None}):
                warnings.append(f'[{name}] edges {first} and {second} {relation}')
    for edge_id, box in labels:
        for other_id, path in routes:
            if edge_id != other_id and any(_intersects_segment(box, a, b) for a, b in zip(path, path[1:])):
                warnings.append(f'[{name}] edge {other_id} crosses estimated edge label {edge_id}')
