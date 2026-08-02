#!/usr/bin/env python3
"""Validate repository structure, local links, graph assets and job data."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "LICENSE.md",
    "Makefile",
    "docs/PATH.md",
    "docs/PROJECTS.md",
    "docs/GUIDES.md",
    "docs/REPOSITORY_STRATEGY.md",
    "docs/APPLICATION_STRATEGY.md",
    "docs/JOBS_2026-08-03.md",
    "docs/REVIEW_CHECKLIST.md",
    "docs/DECISIONS.md",
    "data/jobs-2026-08-03.json",
    "assets/path/path-overview.mmd",
    "assets/path/path-overview.dot",
    "assets/path/path-overview.svg",
    "assets/path/path-overview.png",
    "scripts/build_jobs.py",
    "scripts/check_repo.py",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PROJECT_IDS = [f"P{i:02d}" for i in range(1, 25)]
GUIDE_IDS = [f"G{i:02d}" for i in range(0, 15)]
VALID_GRADES = {"즉시 지원", "조건부 지원", "향후 지원"}
VALID_SOURCES = {"공식", "플랫폼"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_required(errors: list[str]) -> None:
    for rel in sorted(REQUIRED):
        if not (ROOT / rel).is_file():
            fail(errors, f"missing required file: {rel}")


def check_markdown_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "/mnt/data/" in text or "sandbox:/" in text:
            fail(errors, f"runtime-only path found: {path.relative_to(ROOT)}")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip("<>")
            parsed = urlparse(target)
            if parsed.scheme in {"http", "https", "mailto"}:
                continue
            if parsed.scheme:
                fail(errors, f"unsupported link scheme in {path.relative_to(ROOT)}: {target}")
                continue
            local = unquote(parsed.path)
            if not local:
                continue
            resolved = (path.parent / local).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(errors, f"link escapes repository in {path.relative_to(ROOT)}: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"broken local link in {path.relative_to(ROOT)}: {target}")


def check_path_tables(errors: list[str]) -> None:
    projects = (ROOT / "docs/PROJECTS.md").read_text(encoding="utf-8")
    guides = (ROOT / "docs/GUIDES.md").read_text(encoding="utf-8")
    for pid in PROJECT_IDS:
        count = len(re.findall(rf"^\| {re.escape(pid)} \|", projects, flags=re.MULTILINE))
        if count != 1:
            fail(errors, f"{pid} must have exactly one table row in docs/PROJECTS.md (found {count})")
    for gid in GUIDE_IDS:
        count = len(re.findall(rf"^\| {re.escape(gid)} \|", guides, flags=re.MULTILINE))
        if count != 1:
            fail(errors, f"{gid} must have exactly one table row in docs/GUIDES.md (found {count})")


def check_jobs(errors: list[str]) -> None:
    path = ROOT / "data/jobs-2026-08-03.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(errors, f"invalid jobs JSON: {exc}")
        return
    active = data.get("active_jobs", [])
    ids = [job.get("id") for job in active]
    urls = [job.get("url") for job in active]
    if len(ids) != len(set(ids)):
        fail(errors, "duplicate active job id")
    if len(urls) != len(set(urls)):
        fail(errors, "duplicate active job URL")
    for job in active:
        if job.get("grade") not in VALID_GRADES:
            fail(errors, f"invalid grade: {job.get('id')} -> {job.get('grade')}")
        if job.get("source_type") not in VALID_SOURCES:
            fail(errors, f"invalid source type: {job.get('id')} -> {job.get('source_type')}")
        if job.get("status") != "공고중":
            fail(errors, f"active job is not marked 공고중: {job.get('id')}")
        if not str(job.get("url", "")).startswith("https://"):
            fail(errors, f"non-HTTPS job URL: {job.get('id')}")
    expired_urls = {job.get("url") for job in data.get("expired_or_removed", [])}
    overlap = set(urls) & expired_urls
    if overlap:
        fail(errors, f"active/expired URL overlap: {sorted(overlap)}")


def check_generated_jobs(errors: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_jobs.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(errors, result.stderr.strip() or "generated job snapshot is stale")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    if not errors:
        check_markdown_links(errors)
        check_path_tables(errors)
        check_jobs(errors)
        check_generated_jobs(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("repository structure, links, PATH tables and job snapshot: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
