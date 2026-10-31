"""Block 1 정답 — 노이즈 vs 추세

현재 폴더의 day5_sensor_50_synthetic.csv 를 읽어
1) 설비별 평균 ± 2표준편차로 진동 이상 후보를 찾고
2) 진동이 세 번 연속 오르기 시작한 시각을 "추세 시작"으로 잡아
3) 그래프 한 장 대시보드 index.html 과 expected.json 을 현재 폴더에 쓴다.
"""
import csv
import json
import statistics as st
from pathlib import Path

CSV = "day5_sensor_50_synthetic.csv"
COL = "진동(mm/s)"

rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))


def series(prefix):
    r = [x for x in rows if x["설비"].startswith(prefix)]
    return r[0]["설비"], [x["시간"][-5:] for x in r], [float(x[COL]) for x in r]


def outliers(times, vals):
    # 원본 덱 19장: 평상 범위 = 평균 ± 2표준편차, 설비별로 따로
    m, s = st.mean(vals), st.pstdev(vals)
    lo, hi = m - 2 * s, m + 2 * s
    return lo, hi, [(times[i], vals[i]) for i, v in enumerate(vals) if v < lo or v > hi]


def trend_start(times, vals):
    # 이 실습판의 규칙(가정): 세 번 연속 오르기 시작한 시각
    for i in range(len(vals) - 3):
        if vals[i] < vals[i + 1] < vals[i + 2] < vals[i + 3]:
            return times[i]
    return None


nameA, tA, vA = series("설비A")
nameB, tB, vB = series("설비B")
loA, hiA, oA = outliers(tA, vA)
loB, hiB, oB = outliers(tB, vB)
start = trend_start(tB, vB)

fmt = lambda pts: " · ".join(f"{t} {v}" for t, v in pts)
a_out, b_out = fmt(oA), fmt(oB)

# ---- 그래프 (외부 라이브러리 없이 SVG) ----
W, H, L, R, T, B = 760, 360, 48, 16, 20, 40
ymax = 4.0
x = lambda i: L + i * (W - L - R) / (len(tA) - 1)
y = lambda v: T + (ymax - v) * (H - T - B) / ymax
line = lambda vals: " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
si = tB.index(start)

svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="설비A·B 진동 추이">']
for g in range(0, 5):
    svg.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" class="grid"/>'
               f'<text x="{L-8}" y="{y(g)+4:.1f}" class="ax" text-anchor="end">{g}</text>')
for i, t in enumerate(tA):
    if i % 3 == 0:
        svg.append(f'<text x="{x(i):.1f}" y="{H-B+18}" class="ax" text-anchor="middle">{t}</text>')
svg.append(f'<line x1="{L}" x2="{W-R}" y1="{y(hiA):.1f}" y2="{y(hiA):.1f}" class="lim a"/>')
svg.append(f'<line x1="{L}" x2="{W-R}" y1="{y(hiB):.1f}" y2="{y(hiB):.1f}" class="lim b"/>')
svg.append(f'<line x1="{x(si):.1f}" x2="{x(si):.1f}" y1="{T}" y2="{H-B}" class="start"/>'
           f'<text x="{x(si)+6:.1f}" y="{T+14}" class="lab">추세 시작 {start}</text>')
svg.append(f'<polyline points="{line(vA)}" class="s a"/><polyline points="{line(vB)}" class="s b"/>')
for t, v in oA + oB:
    i = tA.index(t)
    svg.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="5" class="pt"/>')
svg.append("</svg>")

html = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>노이즈 vs 추세</title>
<style>
:root{{--bg:#fff;--fg:#1d1d1f;--mut:#6b6b70;--grid:#e6e6ea;--a:#2f6fd6;--b:#d9822b;--pt:#c62828}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151517;--fg:#ececf0;--mut:#9a9aa2;--grid:#2c2c31;--a:#6ea0ff;--b:#f0a35a;--pt:#ff6b6b}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,"Malgun Gothic",sans-serif}}
main{{max-width:820px;margin:0 auto;padding:20px 16px}}
h1{{font-size:20px;margin:0 0 4px}} .sum{{margin:0 0 14px}} .mut{{color:var(--mut);font-size:13px}}
svg{{width:100%;height:auto;display:block}}
.grid{{stroke:var(--grid)}} .ax{{fill:var(--mut);font-size:11px}} .lab{{fill:var(--fg);font-size:12px;font-weight:600}}
.s{{fill:none;stroke-width:2}} .s.a{{stroke:var(--a)}} .s.b{{stroke:var(--b)}}
.lim{{stroke-dasharray:4 4;stroke-width:1}} .lim.a{{stroke:var(--a)}} .lim.b{{stroke:var(--b)}}
.start{{stroke:var(--fg);stroke-dasharray:2 3}} .pt{{fill:var(--pt)}}
.key{{display:flex;flex-wrap:wrap;gap:12px;font-size:13px;margin:8px 0 14px}}
.key i{{display:inline-block;width:14px;height:3px;vertical-align:middle;margin-right:4px}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{border-bottom:1px solid var(--grid);padding:6px 4px;text-align:left}}
</style></head><body><main>
<h1>노이즈인가, 추세인가</h1>
<p class="sum">설비B 진동이 <b>{start}</b>부터 꾸준히 오른다 — 계획 정비 대상은 설비B.</p>
{''.join(svg)}
<div class="key"><span><i style="background:var(--a)"></i>설비A 진동</span><span><i style="background:var(--b)"></i>설비B 진동</span>
<span>점선 = 설비별 평균 + 2σ</span><span><i style="background:var(--pt);height:8px;width:8px;border-radius:50%"></i>이상 후보</span></div>
<table><tr><th>설비</th><th>이상 후보 (평균 ± 2σ 밖)</th><th>판정</th></tr>
<tr><td>{nameA}</td><td>{a_out}</td><td>노이즈형 — 한 번 튀고 정상</td></tr>
<tr><td>{nameB}</td><td>{b_out}</td><td>추세형 — {start}부터 상승</td></tr></table>
<p class="mut">추세 시작 = 진동이 세 번 연속 오르기 시작한 시각(이 실습판의 가정).<br>
데이터: <b>가상 데이터</b> · keerhee/kma-auto-genai-3-1 <code>data/Day5/Day5_설비센서_50건_가상.csv</code> · 기준: Day5 본 강의 14·19·20·27장</p>
</main></body></html>
"""
Path("index.html").write_text(html, encoding="utf-8")

values = {
    "a_outlier": {"value": a_out, "decimals": None, "block": 1},
    "b_outliers": {"value": b_out, "decimals": None, "block": 1},
    "trend_start": {"value": start, "decimals": None, "block": 1},
}
Path("expected.json").write_text(json.dumps({"values": values}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"설비A 이상 후보: {a_out}\n설비B 이상 후보: {b_out}\n추세 시작: {start}")
