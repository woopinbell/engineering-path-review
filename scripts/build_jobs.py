#!/usr/bin/env python3
"""Validate and render the static job snapshot from canonical JSON."""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "jobs-2026-08-03.json"
OUTPUT = ROOT / "docs" / "05-JOBS-2026-08-03.md"

CATEGORY_NAMES = {
    "A": "프런트엔드",
    "B": "풀스택",
    "C": "Node·TypeScript 백엔드",
    "D": "Java·Spring 백엔드",
    "E": "C·C++ 시스템·서버",
    "G": "일반 주니어 개발",
}
VALID_GRADES = {"즉시 지원", "조건부 지원", "향후 지원"}
VALID_SOURCES = {"공식", "플랫폼"}
VALID_EMPLOYMENT = {"정규직", "정규직전환형"}
PLATFORM_DOMAINS = {"www.wanted.co.kr", "www.rallit.com", "www.jobkorea.co.kr"}
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
CONTACT_RE = re.compile(
    r"(?:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|"
    r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d))"
)


def load_data() -> dict[str, object]:
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {DATA.relative_to(ROOT)}: {exc}") from exc
    validate_data(data)
    return data


def safe_text(value: object, *, field: str) -> str:
    text = str(value).strip()
    if CONTROL_RE.search(text):
        raise ValueError(f"control character in {field}")
    if CONTACT_RE.search(text):
        raise ValueError(f"contact information is not allowed in {field}")
    return text


def validate_https(url: object, *, field: str) -> str:
    text = safe_text(url, field=field)
    parsed = urlparse(text)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f"invalid HTTPS URL in {field}: {text}")
    return text


def validate_data(data: dict[str, object]) -> None:
    required_top = {
        "snapshot_date", "checked_at", "timezone", "snapshot_kind", "source_policy",
        "privacy_policy", "candidate_profile", "grade_definitions", "active_jobs",
        "expired_or_removed",
    }
    missing = required_top - set(data)
    if missing:
        raise ValueError(f"missing top-level keys: {sorted(missing)}")
    snapshot = date.fromisoformat(str(data["snapshot_date"]))
    date.fromisoformat(str(data["checked_at"]))
    if data["timezone"] != "Asia/Seoul" or data["snapshot_kind"] != "정적 스냅숏":
        raise ValueError("unexpected snapshot metadata")
    definitions = data["grade_definitions"]
    if not isinstance(definitions, dict) or set(definitions) != VALID_GRADES:
        raise ValueError("grade_definitions must contain exactly three grades")
    active = data["active_jobs"]
    expired = data["expired_or_removed"]
    if not isinstance(active, list) or not isinstance(expired, list):
        raise ValueError("job collections must be lists")
    ids: set[str] = set()
    urls: set[str] = set()
    company_titles: set[tuple[str, str]] = set()
    for index, job in enumerate(active):
        if not isinstance(job, dict):
            raise ValueError(f"active_jobs[{index}] must be an object")
        required = {
            "id", "company", "title", "categories", "milestone", "grade",
            "source_type", "status", "employment", "location", "remote",
            "experience", "deadline", "url", "status_basis", "fit", "gap",
            "portfolio", "checked_at", "evidence_kind",
        }
        missing_job = required - set(job)
        if missing_job:
            raise ValueError(f"active job missing keys {job.get('id', index)}: {sorted(missing_job)}")
        job_id = safe_text(job["id"], field=f"job[{index}].id")
        if not re.fullmatch(r"[a-z0-9-]+", job_id) or job_id in ids:
            raise ValueError(f"invalid or duplicate job id: {job_id}")
        ids.add(job_id)
        company = safe_text(job["company"], field=f"{job_id}.company")
        title = safe_text(job["title"], field=f"{job_id}.title")
        key = (company.casefold(), title.casefold())
        if key in company_titles:
            raise ValueError(f"duplicate company/title: {company} / {title}")
        company_titles.add(key)
        url = validate_https(job["url"], field=f"{job_id}.url")
        if url in urls:
            raise ValueError(f"duplicate active URL: {url}")
        urls.add(url)
        if job["grade"] not in VALID_GRADES or job["source_type"] not in VALID_SOURCES:
            raise ValueError(f"invalid grade/source: {job_id}")
        if job["employment"] not in VALID_EMPLOYMENT:
            raise ValueError(f"employment is outside the requested scope: {job_id}")
        hostname = (urlparse(url).hostname or "").lower()
        if job["source_type"] == "플랫폼" and hostname not in PLATFORM_DOMAINS:
            raise ValueError(f"unapproved platform domain: {job_id} / {hostname}")
        if job["source_type"] == "공식" and hostname in PLATFORM_DOMAINS:
            raise ValueError(f"official source points to a platform: {job_id}")
        if job["status"] != "공고중":
            raise ValueError(f"active job must be 공고중: {job_id}")
        categories = job["categories"]
        if not isinstance(categories, list) or not categories or len(categories) != len(set(categories)) or any(c not in CATEGORY_NAMES for c in categories):
            raise ValueError(f"invalid categories: {job_id}")
        portfolio = job["portfolio"]
        if not isinstance(portfolio, list) or any(not isinstance(v, str) for v in portfolio):
            raise ValueError(f"invalid portfolio: {job_id}")
        deadline = job.get("deadline")
        if isinstance(deadline, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", deadline):
            if date.fromisoformat(deadline) < snapshot:
                raise ValueError(f"active job has past deadline: {job_id}")
        for field in ("milestone", "employment", "location", "remote", "experience", "status_basis", "fit", "gap", "evidence_kind"):
            safe_text(job[field], field=f"{job_id}.{field}")
        if str(job["checked_at"]) != str(data["checked_at"]):
            raise ValueError(f"checked_at mismatch: {job_id}")
    expired_urls: set[str] = set()
    for index, job in enumerate(expired):
        if not isinstance(job, dict):
            raise ValueError(f"expired_or_removed[{index}] must be an object")
        for field in ("company", "title", "reason", "evidence_kind"):
            safe_text(job[field], field=f"expired[{index}].{field}")
        url = validate_https(job["url"], field=f"expired[{index}].url")
        if url in expired_urls:
            raise ValueError(f"duplicate expired URL: {url}")
        expired_urls.add(url)
        if str(job["checked_at"]) != str(data["checked_at"]):
            raise ValueError(f"expired checked_at mismatch: {url}")
    overlap = urls & expired_urls
    if overlap:
        raise ValueError(f"active/expired URL overlap: {sorted(overlap)}")


def milestone_key(value: str) -> int:
    matches = [int(token) for token in re.findall(r"P(\d{2})", value)]
    return min(matches) if matches else 999


def cell(value: object) -> str:
    return html.escape(str(value), quote=True).replace("|", "&#124;").replace("\n", " ").strip()


def render() -> str:
    data = load_data()
    active = data["active_jobs"]
    expired = data["expired_or_removed"]
    assert isinstance(active, list) and isinstance(expired, list)
    counts = Counter(str(job["grade"]) for job in active)
    source_counts = Counter(str(job["source_type"]) for job in active)
    lines: list[str] = [
        "<!-- Generated by scripts/build_jobs.py. Edit data/jobs-2026-08-03.json instead. -->",
        "# 채용 공고 정적 스냅숏 — 2026-08-03",
        "",
        "> 기준일 당시 확인한 정적 기록이다. 현재 모집 상태를 자동 보장하지 않으며 실제 지원 직전에 원문을 다시 확인한다.",
        "",
        "## 범위",
        "",
        f"- 공고중 후보 **{len(active)}개**: 공식 {source_counts['공식']}개, 플랫폼 {source_counts['플랫폼']}개",
        f"- 등급: 즉시 {counts['즉시 지원']}개, 조건부 {counts['조건부 지원']}개, 향후 {counts['향후 지원']}개",
        "- 한국 전국·원격과 해외 원격, 정규직 또는 정규직전환형",
        "- 신입·경력 무관·1~3년 요구까지 후보로 검토",
        "- 기업 공식 페이지 우선, 플랫폼은 공식 페이지를 찾지 못한 경우 보조",
        "- 공고 전문·로고·연락처를 복제하지 않고 자체 요약과 원문 링크만 제공",
        "",
        "## 판정 전제",
        "",
        "```text",
        "컴퓨터공학 학사 · 42 수료 · 병역 만기 전역",
        "즉시 입사 가능 · 해외근무 결격사유 없음 · 업무 영어는 약한 편",
        "각 행의 최소 PATH까지 실제 완료·검증·공개한 상태만 역량으로 계산",
        "```",
        "",
        "## 등급",
        "",
    ]
    definitions = data["grade_definitions"]
    assert isinstance(definitions, dict)
    for grade in ("즉시 지원", "조건부 지원", "향후 지원"):
        lines.append(f"- **{grade}**: {cell(definitions[grade])}")
    lines += [
        "",
        "## 직군 코드",
        "",
        " · ".join(f"`{key}` {value}" for key, value in CATEGORY_NAMES.items()),
        "",
    ]
    for grade in ("즉시 지원", "조건부 지원", "향후 지원"):
        jobs = sorted(
            (job for job in active if job["grade"] == grade),
            key=lambda job: (milestone_key(str(job["milestone"])), str(job["company"]), str(job["title"])),
        )
        lines += [
            f"## {grade}",
            "",
            "| 최소 PATH | 직군 | 공고 | 조건 | 적합 근거 | 남은 공백 |",
            "|---|---|---|---|---|---|",
        ]
        for job in jobs:
            categories = ", ".join(cell(v) for v in job["categories"])
            url = str(job["url"])
            title = (
                f"[{cell(job['company'])} — {cell(job['title'])}]({url})"
                f"<br><sub>{cell(job['source_type'])} · {cell(job['status'])} · {cell(job['experience'])}</sub>"
            )
            deadline = job.get("deadline") or "원문 확인"
            condition = (
                f"{cell(job['employment'])}<br>{cell(job['location'])}<br>"
                f"{cell(job['remote'])}<br><sub>{cell(deadline)}</sub>"
            )
            lines.append(
                f"| {cell(job['milestone'])} | {categories} | {title} | {condition} | "
                f"{cell(job['fit'])} | {cell(job['gap'])} |"
            )
        lines.append("")
    lines += [
        "## 만료·제외 확인 목록",
        "",
        "검색 결과에 나타났지만 기준일에 마감·삭제·과거 마감일이 확인된 항목이다. 활성 후보 수에 포함하지 않는다.",
        "",
        "| 회사 | 공고 | 제외 사유 |",
        "|---|---|---|",
    ]
    for job in sorted(expired, key=lambda item: (str(item["company"]), str(item["title"]))):
        lines.append(
            f"| {cell(job['company'])} | [{cell(job['title'])}]({job['url']}) | {cell(job['reason'])} |"
        )
    lines += [
        "",
        "## 지원 직전 확인",
        "",
        "1. 원문에 지원하기·채용 중·상시채용 또는 유효한 미래 마감일이 남아 있는지 확인한다.",
        "2. 공식 페이지가 생겼다면 플랫폼 링크를 공식 링크로 교체한다.",
        "3. 최소 PATH 프로젝트가 실제 완료·검증·공개됐는지 확인한다.",
        "4. 직군에 맞는 대표 저장소만 이력서와 GitHub 상단에 배치한다.",
        "5. 경력·영어·현장 경험 요건이 바뀌면 등급을 다시 판정한다.",
        "",
        "## 데이터 정본",
        "",
        "이 문서는 [`data/jobs-2026-08-03.json`](../data/jobs-2026-08-03.json)에서 생성한다. JSON만 수정한 뒤 `make jobs`를 실행한다.",
        "",
    ]
    return "\n".join(lines)


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    except Exception:
        Path(name).unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        rendered = render()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print(f"out of date: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        return 0
    atomic_write(OUTPUT, rendered)
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
