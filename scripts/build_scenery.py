#!/usr/bin/env python3
"""Generate scenery.svg — a night landscape painted from contribution data.

The far mountain ridgeline IS the year's weekly contribution totals:
more commits, taller peaks. Aurora, stars, mist, and a shooting star
complete the scene. Stdlib only; data via build_stats.fetch_calendar.
"""
import argparse
import datetime as dt

from build_stats import fetch_calendar, compute

W, H = 1200, 420
CX, CY, CW, CH = 150, 20, 900, 380  # card frame
BOTTOM = CY + CH


def lcg(seed):
    state = seed & 0x7FFFFFFF or 1

    def rand():
        nonlocal state
        state = (state * 48271) % 0x7FFFFFFF
        return state / 0x7FFFFFFF

    return rand


def catmull_path(pts):
    """Smooth open path through pts as cubic beziers (Catmull-Rom)."""
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f} "
    return d


def ridge(values, base_y, amp, min_h=14, overhang=90):
    """Closed mountain path across the card from a list of magnitudes."""
    peak = max(max(values), 1)
    x0, x1 = CX - overhang, CX + CW + overhang
    n = len(values)
    pts = []
    for i, v in enumerate(values):
        x = x0 + (x1 - x0) * i / (n - 1)
        pts.append((x, base_y - min_h - amp * (v / peak)))
    return catmull_path(pts) + f"L {x1:.1f} {BOTTOM} L {x0:.1f} {BOTTOM} Z"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="ponderrr")
    ap.add_argument("--out", default="scenery.svg")
    args = ap.parse_args()

    today = dt.datetime.now(dt.timezone.utc).date()
    year = today.year
    counts = fetch_calendar(args.user, year)
    total, _, _, weeks = compute(counts, year, today)
    print(f"scenery {year}: {total:,} contributions across {len(weeks)} weeks")

    far = ridge(weeks, base_y=305, amp=130)
    mid = ridge(list(reversed(weeks)), base_y=345, amp=80)
    near_wave = [20, 44, 28, 52, 30, 46, 22]
    near = ridge(near_wave, base_y=400, amp=28, min_h=4)

    rand = lcg(year * 100000 + total)
    stars = []
    for _ in range(42):
        x = CX + 14 + rand() * (CW - 28)
        y = CY + 12 + rand() * (CH * 0.5)
        r = 0.7 + rand() * 1.0
        op = 0.25 + rand() * 0.5
        dur = 2.6 + rand() * 3.4
        begin = rand() * 4
        stars.append(
            f'''    <circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#e6edf3" opacity="{op:.2f}">
      <animate attributeName="opacity" values="{op:.2f};{op * 0.25:.2f};{op:.2f}" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>
    </circle>'''
        )

    def curtain(top, sway, phase):
        """Undulating multi-lobe ribbon across the sky."""
        x0, x1 = CX - 80, CX + CW + 80
        step = (x1 - x0) / 6
        pts = [(x0 + i * step, top + sway * ((-1) ** (i + phase)) * (0.4 + 0.13 * i)) for i in range(7)]
        return catmull_path(pts)

    aurora_bands = []
    for i, (top, sway, width, opac, dur) in enumerate(
        [(105, 34, 36, 0.17, 16), (140, 46, 50, 0.12, 21), (80, 26, 26, 0.09, 26)]
    ):
        a, b, c = curtain(top, sway, 0), curtain(top - sway * 0.4, sway * 1.3, 1), curtain(top + sway * 0.3, sway * 0.8, 0)
        aurora_bands.append(
            f'''    <path fill="none" stroke="url(#accent)" stroke-width="{width}" stroke-linecap="round"
      opacity="{opac}" filter="url(#soft)">
      <animate attributeName="d" dur="{dur}s" repeatCount="indefinite"
        calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1" keyTimes="0;0.33;0.66;1"
        values="{a};{b};{c};{a}"/>
    </path>'''
        )

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d9ff"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
      <animate attributeName="x1" dur="14s" values="0%;22%;0%" repeatCount="indefinite"/>
      <animate attributeName="x2" dur="14s" values="100%;78%;100%" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0a0f1f"/>
      <stop offset="55%" stop-color="#0d1220"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <linearGradient id="mist" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#8b949e" stop-opacity="0"/>
      <stop offset="100%" stop-color="#8b949e" stop-opacity="0.10"/>
    </linearGradient>
    <filter id="soft" filterUnits="userSpaceOnUse" x="{CX - 140}" y="0" width="{CW + 280}" height="320">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
    <filter id="shadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
    <clipPath id="frame"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="16"/></clipPath>
  </defs>

  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.9s"
      calcMode="spline" keySplines="0.25 1 0.5 1" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" values="0 14;0 0"
      begin="0.1s" dur="0.9s" calcMode="spline" keySplines="0.25 1 0.5 1" fill="freeze"/>

    <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="16" fill="url(#sky)" filter="url(#shadow)"/>

    <g clip-path="url(#frame)">
      <!-- stars -->
{chr(10).join(stars)}

      <!-- aurora -->
{chr(10).join(aurora_bands)}

      <!-- shooting star: brief streak every 16s -->
      <g opacity="0">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
          values="0;0;1;0;0" keyTimes="0;0.71;0.745;0.78;1"/>
        <line x1="0" y1="0" x2="46" y2="14" stroke="#e6edf3" stroke-width="1.6" stroke-linecap="round">
          <animateTransform attributeName="transform" type="translate" dur="16s" repeatCount="indefinite"
            values="880 60; 880 60; 640 140; 640 140" keyTimes="0;0.71;0.78;1"/>
        </line>
      </g>

      <!-- mountains: far ridge is the real contribution histogram -->
      <g>
        <path d="{far}" fill="#1b2230"/>
        <path d="{catmull_path([(CX - 90 + (CW + 180) * i / (len(weeks) - 1), 305 - 14 - 130 * (w / max(max(weeks), 1))) for i, w in enumerate(weeks)])}"
          fill="none" stroke="url(#accent)" stroke-width="1.5" opacity="0.35"/>
      </g>
      <path d="{mid}" fill="#131a26">
        <animateTransform attributeName="transform" type="translate" dur="26s" repeatCount="indefinite"
          calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" keyTimes="0;0.5;1" values="0 0;-9 0;0 0"/>
      </path>
      <rect x="{CX - 40}" y="250" width="{CW + 80}" height="90" fill="url(#mist)">
        <animateTransform attributeName="transform" type="translate" dur="30s" repeatCount="indefinite"
          calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" keyTimes="0;0.5;1" values="-18 0;18 0;-18 0"/>
      </rect>
      <path d="{near}" fill="#0a0e14">
        <animateTransform attributeName="transform" type="translate" dur="20s" repeatCount="indefinite"
          calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" keyTimes="0;0.5;1" values="0 0;12 0;0 0"/>
      </path>

      <!-- caption -->
      <text x="{CX + 30}" y="{BOTTOM - 22}" font-size="13"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
        <tspan fill="#7ee787">❯</tspan> <tspan fill="#8b949e">render --terrain contributions@{year}</tspan>
        <tspan fill="#6e7681"> · {total:,} peaks</tspan>
      </text>
    </g>

    <rect x="{CX + 0.5}" y="{CY + 0.5}" width="{CW - 1}" height="{CH - 1}" rx="15.5"
      fill="none" stroke="#30363d" stroke-width="1"/>
    <line x1="{CX + 16}" y1="{CY + 1}" x2="{CX + CW - 16}" y2="{CY + 1}"
      stroke="url(#accent)" stroke-width="1.5" opacity="0.55"/>
  </g>
</svg>
'''
    with open(args.out, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
