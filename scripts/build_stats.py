#!/usr/bin/env python3
"""Generate stats.svg — current-year contribution stats card.

Data comes from GitHub's public contribution calendar HTML fragment
(https://github.com/users/<user>/contributions), the same view visitors
see — no token required, includes anonymized private counts when the
profile setting allows it. Stdlib only.
"""
import argparse
import datetime as dt
import re
import sys
import urllib.request

ACCENT_1, ACCENT_2 = "#00d9ff", "#8b5cf6"


def fetch_calendar(user: str, year: int) -> dict:
    url = f"https://github.com/users/{user}/contributions?from={year}-01-01&to={year}-12-31"
    req = urllib.request.Request(url, headers={"User-Agent": "profile-stats-card"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                html = r.read().decode()
            if 'data-date="' in html:
                break
        except Exception as e:
            if attempt == 3:
                raise
            print(f"fetch attempt {attempt + 1} failed: {e}", file=sys.stderr)
    else:
        raise RuntimeError("calendar fetch returned no day cells")

    id_to_date = dict(re.findall(r'data-date="(\d{4}-\d{2}-\d{2})" id="([\w-]+)"', html))
    id_to_date = {v: k for k, v in id_to_date.items()}
    counts = {}
    for cell_id, text in re.findall(r'<tool-tip [^>]*for="([\w-]+)"[^>]*>([^<]*)</tool-tip>', html):
        date = id_to_date.get(cell_id)
        if not date:
            continue
        m = re.match(r"\s*([\d,]+) contribution", text)
        counts[date] = int(m.group(1).replace(",", "")) if m else 0
    return counts


def compute(counts: dict, year: int, today: dt.date):
    days = sorted(d for d in counts if d.startswith(str(year)) and dt.date.fromisoformat(d) <= today)
    total = sum(counts[d] for d in days)

    longest = current = 0
    run = 0
    for d in days:
        run = run + 1 if counts[d] > 0 else 0
        longest = max(longest, run)

    # current streak: walk back from today (a zero today doesn't break yesterday's streak)
    walk = today
    if counts.get(walk.isoformat(), 0) == 0:
        walk -= dt.timedelta(days=1)
    while walk.year == year and counts.get(walk.isoformat(), 0) > 0:
        current += 1
        walk -= dt.timedelta(days=1)

    # weekly totals for the sparkline (ISO weeks, capped to weeks elapsed)
    weekly = {}
    for d in days:
        week = dt.date.fromisoformat(d).isocalendar()[1]
        weekly[week] = weekly.get(week, 0) + counts[d]
    weeks = [weekly[w] for w in sorted(weekly)]
    return total, current, longest, weeks


def render(total: int, current: int, longest: int, weeks: list, year: int) -> str:
    W, H = 1200, 320
    card_x, card_y, card_w, card_h = 150, 20, 900, 280

    def col(x, number, label, accent=False, delay=0.4):
        fill = "url(#accent)" if accent else "#e6edf3"
        return f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.55s"
      calcMode="spline" keySplines="0.25 1 0.5 1" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" values="0 10;0 0"
      begin="{delay}s" dur="0.55s" calcMode="spline" keySplines="0.25 1 0.5 1" fill="freeze"/>
    <text x="{x}" y="162" text-anchor="middle" fill="{fill}" font-size="46" font-weight="800"
      letter-spacing="-1" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">{number}</text>
    <text x="{x}" y="192" text-anchor="middle" fill="#8b949e" font-size="14"
      font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{label}</text>
  </g>'''

    # sparkline: one slim bar per week, height scaled to the busiest week
    bars = []
    if weeks:
        peak = max(max(weeks), 1)
        bw, gap = 14, 8
        span = len(weeks) * bw + (len(weeks) - 1) * gap
        bx = 600 - span / 2
        base = 262
        for i, w in enumerate(weeks):
            h = max(3, round(38 * w / peak))
            op = 0.3 + 0.7 * (w / peak)
            x = round(bx + i * (bw + gap), 1)
            delay = round(0.9 + i * 0.018, 3)
            bars.append(f'''    <rect x="{x}" y="{base - h}" width="{bw}" height="{h}" rx="2"
      fill="url(#accent)" opacity="0">
      <animate attributeName="opacity" from="0" to="{op:.2f}" begin="{delay}s" dur="0.4s"
        calcMode="spline" keySplines="0.25 1 0.5 1" fill="freeze"/>
    </rect>''')

    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{ACCENT_1}"/>
      <stop offset="100%" stop-color="{ACCENT_2}"/>
    </linearGradient>
    <filter id="shadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
  </defs>
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.7s"
      calcMode="spline" keySplines="0.25 1 0.5 1" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" values="0 14;0 0"
      begin="0.1s" dur="0.7s" calcMode="spline" keySplines="0.25 1 0.5 1" fill="freeze"/>

    <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="16" fill="#0d1117" filter="url(#shadow)"/>
    <rect x="{card_x + 0.5}" y="{card_y + 0.5}" width="{card_w - 1}" height="{card_h - 1}" rx="15.5"
      fill="none" stroke="#30363d" stroke-width="1"/>
    <line x1="{card_x + 16}" y1="{card_y + 1}" x2="{card_x + card_w - 16}" y2="{card_y + 1}"
      stroke="url(#accent)" stroke-width="1.5" opacity="0.55"/>

    <text x="{card_x + 36}" y="68" font-size="18"
      font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
      <tspan fill="#7ee787">❯</tspan> <tspan fill="#e6edf3">stats --year {year}</tspan>
    </text>

{col(320, f"{total:,}", "contributions", accent=True, delay=0.4)}
{col(600, current, "day streak", delay=0.55)}
{col(880, longest, "longest streak", delay=0.7)}

  <g>
{chr(10).join(bars)}
  </g>
  </g>
</svg>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="ponderrr")
    ap.add_argument("--out", default="stats.svg")
    args = ap.parse_args()

    today = dt.datetime.now(dt.timezone.utc).date()
    counts = fetch_calendar(args.user, today.year)
    total, current, longest, weeks = compute(counts, today.year, today)
    print(f"{today.year}: total={total:,} current={current} longest={longest} weeks={len(weeks)}")
    with open(args.out, "w") as f:
        f.write(render(total, current, longest, weeks, today.year))


if __name__ == "__main__":
    main()
