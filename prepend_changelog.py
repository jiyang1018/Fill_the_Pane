"""
prepend_changelog.py -- used by release.bat during the release process.

Reads the entry for VERSION from changelog.md (the dev changelog beside
the source files), formats it, and prepends it to CHANGELOG.md (the
user-facing changelog in the repo root).

Usage:
    python prepend_changelog.py <version>
    e.g.: python prepend_changelog.py 0.6.02

The dev changelog (changelog.md) must have an entry in the format:
    **v0.6.02**
    - bullet one
    - bullet two

The output entry written to CHANGELOG.md will be:
    ## Fill the Pane v0.6.02 -- 2026-05-11

    - bullet one
    - bullet two

    ---

"""

import sys
import os
import re
from datetime import date

if len(sys.argv) < 2:
    print("Usage: python prepend_changelog.py <version>")
    sys.exit(1)

version   = sys.argv[1].lstrip("v")
today     = date.today().strftime("%Y-%m-%d")
src_path  = os.path.join(os.path.dirname(__file__), "changelog.md")
dest_path = os.path.join(os.path.dirname(__file__), "CHANGELOG.md")

# ── Read dev changelog ────────────────────────────────────────────────────────
if not os.path.exists(src_path):
    print(f"ERROR: {src_path} not found.")
    sys.exit(1)

with open(src_path, "r", encoding="utf-8") as f:
    src = f.read()

# Find the block for this version: from **vVERSION** up to the next **v or EOF
pattern = re.compile(
    r"^\*\*v" + re.escape(version) + r"\*\*\s*\n(.*?)(?=^\*\*v|\Z)",
    re.MULTILINE | re.DOTALL
)
match = pattern.search(src)

if not match:
    print(f"ERROR: No entry found for v{version} in {src_path}.")
    sys.exit(1)

bullets = match.group(1).strip()

# ── Format entry ──────────────────────────────────────────────────────────────
header = f"## Fill the Pane v{version} -- {today}\n\n"
entry  = header + bullets + "\n\n---\n\n"

# ── Prepend to CHANGELOG.md ───────────────────────────────────────────────────
existing = ""
if os.path.exists(dest_path):
    with open(dest_path, "r", encoding="utf-8") as f:
        existing = f.read()

with open(dest_path, "w", encoding="utf-8") as f:
    f.write(entry + existing)

print(f"CHANGELOG.md updated with v{version} entry.")
