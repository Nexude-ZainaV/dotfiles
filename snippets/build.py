"""Generate VS Code and Sublime Text snippets from one source of truth.

Why one source: the same guided snippet (an if/else, a fetch call, a
responsive media-query set) should behave identically in both editors, and
maintaining two hand-written copies drifts within a week.

Authoring notation (escape-free, so code reads like code):
    «1:name»   tab stop 1 with default text "name"
    «1»        tab stop 1 again (mirrors what was typed at the first «1»)
    «0»        where the cursor lands when you finish tabbing
Everything else is literal, including $, backslashes and template literals.
Leading groups of 4 spaces become tabs so each editor re-indents to your
own tab settings.

Run from the repo root:
    python snippets/build.py
Output:
    vscode/snippets/<family>.code-snippets
    sublime/snippets/<family>/<prefix>.sublime-snippet
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(__file__).resolve().parent / "src"
VSCODE_OUT = ROOT / "vscode" / "snippets"
SUBLIME_OUT = ROOT / "sublime" / "snippets"

TOKEN = re.compile(r"«(\d+)(?::([^»\n]*))?»")
INDENT = re.compile(r"^((?:    )+)")


def _escape_literal(text: str) -> str:
    """Escape the characters that the TextMate snippet grammar treats as
    syntax. Both editors share that grammar: \\ and $ are escaped with a
    backslash."""
    return text.replace("\\", "\\\\").replace("$", "\\$")


def to_snippet_syntax(body: str) -> str:
    """Convert the «n:default» notation to ${n:default} with literals escaped."""
    out: list[str] = []
    pos = 0
    for m in TOKEN.finditer(body):
        out.append(_escape_literal(body[pos:m.start()]))
        num, default = m.group(1), m.group(2)
        if default is None:
            out.append("${" + num + "}")
        else:
            safe = _escape_literal(default).replace("}", "\\}")
            out.append("${" + num + ":" + safe + "}")
        pos = m.end()
    out.append(_escape_literal(body[pos:]))
    text = "".join(out)
    # 4-space indentation groups -> tabs, so editors apply the user's indent
    lines = [INDENT.sub(lambda g: "\t" * (len(g.group(1)) // 4), ln) for ln in text.split("\n")]
    return "\n".join(lines)


def load_families() -> list:
    families = []
    for path in sorted(SRC.glob("*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        families.append(mod)
    return families


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build() -> int:
    for out in (VSCODE_OUT, SUBLIME_OUT):
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)

    total = 0
    for mod in load_families():
        fam = mod.FAMILY
        vscode: dict = {}
        sub_dir = SUBLIME_OUT / fam["key"]
        sub_dir.mkdir(parents=True, exist_ok=True)
        seen_titles: set[str] = set()
        for entry in mod.SNIPPETS:
            prefix, title, body = entry[0], entry[1], entry[2]
            flags = entry[3] if len(entry) > 3 else {}
            if title in seen_titles:
                raise ValueError(f"{fam['key']}: duplicate title {title!r}")
            seen_titles.add(title)
            body = body.strip("\n")
            converted = to_snippet_syntax(body)
            if "«" in converted or "»" in converted:
                raise ValueError(f"{fam['key']}/{prefix}: unclosed «tab stop» in {title!r}")
            if "]]>" in converted:
                raise ValueError(f"{fam['key']}/{prefix}: body contains ']]>'")

            item = {
                "scope": fam["vscode"],
                "prefix": prefix,
                "body": converted.split("\n"),
                "description": f"{title} (guided)",
            }
            if flags.get("template"):
                item["isFileTemplate"] = True
            vscode[title] = item

            xml = (
                "<snippet>\n"
                f"\t<content><![CDATA[{converted}]]></content>\n"
                f"\t<tabTrigger>{prefix}</tabTrigger>\n"
                f"\t<scope>{fam['sublime']}</scope>\n"
                f"\t<description>{title}</description>\n"
                "</snippet>\n"
            )
            (sub_dir / f"{slug(prefix)}--{slug(title)}.sublime-snippet").write_text(xml, encoding="utf-8")
            total += 1

        (VSCODE_OUT / f"{fam['key']}.code-snippets").write_text(
            json.dumps(vscode, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"  {fam['key']:<8} {len(mod.SNIPPETS):>3} snippets")
    print(f"built {total} snippets")
    return total


if __name__ == "__main__":
    build()
