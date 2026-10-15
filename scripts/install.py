"""Apply these dotfiles to the current machine (Windows, macOS, Linux).

Rebuilds the snippets, then for each editor it finds:
  VS Code   merge settings (your existing keys win), fill in the compiler and
            PHP paths, copy snippets in as guided-<language>.code-snippets.
  Sublime   merge preferences, queue packages for Package Control, re-enable
            Package Control if an interrupted upgrade left it disabled, copy
            snippets into Packages/User.
Every file it changes gets a *.bak-<timestamp> copy first.

Usage:
    python scripts/install.py                # settings + snippets
    python scripts/install.py --extensions   # also install VS Code extensions
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")   # one stamp per run, shared by every backup
sys.path.insert(0, str(ROOT / "snippets"))          # so main() can import build.py


# ---------------------------------------------------------------- JSONC ----
# VS Code and Sublime both allow comments and trailing commas in their settings,
# which json.loads rejects. A small scanner is enough; it skips string contents
# so a "//" inside a URL is left alone.
def strip_jsonc(text: str) -> str:
    """Remove // and /* */ comments (outside strings) and trailing commas."""
    out, i, n = [], 0, len(text)
    in_str = esc = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            i += 1
        elif c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(c)
            i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


# Missing or blank settings files count as empty, which is what a fresh editor install has.
def load_jsonc(path: Path) -> dict:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return {}
    return json.loads(strip_jsonc(path.read_text(encoding="utf-8")))


def merge_user_wins(user: dict, curated: dict) -> dict:
    """Add curated keys the user does not have. Nested objects merge the same way."""
    merged = dict(user)
    for key, value in curated.items():
        if key not in merged:
            merged[key] = value
        elif isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_user_wins(merged[key], value)
    return merged


# Copy next to the original (settings.json.bak-20260101-120000) so undoing is a rename.
def backup(path: Path) -> None:
    if path.exists():
        shutil.copy2(path, path.with_name(f"{path.name}.bak-{STAMP}"))


# -------------------------------------------------------------- paths ----
# Default per-user config folders on each OS.
def vscode_user_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        return Path(os.environ["APPDATA"]) / "Code" / "User"
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Code" / "User"
    return Path.home() / ".config" / "Code" / "User"


def sublime_user_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        return Path(os.environ["APPDATA"]) / "Sublime Text" / "Packages" / "User"
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Sublime Text" / "Packages" / "User"
    return Path.home() / ".config" / "sublime-text" / "Packages" / "User"


# Used for C_Cpp.default.compilerPath, so IntelliSense finds the right headers.
def find_compiler() -> str | None:
    found = shutil.which("g++") or shutil.which("clang++")
    if found:
        return Path(found).as_posix()
    if platform.system() == "Windows":   # winget portable installs may not be on PATH yet
        base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
        for exe in base.glob("*WinLibs*/mingw64/bin/g++.exe"):
            return exe.as_posix()
    return None


# PATH first, then the default XAMPP location on Windows.
def find_php() -> str | None:
    found = shutil.which("php")
    if found:
        return Path(found).as_posix()
    xampp = Path("C:/xampp/php/php.exe")
    return xampp.as_posix() if xampp.exists() else None


# ------------------------------------------------------------- VS Code ----
def install_vscode(with_extensions: bool) -> None:
    user_dir = vscode_user_dir()
    if not user_dir.exists():
        print("VS Code: user directory not found, skipping")
        return
    settings_path = user_dir / "settings.json"
    curated = load_jsonc(ROOT / "vscode" / "settings.json")
    compiler, php = find_compiler(), find_php()
    if compiler:
        curated["C_Cpp.default.compilerPath"] = compiler
    if php:
        curated["php.validate.executablePath"] = php

    backup(settings_path)
    merged = merge_user_wins(load_jsonc(settings_path), curated)
    settings_path.write_text(json.dumps(merged, indent=4) + "\n", encoding="utf-8")
    print(f"VS Code: merged {len(curated)} settings (compiler={compiler}, php={php})")

    # Clear our previous guided-* files first so a snippet file removed here
    # doesn't linger in the editor. The user's own snippet files are untouched.
    snip_dir = user_dir / "snippets"
    snip_dir.mkdir(exist_ok=True)
    for old in snip_dir.glob("guided-*.code-snippets"):
        old.unlink()
    count = 0
    for src in (ROOT / "vscode" / "snippets").glob("*.code-snippets"):
        shutil.copy2(src, snip_dir / f"guided-{src.name}")
        count += 1
    print(f"VS Code: installed {count} snippet files")

    if with_extensions:
        code = shutil.which("code")
        if not code:
            print("VS Code: `code` CLI not on PATH, skipping extensions")
            return
        for line in (ROOT / "vscode" / "extensions.txt").read_text(encoding="utf-8").splitlines():
            ext = line.strip()
            if ext and not ext.startswith("#"):
                ok = subprocess.run([code, "--install-extension", ext], capture_output=True).returncode == 0
                print(f"  {'ok  ' if ok else 'FAIL'} {ext}")


# -------------------------------------------------------- Sublime Text ----
# Writes tab-indented JSON like Sublime does. json.dumps drops comments, so the
# user's commented-out lines are appended at the end of the object instead of lost.
def _write_sublime(path: Path, data: dict, preserved_comments: list[str] | None = None) -> None:
    body = json.dumps(data, indent="\t")
    if preserved_comments:
        block = "\n".join("\t" + c for c in preserved_comments)
        body = body[: body.rfind("}")].rstrip() + "\n\t// ---- kept from your previous file ----\n" + block + "\n}"
    path.write_text(body + "\n", encoding="utf-8")


def install_sublime() -> None:
    user_dir = sublime_user_dir()
    if not user_dir.exists():
        print("Sublime Text: Packages/User not found, skipping")
        return
    src = ROOT / "sublime"

    # Preferences: merge, keep the user's commented-out lines, un-ignore Package Control
    prefs_path = user_dir / "Preferences.sublime-settings"
    old_text = prefs_path.read_text(encoding="utf-8") if prefs_path.exists() else ""
    comments = [ln.strip() for ln in old_text.splitlines() if ln.strip().startswith(("/*", "//"))]
    prefs = merge_user_wins(load_jsonc(prefs_path), load_jsonc(src / "Preferences.sublime-settings"))
    ignored = [p for p in prefs.get("ignored_packages", []) if p != "Package Control"]
    if ignored != prefs.get("ignored_packages", []):
        print("Sublime Text: Package Control was disabled (interrupted upgrade); re-enabled it")
    prefs["ignored_packages"] = ignored
    backup(prefs_path)
    _write_sublime(prefs_path, prefs, comments)

    # Syntax-specific settings (merged the same way)
    for syntax in src.glob("*.sublime-settings"):
        if syntax.name == "Preferences.sublime-settings":
            continue
        target = user_dir / syntax.name
        backup(target)
        _write_sublime(target, merge_user_wins(load_jsonc(target), load_jsonc(syntax)))

    # Package Control: add packages, clear a stuck in-process marker
    pc_path = user_dir / "Package Control.sublime-settings"
    pc = load_jsonc(pc_path)
    wanted = json.loads((src / "packages.json").read_text(encoding="utf-8"))["packages"]
    pc["installed_packages"] = sorted(set(pc.get("installed_packages", [])) | set(wanted), key=str.lower)
    pc["in_process_packages"] = []
    backup(pc_path)
    _write_sublime(pc_path, pc)
    print(f"Sublime Text: {len(wanted)} packages queued (installed on next start)")

    # Snippets: our own folder, replaced whole so removed snippets go away too
    dest = user_dir / "Guided Snippets"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src / "snippets", dest)
    print(f"Sublime Text: installed {sum(1 for _ in dest.rglob('*.sublime-snippet'))} snippets")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install editor dotfiles")
    parser.add_argument("--extensions", action="store_true", help="also install VS Code extensions")
    args = parser.parse_args()

    import build   # snippets/build.py, importable via the sys.path line at the top

    build.build()
    install_vscode(args.extensions)
    install_sublime()
    return 0


if __name__ == "__main__":
    sys.exit(main())
