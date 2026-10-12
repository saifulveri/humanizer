#!/usr/bin/env python3
"""Humanizer audit. Usage:
  audit.py scan  <file...> [--out report.json]      flag banned words, stats
  audit.py facts <copy.json>                         check numbers/names kept in key->value pairs
  audit.py diff  <old-report.json> <new-report.json> compare two scans
Files: .json (string values scanned; key->value maps scanned on values only) or .html/.md/.txt (tags stripped)."""
import json, re, sys, statistics, collections, html

BANNED = {
 'formal_id': r'\b(serta|secara|berbagai|beragam|ditambah|solusi|mengelola|berbasis|memungkinkan|dilengkapi|merupakan|sebuah|menyeluruh|komprehensif|krusial|signifikan|optimal|mutakhir|kokoh|lintas platform|terintegrasi|andal|handal|guna|demi|adapun|dalam rangka|memiliki|menggunakan|melalui|dapat (?=(?:me|di|ber|ter)\w)|memantau|mengimplementasikan|efektif dan efisien|sehingga memastikan)\b',
 'inflated_en': r'\b(leverag\w*|robust|seamless|end-to-end|scalable|streamlin\w*|cutting-edge|synergy|empower\w*|utiliz\w*|pivotal|crucial|comprehensive|significant)\b',
 'em_dash': r'—',
 'not_only': r'tidak hanya|bukan hanya|not just|not only',
 'tail_clause': r', (ensuring|highlighting|sehingga memastikan)\b',
 'generic_opener': r'di era digital|in today\'s|overall,',
}
WEAK = {  # not banned, but count and watch density
 'sistem': r'\bsistem\b', 'platform': r'\bplatform\b', 'untuk': r'\buntuk\b',
 'dengan': r'\bdengan\b', 'yang': r'\byang\b', 'colon': r':', 'list3': r'[^,.;:]+, [^,.;:]+, (?:dan|and) [^,.;:]+',
}

def strings(path):
    if path.endswith('.json'):
        out = []
        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    walk(v) if not isinstance(v, str) else out.append(v)
            elif isinstance(x, list):
                for v in x: walk(v)
            elif isinstance(x, str): out.append(x)
        walk(json.load(open(path)))
        return [s for s in out if len(s) > 3]
    t = open(path).read()
    lit = []
    if path.endswith('.html'):  # built pages keep their copy as JSON string literals inside <script>
        for sc in re.findall(r'<script[^>]*>([\s\S]*?)</script>', t):
            lit += [json.loads('"' + m + '"') for m in re.findall(r'"((?:[^"\\\n]|\\.){14,})"', sc) if ' ' in m and not m.startswith(('http', '/', '.'))] if True else []
    t = re.sub(r'<(script|style)[\s\S]*?</\1>', ' ', t)
    t = html.unescape(re.sub(r'<[^>]+>', '\n', t))
    return [l.strip() for l in t.split('\n') if len(l.strip()) > 3] + lit

def scan(paths):
    rep = {'files': {}, 'total_strings': 0, 'banned': {}, 'weak': {}, 'hits': {}, 'sentence': {}}
    allv = []
    for p in paths:
        s = strings(p); allv += s
        rep['files'][p] = len(s)
    rep['total_strings'] = len(allv)
    bc = collections.Counter(); wc = collections.Counter(); hits = collections.defaultdict(list)
    for v in allv:
        for grp, pat in BANNED.items():
            for m in re.finditer(pat, v, re.I):
                bc[m.group(0).lower()] += 1
                if len(hits[m.group(0).lower()]) < 3: hits[m.group(0).lower()].append(v[:140])
        for k, pat in WEAK.items(): wc[k] += len(re.findall(pat, v, re.I))
    sl = [len(x.split()) for v in allv for x in re.split(r'(?<=[.!?]) ', v) if len(x) > 10]
    rep['banned'] = dict(bc.most_common()); rep['weak'] = dict(wc.most_common())
    rep['hits'] = hits
    rep['banned_total'] = sum(bc.values())
    rep['banned_per_100_strings'] = round(100 * sum(bc.values()) / max(1, len(allv)), 2)
    if sl: rep['sentence'] = {'n': len(sl), 'avg_words': round(statistics.mean(sl), 1), 'stdev': round(statistics.pstdev(sl), 1), 'over_30_words': sum(1 for x in sl if x > 30)}
    return rep

TOK = re.compile(r'\b\d[\d.,%]*\b|\b[A-Z][A-Za-z0-9]*(?:\.[a-z]+|[A-Z][a-z]+)\b|\b[A-Z]{2,}[a-z0-9]*\b')
def facts(path):
    d = json.load(open(path)); bad = []; n = 0
    def walk(x, trail=''):
        nonlocal n
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(v, str) and len(k) > 8:
                    n += 1
                    a, b = set(TOK.findall(k)), set(TOK.findall(v))
                    miss = {t for t in a - b if not (t.rstrip('.,') in b)}
                    if miss: bad.append({'missing_in_rewrite': sorted(miss), 'original': k[:160], 'rewrite': v[:160]})
                else: walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(d)
    return {'pairs_checked': n, 'pairs_with_missing_tokens': len(bad), 'details': bad}

def main(a):
    if len(a) < 2: print(__doc__); return
    cmd = a[0]; out = None
    if '--out' in a: i = a.index('--out'); out = a[i+1]; a = a[:i] + a[i+2:]
    if cmd == 'scan': r = scan(a[1:])
    elif cmd == 'facts': r = facts(a[1])
    elif cmd == 'diff':
        o, n = json.load(open(a[1])), json.load(open(a[2]))
        keys = set(o['banned']) | set(n['banned'])
        r = {'banned_total': [o['banned_total'], n['banned_total']],
             'per_100': [o['banned_per_100_strings'], n['banned_per_100_strings']],
             'changes': {k: [o['banned'].get(k, 0), n['banned'].get(k, 0)] for k in sorted(keys) if o['banned'].get(k, 0) != n['banned'].get(k, 0)},
             'weak_before_after': {k: [o['weak'].get(k, 0), n['weak'].get(k, 0)] for k in n['weak']}}
    else: print(__doc__); return
    s = json.dumps(r, ensure_ascii=False, indent=2)
    if out: open(out, 'w').write(s); print('written', out)
    print(s if not out else json.dumps({k: v for k, v in r.items() if k not in ('hits', 'details')}, ensure_ascii=False, indent=2))
main(sys.argv[1:])
