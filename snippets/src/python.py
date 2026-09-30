"""Python (3.10+) snippets: control flow incl. match, typed functions, classes,
dataclasses, comprehensions, timing, asyncio, HTTP, FastAPI, pytest, logging."""

FAMILY = dict(key="python", vscode="python", sublime="source.python")

SNIPPETS = [
    ("imp", "Import block (PEP 8 order)", r"""
# PEP 8 import order, one blank line between groups (ruff/isort enforce this):
# 1. standard library
import json
import logging
from pathlib import Path

# 2. third-party packages
import «1:requests»

# 3. local application modules
from «2:app».«3:services» import «4:thing»
«0»
"""),
    ("script", "Python script file", r'''
"""«1:tool_name»: «2:one line on what this script does».

Usage:
    python «1».py «3:input.csv»
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", type=Path, help="«4:file to process»")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    «0»
    return 0


# Only runs when executed directly, not when imported by tests or other modules
if __name__ == "__main__":
    sys.exit(main())
''', {"template": True}),
    ("main", "main guard", r"""
def main() -> None:
    «0»


# True only when this file is run directly (python file.py), not when imported
if __name__ == "__main__":
    main()
"""),
    ("if", "if statement", r"""
# if: runs when the condition is truthy (not False, None, 0, "", [], {})
if «1:condition»:
    «0»
"""),
    ("ife", "if / else", r"""
# if / else: exactly one branch runs
if «1:condition»:
    «2:pass»
else:
    «0»
"""),
    ("elif", "if / elif / else chain", r"""
# elif chain: first true branch wins; order from most to least specific
if «1:score» >= «2:90»:
    «3:grade = "A"»
elif «1» >= «4:75»:
    «5:grade = "B"»
else:
    «0»
"""),
    ("ifn", "Nested if vs guard clause", r"""
# Nested if: the inner check only runs when the outer one passed
if «1:user» is not None:
    if «1».«2:is_active»:
        «0»
# Flatter alternative (guard clause) inside a function:
#     if «1» is None or not «1».«2»:
#         return
"""),
    ("tern", "Conditional expression (ternary)", r"""
# Python's ternary: value_if_true if condition else value_if_false
«1:label» = «2:"adult"» if «3:age >= 18» else «4:"minor"»«0»
"""),
    ("match", "match statement (switch)", r"""
# match (3.10+): Python's switch, with structural pattern matching
match «1:command»:
    case "«2:start»":
        «3»
    case "«4:stop»" | "«5:quit»":   # | matches either value
        «6»
    case {"action": action, "id": int(item_id)}:   # destructure a dict
        «7:pass»
    case _:   # default: matches anything
        «0»
"""),
    ("for", "for loop", r"""
# for iterates over any iterable directly: no index needed
for «1:item» in «2:items»:
    «0»
"""),
    ("fore", "for with enumerate / zip", r"""
# enumerate gives (index, value); zip pairs up two iterables, strict=True catches length bugs
for «1:i», «2:item» in enumerate(«3:items», start=1):
    «4»
for «5:name», «6:score» in zip(«7:names», «8:scores», strict=True):
    «0»
"""),
    ("forr", "for over range", r"""
# range(start, stop, step): stop is exclusive
for «1:i» in range(«2:0», «3:10»):
    «0»
"""),
    ("while", "while loop", r"""
# while: checks before each pass; `break` exits, `continue` skips to the next pass
while «1:condition»:
    «0»
"""),
    ("try", "try / except / else / finally", r"""
# except the narrowest exception you can handle; else runs only if nothing was raised
try:
    «1»
except «2:FileNotFoundError» as exc:
    log.warning("«3:file missing»: %s", exc)
else:
    «4:pass»
finally:
    «0»
"""),
    ("with", "with (context manager)", r"""
# with: the resource is always closed, even if an exception is raised inside
with open(«1:path», encoding="utf-8") as «2:fh»:
    «0»
"""),
    ("def", "typed function with docstring", r'''
def «1:name»(«2:value»: «3:int») -> «4:bool»:
    """«5:One line on what it does.»

    Args:
        «2»: «6:what it means»

    Returns:
        «7:what comes back»
    """
    «0»
'''),
    ("cls", "class", r'''
class «1:Account»:
    """«2:What this class represents.»"""

    def __init__(self, «3:owner»: str) -> None:
        self.«3» = «3»
        self._balance = 0   # leading underscore: internal by convention

    def __repr__(self) -> str:   # shown in the debugger and REPL
        return f"«1»(«3»={self.«3»!r})"
    «0»
'''),
    ("dc", "dataclass", r'''
from dataclasses import dataclass, field


@dataclass(slots=True)
class «1:Item»:
    """«2:A plain data record: __init__, __repr__ and __eq__ are generated.»"""

    «3:name»: str
    «4:price»: float = 0.0
    tags: list[str] = field(default_factory=list)   # never use a mutable default directly
«0»
'''),
    ("lc", "comprehensions", r"""
# List comprehension: [expression for item in iterable if condition]
«1:squares» = [«2:x * x» for «3:x» in «4:numbers» if «5:x % 2 == 0»]
# Dict comprehension
«6:by_id» = {«7:u».id: «7» for «7» in «8:users»}«0»
"""),
    ("timer", "measure elapsed time", r"""
import time

# perf_counter: the highest-resolution clock for measuring durations
«1:start» = time.perf_counter()
«0»
print(f"elapsed: {(time.perf_counter() - «1») * 1000:.1f} ms")
"""),
    ("ctimer", "timing context manager", r'''
import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    """Usage: with timer("load"): do_work()"""
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {(time.perf_counter() - start) * 1000:.1f} ms")
«0»
'''),
    ("async", "asyncio entry point", r"""
import asyncio


async def «1:fetch_one»(i: int) -> int:
    await asyncio.sleep(0.1)   # stands in for I/O: a request, a DB call
    return i


async def main() -> None:
    # gather runs coroutines concurrently and returns results in order
    results = await asyncio.gather(*(«1»(i) for i in range(«2:5»)))
    «0»


if __name__ == "__main__":
    asyncio.run(main())
"""),
    ("req", "HTTP GET with requests", r"""
import requests

# Always set a timeout: without one a hung server blocks forever
resp = requests.get(«1:"https://api.example.com/items"», params={«2:"page": 1»}, timeout=«3:10»)
resp.raise_for_status()   # turn 4xx/5xx into an exception
«4:data» = resp.json()«0»
"""),
    ("fastapi", "FastAPI app", r'''
"""FastAPI application: `uvicorn app.main:app --reload`, docs at /docs."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="«1:My API»")


class «2:Item»In(BaseModel):
    name: str = Field(min_length=1, max_length=100)   # validated automatically


class «2»Out(«2»In):
    id: int


_db: dict[int, «2»Out] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/«3:items»", status_code=status.HTTP_201_CREATED)
def create(item: «2»In) -> «2»Out:
    new = «2»Out(id=len(_db) + 1, **item.model_dump())
    _db[new.id] = new
    return new


@app.get("/«3»/{item_id}")
def read(item_id: int) -> «2»Out:
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Not found")
    return _db[item_id]
«0»
''', {"template": True}),
    ("pytest", "pytest test file", r'''
"""Tests for «1:module»."""

import pytest

from «2:app».«1» import «3:function_under_test»


def test_«4:happy_path»() -> None:
    # Arrange, act, assert
    result = «3»(«5:2»)
    assert result == «6:4»


@pytest.mark.parametrize(("value", "expected"), [(0, 0), (3, 9)])
def test_«4»_cases(value: int, expected: int) -> None:
    assert «3»(value) == expected
«0»
''', {"template": True}),
    ("logging", "logging setup", r"""
import logging

# Configure once at startup; everywhere else just use logging.getLogger(__name__)
logging.basicConfig(
    level=logging.«1:INFO»,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)«0»
"""),
    ("readcsv", "read a CSV file", r"""
import csv

# DictReader maps each row to {column_name: value}; newline="" is required by the csv module
with open(«1:"data.csv"», newline="", encoding="utf-8") as fh:
    for «2:row» in csv.DictReader(fh):
        «0»
"""),
]
