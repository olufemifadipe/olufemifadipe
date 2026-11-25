"""Render the profile's light/dark SVG cards using only Python's standard library."""

from html import escape
from pathlib import Path
from textwrap import wrap


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "cards"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
PALETTES = {
    "dark": dict(bg="#0D1724", fg="#F0F6FC", muted="#9EACBD", accent="#7EE2C2",
                 line="#253748", panel="#121F2E", dim="#456476"),
    "light": dict(bg="#F2F7F6", fg="#122C35", muted="#506971", accent="#166C5B",
                  line="#D3E3DF", panel="#E8F1EE", dim="#91B3A9"),
}
PROJECTS = [
    ("verdant-clay", "Verdant Clay", "WEB DEVELOPMENT",
     "A jewelry website prototype with collection filters, product detail dialogs, and WhatsApp enquiries.",
     ["HTML", "CSS", "JavaScript"]),
    ("air-quality", "Air Quality Explorer", "API INTEGRATION",
     "A Python application that retrieves IQAir air quality and weather data, processes JSON responses, and generates a Folium map.",
     ["Python", "REST APIs", "Folium"]),
    ("musical-instruments", "Musical Instruments", "SOFTWARE DESIGN",
     "An object-oriented implementation of the Strategy Pattern, separating instruments from interchangeable playing behaviors.",
     ["Python", "OOP", "Design patterns"]),
]
TOOLS = [
    ("Languages", ["Python", "Java", "SQL", "HTML", "CSS", "JavaScript"]),
    ("Data & automation", ["SQLite", "MySQL", "REST APIs", "JSON", "Playwright"]),
    ("Development", ["Git", "GitHub", "Linux", "VS Code", "pytest"]),
]
FEATURES = [
    ("Discover", "Greenhouse and Lever listings from configured employer feeds."),
    ("Compare", "Skill matching with location and eligibility notes for review."),
    ("Track", "SQLite history, application status, and CSV/JSON exports."),
    ("Test", "Automated tests and a local Playwright practice demo."),
]


def text(x, y, value, size, color, weight=400, mono=False, extra=""):
    family = MONO if mono else FONT
    return (f'<text x="{x}" y="{y}" font-family="{escape(family, quote=True)}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>'
            f'{escape(value)}</text>')


def lines(x, y, values, size, line_height, color):
    return "".join(text(x, y + i * line_height, value, size, color)
                   for i, value in enumerate(values))


def width_estimate(value, size):
    """Conservative widths for the card's short pill labels."""
    return sum(0.28 if ch in "ilI. " else 0.85 if ch in "MW@" else 0.6
               for ch in value) * size


def pills(values, x, y, available, palette, size=18):
    parts, px, py = [], x, y
    height, gap = size + 17, 8
    for value in values:
        width = round(width_estimate(value, size) + 26)
        if px > x and px + width > x + available:
            px, py = x, py + height + gap
        parts.append(f'<rect x="{px}" y="{py}" width="{width}" height="{height}" '
                     f'rx="7" fill="{palette["accent"]}" fill-opacity=".085" '
                     f'stroke="{palette["line"]}"/>')
        parts.append(text(px + 13, py + size + 4, value, size, palette["accent"], 500))
        px += width + gap
    return "".join(parts), py + height


def shell(width, height, palette, title, description, contents):
    grid_start = round(width * 0.60)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="{palette['line']}" stroke-width=".7"/></pattern>
    <linearGradient id="fade" x1="{grid_start}" y1="0" x2="{width}" y2="0" gradientUnits="userSpaceOnUse"><stop stop-color="{palette['bg']}"/><stop offset="1" stop-color="{palette['bg']}" stop-opacity=".2"/></linearGradient>
    <clipPath id="clip"><rect width="{width}" height="{height}" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{width}" height="{height}" fill="{palette['bg']}"/>
    <rect x="{grid_start}" width="{width - grid_start}" height="{height}" fill="url(#grid)"/>
    <rect x="{grid_start}" width="{width - grid_start}" height="{height}" fill="url(#fade)"/>
    <rect x="1" y="34" width="3" height="{height - 68}" rx="1.5" fill="{palette['accent']}"/>
    {contents}
    <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="19.5" stroke="{palette['line']}"/>
  </g>
</svg>
'''


def project_card(project, index, theme, mobile):
    slug, title, category, description, tech = project
    c = PALETTES[theme]
    width, pad = (440, 30) if mobile else (960, 36)
    size, line_height = (21, 29) if mobile else (23, 32)
    description_lines = wrap(description, width=33 if mobile else 72)
    body = text(pad, 42, f"0{index} / {category}", 12, c["accent"], 500, True,
                'letter-spacing="1.5"')
    body += text(pad, 94, title, 32 if mobile else 36, c["fg"], 700,
                 extra='letter-spacing="-.7"')
    body += lines(pad, 135, description_lines, size, line_height, c["muted"])
    tags_y = 135 + (len(description_lines) - 1) * line_height + 28
    tags, tags_bottom = pills(tech, pad, tags_y, width - pad * 2, c, 17 if mobile else 18)
    body += tags
    arrow_x = width - pad - 15
    body += f'<path d="m{arrow_x} 45 15-15m-15 0h15v15" stroke="{c["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    if not mobile:
        body += text(arrow_x - 15, 42, "VIEW SOURCE", 11, c["muted"], 500, True,
                     'text-anchor="end" letter-spacing="1.2"')
    return shell(width, tags_bottom + 32, c, title, description + " Open repository.", body)


def tools_card(theme, mobile):
    c = PALETTES[theme]
    width, pad = (440, 30) if mobile else (960, 36)
    body = text(pad, 42, "DEVELOPER TOOLKIT", 12, c["accent"], 500, True,
                'letter-spacing="1.8"')
    y, bottom = 98, 0
    for i, (label, values) in enumerate(TOOLS):
        x = pad if mobile else pad + i * 304
        if i and not mobile:
            body += f'<path d="M{x - 20} 80V254" stroke="{c["line"]}"/>'
        if i and mobile:
            body += f'<path d="M{pad} {y - 31}H{width - pad}" stroke="{c["line"]}"/>'
        body += text(x, y, label, 23 if mobile else 22, c["fg"], 600)
        tags, bottom = pills(values, x, y + 20, width - pad * 2 if mobile else 266,
                             c, 19 if mobile else 18)
        body += tags
        if mobile:
            y = bottom + 71
    height = bottom + 35 if mobile else 288
    desc = ". ".join(label + ": " + ", ".join(values) for label, values in TOOLS) + "."
    return shell(width, height, c, "Tools I work with", desc, body)


def jobbot_card(theme, mobile):
    c = PALETTES[theme]
    width, pad = (440, 30) if mobile else (960, 36)
    body = text(pad, 42, "CURRENT BUILD", 12, c["accent"], 500, True,
                'letter-spacing="1.8"')
    body += text(pad, 98, "Job Application Bot", 32 if mobile else 44, c["fg"], 700,
                 extra='letter-spacing="-.8"')
    subtitle = ["A more manageable job search,", "built in Python."] if mobile else [
        "A more manageable job search, built in Python."]
    body += lines(pad, 139, subtitle, 21 if mobile else 24, 29, c["muted"])
    start_y = 205 if mobile else 184
    feature_width = width - pad * 2 if mobile else 432
    feature_height, feature_gap = (131, 12) if mobile else (130, 16)
    bottom = 0
    for i, (label, description) in enumerate(FEATURES):
        x = pad if mobile else pad + (i % 2) * 456
        y = start_y + (i if mobile else i // 2) * (feature_height + feature_gap)
        body += f'<rect x="{x}" y="{y}" width="{feature_width}" height="{feature_height}" rx="11" fill="{c["panel"]}" stroke="{c["line"]}"/>'
        body += text(x + 20, y + 35, label, 23, c["fg"], 600)
        body += text(x + feature_width - 20, y + 32, f"0{i + 1}", 12, c["accent"],
                     500, True, 'text-anchor="end"')
        desc_lines = wrap(description, width=34 if mobile else 36)
        body += lines(x + 20, y + 69, desc_lines, 19 if mobile else 21, 27, c["muted"])
        bottom = y + feature_height
    separator = bottom + 24
    body += f'<path d="M{pad} {separator}H{width - pad}" stroke="{c["line"]}"/>'
    stack = ["Python · REST APIs · SQLite", "Playwright · pytest"] if mobile else [
        "Python · REST APIs · SQLite · Playwright · pytest"]
    body += lines(pad, separator + 32, stack, 18, 26, c["accent"])
    status_y = separator + 32 + (len(stack) - 1) * 26 + 34
    status = ["Working CLI · Active development", "Private source"] if mobile else [
        "Working CLI · Active development · Private source"]
    body += lines(pad, status_y, status, 15 if mobile else 17, 24, c["muted"])
    desc = ("A Python application for job discovery, skills matching, and application tracking. "
            "Greenhouse and Lever feeds, SQLite storage, CSV and JSON exports, automated tests, "
            "and a local Playwright practice demo. Working CLI; active development; private source.")
    return shell(width, status_y + (len(status) - 1) * 24 + 30, c, "Job Application Bot", desc, body)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for theme in PALETTES:
        for mobile in (False, True):
            suffix = f"{theme}{'-mobile' if mobile else ''}.svg"
            for index, project in enumerate(PROJECTS, start=1):
                (DEST / f"{project[0]}-{suffix}").write_text(
                    project_card(project, index, theme, mobile), encoding="utf-8")
            (DEST / f"tools-{suffix}").write_text(tools_card(theme, mobile), encoding="utf-8")
            (DEST / f"jobbot-{suffix}").write_text(jobbot_card(theme, mobile), encoding="utf-8")
    print(f"Rendered {len(list(DEST.glob('*.svg')))} SVG cards.")


if __name__ == "__main__":
    main()
