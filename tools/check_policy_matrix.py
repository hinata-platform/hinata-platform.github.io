#!/usr/bin/env python3
"""Check that the policy matrix in admin-time-tracking.md matches the server code.

Reads the policy fields from ServerSettings.java and compares them with the
backticked names in the first column of the matrix table, in English and German.

Fails when a field from the code is missing in a matrix, or when a matrix names
a field the code does not have.

Usage:
    python3 tools/check_policy_matrix.py [path/to/ServerSettings.java]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = (
    REPO.parent
    / "hinata-server/src/main/java/com/ahmadre/hinata/setup/ServerSettings.java"
)

# The nested classes of ServerSettings whose fields are policies in the matrix.
# Absence and billing policies live inside TimeTracking (absenceManagementEnabled,
# absenceManagers, absenceCalendarVisibility, absenceReportsEnabled,
# absenceRateEnabled, timeOffRetention, expiryNotice, billingEnabled, currency).
# Holidays holds the platform's holiday region.
SOURCES = ["TimeTracking", "Holidays"]

# Fields that are not policies: read-only views the server fills on the way out.
IGNORED = {"effective"}

# The heading the matrix sits under, per language.
MATRICES = {
    "content/en/admin-time-tracking.md": "## Policy matrix",
    "content/de/admin-time-tracking.md": "## Richtlinienmatrix",
}

FIELD = re.compile(r"^\s*private\s+(?!static\b)(?:final\s+)?[\w.<>,\s?]+?\s+(\w+)\s*(?:=[^;]*)?;")
CLASS = re.compile(r"\bclass\s+(\w+)")
CAMEL = re.compile(r"`([a-z][A-Za-z0-9]*)`")


def class_bodies(java: str) -> dict[str, list[tuple[int, str]]]:
    """Map every class name to its lines, each with the brace depth inside that class."""
    bodies: dict[str, list[tuple[int, str]]] = {}
    stack: list[tuple[str, int]] = []
    depth = 0
    pending: str | None = None
    for line in java.splitlines():
        code = re.sub(r"//.*", "", line)
        match = CLASS.search(code)
        if match and not code.strip().startswith("*"):
            pending = match.group(1)
        for name, start in stack:
            bodies.setdefault(name, []).append((depth - start, code))
        for char in code:
            if char == "{":
                depth += 1
                if pending:
                    stack.append((pending, depth))
                    pending = None
            elif char == "}":
                if stack and stack[-1][1] == depth:
                    stack.pop()
                depth -= 1
    return bodies


def fields(bodies: dict[str, list[tuple[int, str]]], name: str) -> list[str]:
    """The fields declared directly in a class, not in its nested classes."""
    found = []
    for level, code in bodies.get(name, []):
        if level != 0:
            continue
        match = FIELD.match(code)
        if match and match.group(1) not in IGNORED:
            found.append(match.group(1))
    return found


def nested(bodies: dict[str, list[tuple[int, str]]], name: str) -> set[str]:
    """Every field of every class, so a matrix may also name a sub-field."""
    return {f for cls in bodies for f in fields(bodies, cls)}


def matrix_names(markdown: str, heading: str) -> set[str] | None:
    """Backticked camelCase names in the first column of the table under the heading."""
    lines = markdown.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return None
    names: set[str] = set()
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        first = line.split("|")[1]
        names.update(CAMEL.findall(first))
    return names


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not source.is_file():
        print(f"ServerSettings.java not found: {source}")
        return 1
    bodies = class_bodies(source.read_text(encoding="utf-8"))

    expected: set[str] = set()
    for cls in SOURCES:
        found = fields(bodies, cls)
        if not found:
            print(f"No fields found in ServerSettings.{cls}. Did the class move?")
            return 1
        expected.update(found)
    known = expected | nested(bodies, "ServerSettings")

    failed = False
    for rel, heading in MATRICES.items():
        path = REPO / rel
        if not path.is_file():
            print(f"{rel}: file missing")
            failed = True
            continue
        names = matrix_names(path.read_text(encoding="utf-8"), heading)
        if names is None:
            print(f"{rel}: heading '{heading}' missing")
            failed = True
            continue
        missing = sorted(expected - names)
        unknown = sorted(names - known)
        for name in missing:
            print(f"{rel}: policy `{name}` is in the code but not in the matrix")
        for name in unknown:
            print(f"{rel}: `{name}` is in the matrix but not in the code")
        failed = failed or bool(missing or unknown)

    if failed:
        return 1
    print(f"Policy matrix OK: {len(expected)} policies from {', '.join(SOURCES)} in both languages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
