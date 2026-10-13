#!/usr/bin/env python3
"""Checks the built site: SEO limits, conduct wording, links, structured data. Exit code 1 on failure."""
import json, pathlib, re, sys
from html.parser import HTMLParser
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://ieqlaw.com"
FORBID = r"\b(best|top[- ]rated|leading|premier|number one|no\.? ?1|expert|specialist|specialis[ea]|we guarantee|guaranteed (result|outcome|success)|win rate|success rate|unmatched|renowned|famous|formidable|foremost|testimonial|clients say|book (a )?consultation|free consultation|complimentary|contact us today|hire us)\b"
ENROL = r"\b(UP|U\.P\.|D|DL|MH)\s*/\s*\d{1,5}\s*/\s*\d{4}\b|enrol+ment (no|number)|bar council (no|number)|roll (no|number)"
fails = []
def fail(m): fails.append(m)
class P(HTMLParser):
    VOID = {"meta","link","img","br","hr","input","source","path","circle"}
    def __init__(s): super().__init__(); s.stack=[]; s.ids=set(); s.links=[]; s.bad=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if "id" in a: s.ids.add(a["id"])
        if t=="a" and a.get("href"): s.links.append(a["href"])
        if t in ("link","script","img") :
            for k in ("href","src"):
                if a.get(k): s.links.append(a[k])
        if t not in s.VOID: s.stack.append(t)
    def handle_startendtag(s,t,a): pass
    def handle_endtag(s,t):
        if t in s.VOID: return
        if not s.stack or s.stack[-1]!=t: s.bad.append(t)
        else: s.stack.pop()
pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "tools" not in p.relative_to(ROOT).parts)
canon = {}
for f in pages:
    rel = f.relative_to(ROOT).as_posix(); s = f.read_text(encoding="utf-8")
    t = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    d = re.search(r'name="description" content="(.*?)"', s).group(1)
    if len(t) > 62: fail(f"{rel}: title {len(t)} chars")
    if len(d) > 160: fail(f"{rel}: description {len(d)} chars")
    c = re.search(r'rel="canonical" href="(.*?)"', s).group(1)
    canon[rel] = c
    exp = BASE + "/" + ("" if rel == "index.html" else rel)
    if c != exp: fail(f"{rel}: canonical {c} != {exp}")
    if len(re.findall(r"<h1[ >]", s)) != 1: fail(f"{rel}: h1 count")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(m.group(1))
        except Exception as e: fail(f"{rel}: bad JSON-LD {e}")
    vis = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", vis)
    for m in re.finditer(FORBID, txt, re.I): fail(f"{rel}: forbidden wording '{m.group(0)}'")
    for m in re.finditer(ENROL, s, re.I): fail(f"{rel}: enrolment-number pattern '{m.group(0)}'")
    p = P(); p.feed(s)
    if p.bad or p.stack: fail(f"{rel}: unbalanced tags {p.bad[:3]} {p.stack[:3]}")
    for h in p.links:
        if re.match(r"(https?:|mailto:|tel:|#|data:)", h): continue
        h = h.split("#")[0].split("?")[0]
        if rel == "404.html" and h.startswith("/"): tgt = ROOT / h.lstrip("/")
        else: tgt = (f.parent / h).resolve()
        if h in ("", "/") : tgt = ROOT / "index.html"
        if tgt.is_dir(): tgt = tgt / "index.html"
        if not tgt.exists(): fail(f"{rel}: broken link {h}")
# sitemap
sm = (ROOT/"sitemap.xml").read_text()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
for rel, c in canon.items():
    noidx = 'content="noindex' in (ROOT/rel).read_text()
    if noidx and c in locs: fail(f"{rel}: noindex page in sitemap")
    if not noidx and c not in locs: fail(f"{rel}: missing from sitemap")
for l in locs:
    if l not in canon.values(): fail(f"sitemap URL without page: {l}")
# map.html must reach every area page and every scenario page (it is generated, so this catches a broken build or config)
mp = ROOT / "map.html"
if mp.exists():
    ms = mp.read_text(encoding="utf-8")
    for d in ("practice", "library"):
        for f in sorted((ROOT / d).glob("*.html")):
            if f"{d}/{f.name}" not in ms: fail(f"map.html does not link to {d}/{f.name}")
# whole-repo enrolment/secret scan
for f in ROOT.rglob("*"):
    if f.is_file() and ".git" not in f.parts and f.suffix in (".html",".js",".css",".md",".txt",".xml",".py",".svg"):
        s = f.read_text(errors="ignore")
        if re.search(ENROL, s, re.I) and f.name != "lint.py": fail(f"{f.relative_to(ROOT)}: enrolment pattern")
        if f.name != "lint.py" and re.search(r"ghp_[A-Za-z0-9]{20,}|github_pat_", s): fail(f"{f.name}: token-like string")
print(f"{len(pages)} pages checked, {len(locs)} sitemap URLs")
print("FAIL\n" + "\n".join(fails) if fails else "OK")
sys.exit(1 if fails else 0)
