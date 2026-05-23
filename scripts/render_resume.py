from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "resume-data.yml"
TEMPLATE_DIR = ROOT / "templates"
BUILD_DIR = ROOT / "build"

LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(value: Any) -> str:
    """Escape user-controlled YAML text before injecting it into LaTeX."""
    if value is None:
        return ""
    text = str(value)
    # Normalize a few typography characters that can be annoying with pdflatex.
    text = (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "--")
        .replace("—", "---")
    )
    return "".join(LATEX_REPLACEMENTS.get(ch, ch) for ch in text)


def url_value(value: Any) -> str:
    """Keep URLs mostly raw for href arguments, while removing accidental spaces."""
    if value is None:
        return ""
    return str(value).strip().replace(" ", "%20")


def display_url(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    text = re.sub(r"^https?://", "", text)
    return text.rstrip("/")


def main() -> None:
    BUILD_DIR.mkdir(exist_ok=True)

    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    data.setdefault("last_updated", datetime.now(timezone.utc).strftime("%B %Y"))

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        comment_start_string="((*#",
        comment_end_string="#*))",
    )
    env.filters["latex"] = latex_escape
    env.filters["url"] = url_value
    env.filters["display_url"] = display_url

    for variant in ["design", "ats"]:
        template = env.get_template(f"resume-{variant}.tex.j2")
        output = template.render(**data)
        (BUILD_DIR / f"resume-{variant}.tex").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
