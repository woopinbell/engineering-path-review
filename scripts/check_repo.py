#!/usr/bin/env python3
"""Security- and integrity-focused validation for the review repository."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_TOTAL_SIZE = 25 * 1024 * 1024
BINARY_SUFFIXES = {".png"}
REQUIRED = {
    ".editorconfig", ".gitattributes", ".gitignore",
    ".github/CODEOWNERS", ".github/dependabot.yml",
    ".github/pull_request_template.md", ".github/workflows/verify.yml",
    "README.md", "LICENSE.md", "SECURITY.md", "CONTRIBUTING.md", "Makefile",
    "docs/01-PATH.md", "docs/02-L-LANE.md", "docs/03-REPOSITORY-STRATEGY.md",
    "docs/04-APPLICATION-STRATEGY.md", "docs/05-JOBS-2026-08-03.md",
    "docs/06-REVIEW-PROCESS.md", "docs/07-SECURITY-AND-INTEGRITY.md",
    "docs/08-THREAT-MODEL.md", "docs/09-SOURCES.md", "docs/10-DECISIONS.md",
    "docs/11-PARALLEL-PATH.md",
    "data/jobs-2026-08-03.json",
    "scripts/build_jobs.py", "scripts/check_repo.py", "scripts/render_graphs.sh",
    "scripts/package_release.py", "tests/test_security_tools.py",
    "targets/42-main/.editorconfig", "targets/42-main/.gitattributes", "targets/42-main/.gitignore",
    "targets/42-main/README.md", "targets/42-main/LICENSE.md",
    "targets/42-main/SECURITY.md", "targets/42-main/CONTRIBUTING.md",
    "targets/42-main/REPOSITORY-SETTINGS.md", "targets/42-main/ORPHAN-BRANCH-BASELINE.md",
    "targets/42-main/.github/CODEOWNERS", "targets/42-main/.github/dependabot.yml",
    "targets/42-main/.github/pull_request_template.md",
    "targets/42-main/.github/workflows/verify-main.yml",
    "targets/42-main/scripts/check_main.py",
    "targets/guides-main/.editorconfig", "targets/guides-main/.gitattributes", "targets/guides-main/.gitignore",
    "targets/guides-main/README.md", "targets/guides-main/LICENSE.md",
    "targets/guides-main/SECURITY.md", "targets/guides-main/CONTRIBUTING.md",
    "targets/guides-main/REPOSITORY-SETTINGS.md", "targets/guides-main/ORPHAN-BRANCH-BASELINE.md",
    "targets/guides-main/.github/CODEOWNERS", "targets/guides-main/.github/dependabot.yml",
    "targets/guides-main/.github/pull_request_template.md",
    "targets/guides-main/.github/workflows/verify-main.yml",
    "targets/guides-main/scripts/check_main.py",
    "assets/path/master-path.dot", "assets/path/master-path.mmd",
    "assets/path/master-path.svg", "assets/path/master-path.png",
    "assets/path/master-path.txt",
    "assets/path/l-lane.dot", "assets/path/l-lane.mmd",
    "assets/path/l-lane.svg", "assets/path/l-lane.png", "assets/path/l-lane.txt",
    "assets/path/career-expansion.dot", "assets/path/career-expansion.mmd",
    "assets/path/career-expansion.svg", "assets/path/career-expansion.png",
    "assets/path/career-expansion.txt",
    "assets/path/parallel-path.dot", "assets/path/parallel-path.mmd",
    "assets/path/parallel-path.svg", "assets/path/parallel-path.png",
    "assets/path/parallel-path.txt",
    "assets/path/parallel-guide-packets.dot", "assets/path/parallel-guide-packets.mmd",
    "assets/path/parallel-guide-packets.svg", "assets/path/parallel-guide-packets.png",
    "assets/path/parallel-guide-packets.txt", "assets/path/render-manifest.json",
}
PROJECT_IDS = [f"P{i:02d}" for i in range(1, 25)]
GUIDE_IDS = [f"G{i:02d}" for i in range(0, 15)]
L_IDS = [f"L{i:02d}" for i in range(1, 16)]
PARALLEL_GUIDE_COVERAGE = {
    "guide-git": "01~06",
    "guide-c": "01~10 전체",
    "guide-unix-systems": "01~09 전체",
    "guide-operating-systems": "01~10 전체",
    "guide-cpp": "01~09 전체",
    "guide-algorithms": "01~16 전체",
    "guide-computer-architecture": "01~10 전체",
    "guide-computer-networks": "01~12 전체",
    "guide-web-infrastructure": "01~07 전체",
    "guide-web-applications": "00~09 전체",
    "guide-frontend-react-nextjs": "00~04 전체",
    "guide-database-systems": "01~12 전체",
    "guide-java": "01~08 전체",
    "guide-backend-spring-boot": "01~10 전체",
    "guide-distributed-services": "01~10 전체",
    "guide-shell-scripting": "01~08 전체",
}
PARALLEL_FORBIDDEN_TERMS = (
    "`VERIFIED`", "`MISSING`", "`DEFERRED`", "가이드 풀", "개념 패킷 단위",
    "C·C++·WEB 3트랙 병렬 PATH", "P16~P24는 기본 PATH",
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
AUTOLINK_RE = re.compile(r"<((?:https?|file|javascript|data|sandbox):[^>]+)>", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
ACTION_RE = re.compile(r"^\s*uses:\s*([^\s#]+)", re.M)
FULL_SHA_RE = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
}
CONTACT_RE = re.compile(
    r"(?:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|"
    r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d))"
)
PROHIBITED_NAMES = {
    ".git", ".env", "id_rsa", "id_ed25519", "credentials", "secrets",
    "resume", "cv", "cover-letter", ".DS_Store",
}
PROHIBITED_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".pyc", ".zip"}
BIDI_OR_INVISIBLE = {chr(code) for code in [0x200B, 0x200E, 0x200F, 0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069, 0xFEFF]}
RUNTIME_MARKERS = ("/mnt/data/", "sandbox:/", "file://", "javascript:", "data:text/html")
UNSAFE_WORKFLOW_TOKENS = (
    "pull_request_target", "workflow_run", "issue_comment", "repository_dispatch",
    "permissions: write-all", "self-hosted", "curl ", "wget ", "sudo ",
    "apt-get ", "pip install", "npm install", "pnpm install",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_ignored(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False
    return bool(relative.parts and relative.parts[0] == "dist")


def iter_files() -> list[Path]:
    return sorted(
        (p for p in ROOT.rglob("*") if not is_ignored(p) and (p.is_file() or p.is_symlink())),
        key=lambda p: rel(p),
    )


def strip_fences(text: str) -> str:
    result: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence = stripped[:3]
            continue
        if fence is not None and stripped.startswith(fence):
            fence = None
            continue
        if fence is None:
            result.append(line)
    return "\n".join(result)


def github_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\-\s가-힣]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s]+", "-", text).strip("-")


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = github_slug(match.group(2))
        if not base:
            continue
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def check_required(errors: list[str]) -> None:
    for item in sorted(REQUIRED):
        if not (ROOT / item).is_file():
            errors.append(f"missing required file: {item}")


def check_filesystem(errors: list[str]) -> None:
    total_size = 0
    for path in sorted(ROOT.rglob("*"), key=lambda p: p.as_posix()):
        if is_ignored(path):
            continue
        if any(char in BIDI_OR_INVISIBLE for char in path.name):
            errors.append(f"invisible/bidirectional character in path: {rel(path)}")
        if path.is_symlink():
            errors.append(f"symlink is not allowed: {rel(path)}")
            continue
        name_lower = path.name.lower()
        if any(part.lower() == ".git" for part in path.parts):
            errors.append(f".git content is not allowed: {rel(path)}")
        if path.is_file():
            size = path.stat().st_size
            total_size += size
            if size > MAX_FILE_SIZE:
                errors.append(f"file exceeds {MAX_FILE_SIZE} bytes: {rel(path)}")
            if name_lower in PROHIBITED_NAMES or path.suffix.lower() in PROHIBITED_SUFFIXES:
                errors.append(f"prohibited file name/type: {rel(path)}")
            data = path.read_bytes()
            if path.suffix.lower() == ".png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
                errors.append(f"invalid PNG signature: {rel(path)}")
            if b"\x00" in data and path.suffix.lower() not in BINARY_SUFFIXES:
                errors.append(f"unexpected binary file: {rel(path)}")
    if total_size > MAX_TOTAL_SIZE:
        errors.append(f"repository content exceeds {MAX_TOTAL_SIZE} bytes")


def check_text_security(errors: list[str]) -> None:
    for path in iter_files():
        if path.is_symlink() or path.suffix.lower() in BINARY_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 text file: {rel(path)}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label}: {rel(path)}")
        if CONTACT_RE.search(text):
            errors.append(f"email/phone-like personal contact found: {rel(path)}")
        if any(char in BIDI_OR_INVISIBLE for char in text):
            errors.append(f"invisible/bidirectional Unicode control found: {rel(path)}")
        if "\r" in text:
            errors.append(f"CR line ending: {rel(path)}")
        if text and not text.endswith("\n"):
            errors.append(f"missing final newline: {rel(path)}")


def check_markdown_links(errors: list[str]) -> None:
    anchor_cache: dict[Path, set[str]] = {}
    for path in sorted(ROOT.rglob("*.md")):
        text = strip_fences(path.read_text(encoding="utf-8"))
        targets = LINK_RE.findall(text) + AUTOLINK_RE.findall(text)
        for raw in targets:
            target = raw.strip().split()[0].strip("<>")
            parsed = urlparse(target)
            if parsed.scheme:
                if parsed.scheme != "https":
                    errors.append(f"non-HTTPS/unsafe link in {rel(path)}: {target}")
                elif not parsed.netloc or parsed.username or parsed.password:
                    errors.append(f"invalid HTTPS URL in {rel(path)}: {target}")
                continue
            local_path = unquote(parsed.path)
            resolved = path if not local_path else (path.parent / local_path).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository in {rel(path)}: {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link in {rel(path)}: {target}")
                continue
            if parsed.fragment and resolved.suffix.lower() == ".md":
                anchors = anchor_cache.setdefault(resolved, markdown_anchors(resolved))
                if unquote(parsed.fragment).lower() not in anchors:
                    errors.append(f"missing markdown anchor in {rel(path)}: {target}")


def count_table_ids(text: str, prefix: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(rf"^\| ({prefix}\d{{2}}) \|", line)
        if match:
            counts[match.group(1)] = counts.get(match.group(1), 0) + 1
    return counts


def check_path_ids(errors: list[str]) -> None:
    path_text = (ROOT / "docs/01-PATH.md").read_text(encoding="utf-8")
    project_section = path_text.split("## 프로젝트 레인 `P`", 1)[1].split("## 가이드 레인 `G`", 1)[0]
    guide_section = path_text.split("## 가이드 레인 `G`", 1)[1].split("## 하드 게이트", 1)[0]
    project_counts = count_table_ids(project_section, "P")
    guide_counts = count_table_ids(guide_section, "G")
    for item in PROJECT_IDS:
        if project_counts.get(item, 0) != 1:
            errors.append(f"{item} must appear once in P table")
    for item in GUIDE_IDS:
        if guide_counts.get(item, 0) != 1:
            errors.append(f"{item} must appear once in G table")
    l_text = (ROOT / "docs/02-L-LANE.md").read_text(encoding="utf-8")
    l_counts = count_table_ids(l_text, "L")
    for item in L_IDS:
        if l_counts.get(item, 0) != 1:
            errors.append(f"{item} must appear once in L table")


def check_parallel_path(errors: list[str]) -> None:
    path = ROOT / "docs/11-PARALLEL-PATH.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = (
        "C·C++·WEB·SPORTSBOOK 4트랙 병렬 PATH",
        "프로젝트만 원자적으로 완료한다",
        "필수 범위는 생략하지 않고",
        "G와 P를 선형",
        "P09를 P03 뒤",
        "CPP-G02 → P09",
        "CPP-G05 → WEB-G07",
        "WEB-G04 → P22",
        "WEB-G01·WEB-G06·WEB-G07 → P24",
        "양방향 rendezvous가 아니다",
        "A 블록이 완료",
        "WEB-G01부터 WEB-G06까지 외부 선행 없이",
        "동기화 노드로 표시",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"parallel PATH missing required rule: {phrase}")
    for term in PARALLEL_FORBIDDEN_TERMS:
        if term in text:
            errors.append(f"parallel PATH contains obsolete skip/status model: {term}")
    for guide, coverage in PARALLEL_GUIDE_COVERAGE.items():
        pattern = rf"^\| `{re.escape(guide)}` \| .* \| {re.escape(coverage)} \|$"
        if not re.search(pattern, text, re.M):
            errors.append(f"parallel PATH missing mandatory guide coverage: {guide} {coverage}")
    for project in PROJECT_IDS:
        if project not in text:
            errors.append(f"parallel PATH missing project: {project}")

    overview_dot = (ROOT / "assets/path/parallel-path.dot").read_text(encoding="utf-8")
    detail_dot = (ROOT / "assets/path/parallel-guide-packets.dot").read_text(encoding="utf-8")
    for sync_id in ("C-S01", "WEB-S01", "SB-S01", "SB-S02"):
        if sync_id not in overview_dot or sync_id not in detail_dot:
            errors.append(f"parallel graph missing synchronization node: {sync_id}")
    if overview_dot.count('BGCOLOR="#fff7ed" BORDER="2" COLOR="#d97706"') != 4:
        errors.append("parallel overview synchronization nodes must share one palette")
    for token in (
        'fillcolor="#fff7ed", color="#d97706", fontcolor="#92400e", penwidth=2',
        'BGCOLOR="#ede9fe"',
        'BGCOLOR="#d1fae5"',
    ):
        if token not in detail_dot:
            errors.append(f"parallel detail graph missing synchronization styling: {token}")
    for mermaid_name in ("parallel-path.mmd", "parallel-guide-packets.mmd"):
        mermaid = (ROOT / "assets/path" / mermaid_name).read_text(encoding="utf-8")
        if "classDef sync fill:#fff7ed,stroke:#d97706,color:#92400e,stroke-width:2px" not in mermaid:
            errors.append(f"parallel Mermaid missing sync-node palette: {mermaid_name}")
        if "class CS1,WS1,SS1,SS2 sync" not in mermaid:
            errors.append(f"parallel Mermaid missing sync-node class assignment: {mermaid_name}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_render_manifest(errors: list[str]) -> None:
    manifest_path = ROOT / "assets/path/render-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid render manifest: {exc}")
        return
    for name in ("master-path", "l-lane", "career-expansion", "parallel-path", "parallel-guide-packets"):
        record = manifest.get(name)
        if not isinstance(record, dict):
            errors.append(f"missing graph manifest entry: {name}")
            continue
        for suffix in ("dot", "svg", "png"):
            path = ROOT / "assets/path" / f"{name}.{suffix}"
            expected = record.get(f"{suffix}_sha256")
            if not path.is_file() or expected != sha256(path):
                errors.append(f"stale or mismatched graph asset: {name}.{suffix}")
    for svg in sorted((ROOT / "assets/path").glob("*.svg")):
        text = svg.read_text(encoding="utf-8")
        lowered = text.lower()
        for token in ("<script", "javascript:", "data:", "onload=", "onerror=", "<!entity"):
            if token in lowered:
                errors.append(f"unsafe SVG token {token!r}: {rel(svg)}")
        if "<!doctype" in lowered:
            errors.append(f"SVG DOCTYPE must be removed: {rel(svg)}")
        external_href = re.search(r"(?:href|xlink:href)=[\"'](?:https?:|//)", text, re.I)
        if external_href:
            errors.append(f"external SVG reference: {rel(svg)}")


def check_workflows(errors: list[str]) -> None:
    workflows = sorted(ROOT.rglob(".github/workflows/*.yml")) + sorted(ROOT.rglob(".github/workflows/*.yaml"))
    for path in workflows:
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for token in UNSAFE_WORKFLOW_TOKENS:
            if token.lower() in lowered:
                errors.append(f"unsafe workflow token {token!r}: {rel(path)}")
        if "permissions:\n  contents: read" not in text:
            errors.append(f"workflow must declare read-only contents: {rel(path)}")
        if "persist-credentials: false" not in text:
            errors.append(f"workflow checkout must disable persisted credentials: {rel(path)}")
        if "timeout-minutes:" not in text:
            errors.append(f"workflow job needs timeout-minutes: {rel(path)}")
        for action in ACTION_RE.findall(text):
            if not FULL_SHA_RE.fullmatch(action):
                errors.append(f"action is not pinned to full SHA in {rel(path)}: {action}")


def check_source_syntax(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.py")):
        if is_ignored(path):
            continue
        try:
            compile(path.read_text(encoding="utf-8"), rel(path), "exec")
        except SyntaxError as exc:
            errors.append(f"Python syntax error in {rel(path)}: {exc}")
    for path in sorted(ROOT.rglob("*.sh")):
        if is_ignored(path):
            continue
        result = subprocess.run(["bash", "-n", str(path)], text=True, capture_output=True, check=False)
        if result.returncode:
            errors.append(f"shell syntax error in {rel(path)}: {result.stderr.strip()}")


def check_targets(errors: list[str]) -> None:
    for target in (ROOT / "targets/42-main", ROOT / "targets/guides-main"):
        result = subprocess.run(
            [sys.executable, str(target / "scripts/check_main.py")],
            cwd=target,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            errors.append(f"target check failed {target.name}: {result.stderr.strip() or result.stdout.strip()}")


def check_generated(errors: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_jobs.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        errors.append(result.stderr.strip() or "generated jobs document is stale")


def check_package_manifest(errors: list[str]) -> None:
    path = ROOT / "MANIFEST.sha256"
    if not path.exists():
        return
    expected_paths: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            errors.append("invalid MANIFEST.sha256 line")
            continue
        digest, item = match.groups()
        if item == "MANIFEST.sha256":
            errors.append("manifest must not list itself")
            continue
        target = (ROOT / item).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"manifest path escapes repository: {item}")
            continue
        if not target.is_file() or target.is_symlink():
            errors.append(f"manifest target missing/not regular: {item}")
            continue
        if sha256(target) != digest:
            errors.append(f"manifest hash mismatch: {item}")
        expected_paths.add(item)
    actual = {
        rel(item) for item in iter_files()
        if not item.is_symlink() and rel(item) != "MANIFEST.sha256" and not rel(item).startswith("dist/")
    }
    if expected_paths != actual:
        missing = sorted(actual - expected_paths)
        extra = sorted(expected_paths - actual)
        if missing:
            errors.append(f"manifest missing files: {missing[:8]}")
        if extra:
            errors.append(f"manifest extra files: {extra[:8]}")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_filesystem(errors)
    if not errors:
        check_text_security(errors)
        check_markdown_links(errors)
        check_path_ids(errors)
        check_parallel_path(errors)
        check_render_manifest(errors)
        check_workflows(errors)
        check_source_syntax(errors)
        check_targets(errors)
        check_generated(errors)
        check_package_manifest(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("repository structure, links, PATH/L, targets, jobs, workflows and package integrity: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
