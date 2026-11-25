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
NARRATIVES = {
    "intro": (
        "ABOUT ME", "Building practical applications.",
        "I'm Rafael, an Information Technology student at Florida International University, "
        "based in the Cayman Islands. I work with Python, Java, and web technologies to "
        "build applications around problems I encounter, with a growing focus on backend "
        "development and automation.",
    ),
    "nova": (
        "LOCAL AI & LINUX", "Nova & my home lab",
        "I'm also building Nova, a local AI assistant, and running a home lab with dedicated "
        "machines for AI workloads, development, and Linux practice. It gives me a place to "
        "work with Ollama, SSH, and private networking while learning how to deploy and "
        "troubleshoot applications across machines.",
    ),
    "opportunities": (
        "OPEN TO OPPORTUNITIES", "Opportunities & collaboration",
        "I'm open to software development internships, junior developer roles, and project "
        "collaborations, especially in backend development, automation, and web applications.",
    ),
}


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
    body = text(pad, 42, "WHAT I'M BUILDING", 12, c["accent"], 500, True,
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


def narrative_card(slug, theme, mobile):
    c = PALETTES[theme]
    width, pad = (440, 30) if mobile else (960, 36)
    label, title, description = NARRATIVES[slug]
    body = text(pad, 42, label, 11 if mobile else 12, c["accent"], 500, True,
                'letter-spacing="1.5"')
    title_lines = wrap(title, width=22 if mobile else 43)
    title_height = 40 if mobile else 48
    for index, value in enumerate(title_lines):
        body += text(pad, 98 + index * title_height, value,
                     32 if mobile else 38, c["fg"], 700,
                     extra='letter-spacing="-.7"')
    paragraph_y = 98 + (len(title_lines) - 1) * title_height + (39 if mobile else 43)
    description_lines = wrap(description, width=33 if mobile else 76)
    line_height = 30 if mobile else 32
    body += lines(pad, paragraph_y, description_lines,
                  21 if mobile else 23, line_height, c["muted"])
    last_line = paragraph_y + (len(description_lines) - 1) * line_height
    height = last_line + 36
    if slug == "opportunities":
        button_y, button_width = last_line + 30, 298
        body += (f'<rect x="{pad}" y="{button_y}" width="{button_width}" height="48" '
                 f'rx="9" fill="{c["accent"]}"/>')
        body += text(pad + 18, button_y + 31, "Explore my repositories", 18, c["bg"], 600)
        arrow_x, arrow_y = pad + button_width - 32, button_y + 18
        body += (f'<path d="m{arrow_x} {arrow_y + 12} 12-12m-12 0h12v12" '
                 f'stroke="{c["bg"]}" stroke-width="2" stroke-linecap="round" '
                 'stroke-linejoin="round"/>')
        height = button_y + 48 + 32
        description += " Explore my repositories."
    return shell(width, height, c, title, description, body)


def profile_card(theme, mobile):
    """Keep the identity banner and introduction inside one continuous frame."""
    c = PALETTES[theme]
    width, pad = (440, 30) if mobile else (960, 36)
    body = (f'<rect x="{pad}" y="32" width="30" height="24" rx="5" '
            f'fill="{c["accent"]}" fill-opacity=".12"/>')
    body += text(pad + 15, 49, "RF", 14, c["accent"], 700,
                 extra='text-anchor="middle"')
    body += text(pad + 44, 48, "APPLICATION DEVELOPMENT", 10 if mobile else 12,
                 c["accent"], 500, True,
                 'letter-spacing="1"' if mobile else 'letter-spacing="1.5"')
    body += text(pad, 110, "Olufemi Rafael Fadipe", 34 if mobile else 40,
                 c["fg"], 700, extra='letter-spacing="-1"')
    tagline = ["Application development", "Automation · Local AI"] if mobile else [
        "Application development · Automation · Local AI"]
    body += lines(pad, 150, tagline, 19 if mobile else 20, 29, c["muted"])
    if not mobile:
        body += f'<path d="M{pad} 181h42" stroke="{c["accent"]}" stroke-width="3" stroke-linecap="round"/>'
    body += text(pad, 217, "CAYMAN ISLANDS", 11 if mobile else 12, c["muted"],
                 400, True, 'letter-spacing="1.5"')
    tx, ty, scale = (318, 139, .34) if mobile else (730, 42, .76)
    body += f'''<g transform="translate({tx} {ty}) scale({scale})">
      <rect width="250" height="196" rx="14" fill="{c['panel']}" stroke="{c['line']}" stroke-width="1.5"/>
      <path d="M0 39H250" stroke="{c['line']}" stroke-width="1.5"/>
      <circle cx="20" cy="20" r="3.5" fill="{c['accent']}"/>
      <circle cx="34" cy="20" r="3.5" fill="{c['dim']}" fill-opacity=".55"/>
      <circle cx="48" cy="20" r="3.5" fill="{c['dim']}" fill-opacity=".3"/>
      <path d="m31 69 17 14-17 14M61 98h20" stroke="{c['accent']}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M31 126H132M31 143H184M31 160H107" stroke="{c['dim']}" stroke-opacity=".65" stroke-width="5" stroke-linecap="round"/>
      <path d="m165 83 10 10 21-24" stroke="{c['accent']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>'''
    body += f'<path d="M{pad} 246H{width - pad}" stroke="{c["line"]}"/>'
    body += text(pad, 282, "ABOUT ME", 11 if mobile else 12, c["accent"],
                 500, True, 'letter-spacing="1.5"')
    _, heading, description = NARRATIVES["intro"]
    headings = wrap(heading, width=22 if mobile else 43)
    for index, value in enumerate(headings):
        body += text(pad, 331 + index * 40, value, 32 if mobile else 36,
                     c["fg"], 700, extra='letter-spacing="-.7"')
    paragraph_y = 373 + (len(headings) - 1) * 40
    paragraph_lines = wrap(description, width=33 if mobile else 76)
    line_height = 30 if mobile else 32
    body += lines(pad, paragraph_y, paragraph_lines, 21 if mobile else 23,
                  line_height, c["muted"])
    height = paragraph_y + (len(paragraph_lines) - 1) * line_height + 36
    return shell(width, height, c, "Olufemi Rafael Fadipe — Building practical applications",
                 "Application development, automation and local AI. Cayman Islands. " + description,
                 body)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for theme in PALETTES:
        for mobile in (False, True):
            suffix = f"{theme}{'-mobile' if mobile else ''}.svg"
            (ROOT / "assets" / f"profile-{suffix}").write_text(
                profile_card(theme, mobile), encoding="utf-8")
            for index, project in enumerate(PROJECTS, start=1):
                (DEST / f"{project[0]}-{suffix}").write_text(
                    project_card(project, index, theme, mobile), encoding="utf-8")
            (DEST / f"tools-{suffix}").write_text(tools_card(theme, mobile), encoding="utf-8")
            (DEST / f"jobbot-{suffix}").write_text(jobbot_card(theme, mobile), encoding="utf-8")
            for slug in NARRATIVES:
                if slug == "intro":
                    continue
                (DEST / f"{slug}-{suffix}").write_text(
                    narrative_card(slug, theme, mobile), encoding="utf-8")
    print("Rendered profile banners and section cards.")


if __name__ == "__main__":
    main()
