#!/usr/bin/env python3
"""扫描本目录成品页，生成 index.html（每日动态）、月度日历页、三个归档页、site.css、manifest.json。"""
import re, os, json, datetime, glob, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
STYLE = open(os.path.join(BASE, "_site_style.txt"), encoding="utf-8").read()
VER = hashlib.md5(STYLE.encode()).hexdigest()[:6]
SERIES = [
    ("brief", "要闻观点摘编", "news-brief"),
    ("research", "智库与国际组织研究动态", "research-dynamics"),
    ("policy", "国内外政策动态", "policy-watch"),
    ("academic", "学术研究前沿", "academic-frontier"),
]
TAG = {"academic": '<span class="tag">周更</span>'}
WEEK = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
WK = ["一", "二", "三", "四", "五", "六", "日"]


def extract(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    m = re.search(r'<div class="date">([^<]+)</div>', s) or re.search(r"<title>([^<]+)</title>", s)
    ds = m.group(1).strip() if m else ""
    mm = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", ds)
    iso = f"{int(mm.group(1)):04d}-{int(mm.group(2)):02d}-{int(mm.group(3)):02d}" if mm else ""
    fc = re.search(r"<footer>(.*?)</footer>", s)
    foot = re.sub(r"<[^>]+>", "", fc.group(1)).strip() if fc else ""
    return iso, ds, foot


def collect():
    out = []
    for key, name, prefix in SERIES:
        for f in sorted(glob.glob(os.path.join(BASE, f"{prefix}-*.html"))):
            iso, ds, foot = extract(f)
            if iso:
                out.append(dict(series=key, name=name, file=os.path.basename(f), iso=iso, date=ds, footer=foot))
    out.sort(key=lambda x: (x["iso"], x["series"]), reverse=True)
    return out


def mmdd(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.month}-{d.day}"


def months_of(own):
    out = []
    for x in own:
        k = (int(x["iso"][:4]), int(x["iso"][5:7]))
        if k not in out:
            out.append(k)
    return out


def cal_html(own, y, m):
    first = datetime.date(y, m, 1)
    days = (datetime.date(y + (m == 12), (m % 12) + 1, 1) - first).days
    have = {x["iso"]: x["file"] for x in own}
    cells = ['<div class="wk">' + w + '</div>' for w in WK]
    for _ in range(first.weekday()):
        cells.append('<div class="d"></div>')
    today = datetime.date.today().isoformat()
    for day in range(1, days + 1):
        iso = f"{y:04d}-{m:02d}-{day:02d}"
        if iso in have:
            cls = "d on today" if iso == today else "d on"
            cells.append(f'<a class="{cls}" href="{have[iso]}">{day}</a>')
        elif iso == today:
            cells.append(f'<div class="d today">{day}</div>')
        else:
            cells.append(f'<div class="d">{day}</div>')
    return f'<div class="cal">{"".join(cells)}</div>'


def page(title, body, series=None):
    attr = f' data-series="{series}"' if series else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#efece6">
<title>{title}</title>
<link rel="stylesheet" href="site.css?v={VER}">
</head>
<body{attr}><main>{body}</main></body></html>"""


def build_home(items):
    parts = ["<h1>研究动态</h1>"]
    for key, name, _ in SERIES:
        own = [x for x in items if x["series"] == key]
        ms = months_of(own)
        btns, panels = [], []
        for i, (y, m) in enumerate(ms):
            act = " on" if i == 0 else ""
            btns.append(f'<button class="btn{act}" data-series="{key}" data-month="{y}-{m:02d}">{y} 年 {m} 月</button>')
            style = "" if i == 0 else ' style="display:none"'
            panels.append(f'<div class="panel" data-series="{key}" data-month="{y}-{m:02d}"{style}>{cal_html(own, y, m)}</div>')
        if btns:
            head = f'<h2>{name}{TAG.get(key, "")}</h2><a class="arch" href="archive-{key}.html">归档</a>'
            parts.append(f'<div class="grp" data-series="{key}"><div class="head">\n{head}\n</div><div class="btns">{"".join(btns)}</div>{"".join(panels)}</div>')
        else:
            parts.append(f'<div class="grp" data-series="{key}"><div class="head">\n<h2>{name}{TAG.get(key, "")}</h2>\n</div></div>')
    parts.append("""<script>
document.querySelectorAll('.btn').forEach(function(b){
  b.addEventListener('click',function(){
    var s=b.dataset.series, m=b.dataset.month;
    document.querySelectorAll('.btn[data-series="'+s+'"]').forEach(function(x){x.classList.remove('on');});
    b.classList.add('on');
    document.querySelectorAll('.panel[data-series="'+s+'"]').forEach(function(x){
      x.style.display = (x.dataset.month===m) ? 'block' : 'none';
    });
  });
});
</script>""")
    return page("研究动态", "".join(parts))

def build_month(name, own, y, m):
    body = (f'<p class="back"><a href="index.html">首页</a></p><h1>{name}</h1>'
            f'<h2 class="yr">{y} 年 {m} 月</h2>' + cal_html(own, y, m))
    return page(f"{name} {y} 年 {m} 月", body)


def build_archive(key, name, own):
    body = [f'<p class="back"><a href="index.html">首页</a></p><h1>{name}</h1>']
    for y in sorted({x["iso"][:4] for x in own}, reverse=True):
        body.append(f'<h2 class="yr">{y}</h2>')
        for mo in sorted({x["iso"][5:7] for x in own if x["iso"][:4] == y}, reverse=True):
            grp = [x for x in own if x["iso"][:4] == y and x["iso"][5:7] == mo]
            body.append(f'<h3 class="mo">{int(mo)} 月</h3><ul>')
            for it in grp:
                w = WEEK[datetime.date.fromisoformat(it["iso"]).weekday()]
                body.append(f'<li><a href="{it["file"]}"><span>{mmdd(it["iso"])} {w}</span></a></li>')
            body.append("</ul>")
    return page(name, "".join(body), key)


if __name__ == "__main__":
    items = collect()
    open(os.path.join(BASE, "site.css"), "w", encoding="utf-8").write(STYLE)
    json.dump(items, open(os.path.join(BASE, "manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(build_home(items))
    for key, name, _ in SERIES:
        own = [x for x in items if x["series"] == key]
        open(os.path.join(BASE, f"archive-{key}.html"), "w", encoding="utf-8").write(
            build_archive(key, name, own))
    print("issues:", len(items))
