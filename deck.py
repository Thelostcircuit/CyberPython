#!/usr/bin/env python3
"""CYBER//PYTHON deck: the course runner.

    uv run deck.py                 status board + active job
    uv run deck.py jack-in         run the active job's tests; on pass, unlock the next chapter
    uv run deck.py test <n>        run any chapter's tests (no progress change)
    uv run deck.py replay <n>      re-read a cleared chapter's ending
    uv run deck.py reset           wipe progress

Stdlib only. Tests run with the interpreter that launched the deck; `uv run` makes that the
course venv, which Part III needs for its packages.
"""

from __future__ import annotations

import base64
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEY = b"MONTY//IRIS-VALE"
CHAPTERS_FILE = ROOT / "deck_chapters.txt"
PROGRESS_FILE = ROOT / ".deck" / "progress"

# Part III chapters need a third-party package. dir prefix -> importable module name(s).
NEEDS = {
    "33": ["requests"],
    "34": ["bs4"],
    "35": ["numpy"],
    "36": ["pandas"],
    "37": ["matplotlib"],
    "38": ["pydantic"],
    "39": ["sqlalchemy"],
    "40": ["flask"],
    "41": ["fastapi", "httpx2"],
    "42": ["pytest"],
}

RESET, DIM, BOLD = "\x1b[0m", "\x1b[2m", "\x1b[1m"
CYAN, GREEN, YELLOW, MAGENTA, RED = "\x1b[36m", "\x1b[32m", "\x1b[33m", "\x1b[35m", "\x1b[31m"
if not sys.stdout.isatty():
    RESET = DIM = BOLD = CYAN = GREEN = YELLOW = MAGENTA = RED = ""


def chapters() -> list[tuple[str, str]]:
    """(folder, encrypted ending) pairs, in order."""
    out = []
    for line in CHAPTERS_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            folder, enc = line.split("|", 1)
            out.append((folder, enc))
    return out


def decrypt(enc: str) -> str:
    data = base64.b64decode(enc)
    return bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(data)).decode("utf-8")


def load_progress() -> int:
    try:
        return int(PROGRESS_FILE.read_text().strip())
    except (OSError, ValueError):
        return 0


def save_progress(n: int) -> None:
    PROGRESS_FILE.parent.mkdir(exist_ok=True)
    PROGRESS_FILE.write_text(str(n))


def nice(folder: str) -> str:
    num, _, rest = folder.partition("_")
    return f"{num} · {rest.replace('_', ' ')}"


def banner() -> None:
    print(f"{CYAN}{BOLD}\n   ▓▓▓ CYBER//PYTHON ▓▓▓  jack-in terminal\n{RESET}")


def part_label(i: int) -> str | None:
    return {0: "PART I — JACK IN (the language)",
            8: "PART II — THE LIBRARY (the standard library)",
            32: "PART III — THE CHEESE SHOP (the top 10 packages)",
            42: "FINALE"}.get(i)


def status() -> None:
    chs = chapters()
    cleared = min(load_progress(), len(chs))
    banner()
    print(f"  progress: {GREEN}{cleared}{RESET}/{len(chs)} jobs cleared")
    for i, (folder, _) in enumerate(chs):
        label = part_label(i)
        if label:
            print(f"\n  {MAGENTA}{label}{RESET}")
        if i < cleared:
            mark, color, word = "[x]", GREEN, "cleared"
        elif i == cleared:
            mark, color, word = "[>]", YELLOW, "ACTIVE"
        else:
            mark, color, word = "[ ]", DIM, "locked"
        print(f"  {color}{mark} {nice(folder):<28}{DIM}{word}{RESET}")
    print()
    if cleared >= len(chs):
        print(f"  {MAGENTA}{BOLD}ALL JOBS CLEARED. The Coil is open.{RESET}")
        print(f"  {DIM}uv run deck.py replay <n> to re-read any ending.{RESET}\n")
        return
    folder = chs[cleared][0]
    print(f"  {BOLD}Active job:{RESET} {CYAN}{nice(folder)}{RESET}")
    print(f"  {DIM}cd {folder} && read README.md, then solve job.py{RESET}")
    print(f"  {DIM}when ready:{RESET} {BOLD}uv run deck.py jack-in{RESET}\n")


def missing_packages(folder: str) -> list[str]:
    need = NEEDS.get(folder[:2], [])
    return [m for m in need if importlib.util.find_spec(m) is None]


def run_tests(folder: str) -> bool:
    missing = missing_packages(folder)
    if missing:
        print(f"  {RED}Missing package(s): {', '.join(missing)}{RESET}")
        print(f"  {DIM}The Cheese Shop is closed to this interpreter. From the course root:{RESET}")
        print(f"      uv sync")
        print(f"      uv run deck.py jack-in\n")
        return False
    print(f"  {DIM}running {folder}/tests ...{RESET}\n")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        cwd=ROOT / folder,
    )
    return result.returncode == 0


def jack_in() -> int:
    chs = chapters()
    cleared = load_progress()
    if cleared >= len(chs):
        print(f"{MAGENTA}Every job is done. Nothing left to jack into.{RESET}")
        return 0
    folder, enc = chs[cleared]
    banner()
    print(f"  {BOLD}JACKING IN:{RESET} {CYAN}{nice(folder)}{RESET}\n")
    if not run_tests(folder):
        print(f"\n  {RED}{BOLD}✗ JOB FAILED.{RESET} BASILISK is still watching. Fix job.py and try again.")
        print(f"  {DIM}(stuck? {folder}/HINTS.md){RESET}\n")
        return 1
    save_progress(cleared + 1)
    print(f"\n  {GREEN}{BOLD}✓ JOB CLEARED.{RESET} decrypting transmission...\n")
    print(f"{MAGENTA}{'─' * 72}{RESET}")
    print(decrypt(enc))
    print(f"{MAGENTA}{'─' * 72}{RESET}\n")
    if cleared + 1 < len(chs):
        print(f"  {BOLD}Next job unlocked:{RESET} {CYAN}{nice(chs[cleared + 1][0])}{RESET}\n")
    return 0


def replay(n: int) -> int:
    chs = chapters()
    if not 1 <= n <= len(chs):
        print(f"No chapter {n}. There are {len(chs)}.")
        return 1
    if n > load_progress():
        print(f"{RED}Chapter {n} is still encrypted. Clear it first.{RESET}")
        return 1
    print(f"\n{MAGENTA}── {nice(chs[n - 1][0])} ──{RESET}\n")
    print(decrypt(chs[n - 1][1]))
    return 0


def test(n: int) -> int:
    chs = chapters()
    if not 1 <= n <= len(chs):
        print(f"No chapter {n}.")
        return 1
    return 0 if run_tests(chs[n - 1][0]) else 1


def main(argv: list[str]) -> int:
    if not argv:
        status()
        return 0
    cmd, *rest = argv
    if cmd == "jack-in":
        return jack_in()
    if cmd in ("replay", "test") and rest and rest[0].isdigit():
        return (replay if cmd == "replay" else test)(int(rest[0]))
    if cmd == "reset":
        if input("Wipe all progress? [y/N] ").strip().lower() == "y":
            save_progress(0)
            print("Progress wiped. The deck is cold.")
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
