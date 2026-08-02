#!/usr/bin/env python3
"""Validate the guides default-branch document set."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    ".editorconfig", ".gitattributes", ".gitignore",
    "README.md", "LICENSE.md", "SECURITY.md", "CONTRIBUTING.md",
    "REPOSITORY-SETTINGS.md", "ORPHAN-BRANCH-BASELINE.md",
    ".github/CODEOWNERS", ".github/dependabot.yml",
    ".github/pull_request_template.md", ".github/workflows/verify-main.yml",
    "scripts/check_main.py",
}
GUIDES = [
    "guide-git", "guide-c", "guide-unix-systems", "guide-python",
    "guide-shell-scripting", "guide-cpp", "guide-operating-systems",
    "guide-algorithms", "guide-computer-architecture",
    "guide-computer-networks", "guide-web-infrastructure",
    "guide-web-applications", "guide-frontend-react-nextjs",
    "guide-database-systems", "guide-java",
    "guide-backend-spring-boot", "guide-distributed-services",
]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    for rel in sorted(REQUIRED):
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")
    prohibited_dirs = {"docs", "examples", "exercises", "reference", "projects"}
    for name in prohibited_dirs:
        if (ROOT / name).exists():
            errors.append(f"main must not contain guide implementation directory: {name}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    links = [item.strip().split()[0].strip("<>") for item in LINK_RE.findall(readme)]
    for name in GUIDES:
        expected = f"https://github.com/woopinbell/guides/tree/{name}"
        if links.count(expected) != 1:
            errors.append(f"guide branch link must appear once: {name}")
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip("<>")
            parsed = urlparse(target)
            if parsed.scheme:
                if parsed.scheme != "https":
                    errors.append(f"non-HTTPS link in {path.relative_to(ROOT)}: {target}")
                continue
            if not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository: {path.relative_to(ROOT)}: {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link: {path.relative_to(ROOT)}: {target}")
    workflow = ROOT / ".github/workflows/verify-main.yml"
    if workflow.exists():
        w = workflow.read_text(encoding="utf-8")
        for forbidden in ("pull_request_target", "workflow_run", "issue_comment", "permissions: write-all"):
            if forbidden in w:
                errors.append(f"unsafe workflow token: {forbidden}")
        if "permissions:\n  contents: read" not in w or "persist-credentials: false" not in w:
            errors.append("workflow must use read-only token and disable persisted credentials")
        if "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd" not in w:
            errors.append("checkout must be pinned to the approved full SHA")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("guides main document set: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
