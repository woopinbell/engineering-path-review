#!/usr/bin/env python3
"""Render the static job snapshot from the canonical JSON data file."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "jobs-2026-08-03.json"
OUTPUT = ROOT / "docs" / "JOBS_2026-08-03.md"

CATEGORY_NAMES = {
    "A": "프런트엔드",
    "B": "풀스택",
    "C": "Node·TypeScript 백엔드",
    "D": "Java·Spring 백엔드",
    "E": "C·C++ 시스템·서버",
    "G": "일반 주니어 개발",
}
GRADE_ORDER = {"즉시 지원": 0, "조건부 지원": 1, "향후 지원": 2}
MILESTONE_ORDER = {"P11": 11, "P14": 14, "P15": 15, "P17": 17, "P20": 20, "P22": 22}


def milestone_key(value: str) -> int:
    for token, order in MILESTONE_ORDER.items():
        if token in value:
            return order
    return 999


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render() -> str:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    active = data["active_jobs"]
    expired = data["expired_or_removed"]
    counts = Counter(job["grade"] for job in active)
    source_counts = Counter(job["source_type"] for job in active)

    lines: list[str] = []
    lines.extend(
        [
            "# 채용 공고 정적 스냅숏 — 2026-08-03",
            "",
            "> 이 문서는 검색 기준일 당시 확인한 공고만 기록한다. 채용 상태는 수시로 바뀌므로 실제 지원 직전에 원문을 다시 확인한다.",
            "",
            "## 판정 기준",
            "",
            f"- 활성 후보 **{len(active)}개**: 공식 {source_counts['공식']}개, 플랫폼 {source_counts['플랫폼']}개",
            f"- 지원 등급: 즉시 {counts['즉시 지원']}개, 조건부 {counts['조건부 지원']}개, 향후 {counts['향후 지원']}개",
            "- 기업 공식 채용 페이지를 우선하고, 플랫폼 공고는 공식 페이지에서 같은 공고를 찾지 못한 경우만 사용했다.",
            "- 동일 URL과 동일 회사·직무의 명백한 중복을 제거했다.",
            "- 공고 전문은 복제하지 않고 자체 요약, 적합 근거, 남은 공백과 원문 링크만 제공한다.",
            "- 학력·병역·입사 가능 시점은 충족으로 보며, 영어가 핵심 필수인 해외 공고는 `향후 지원`으로 분류했다.",
            "",
            "### 등급",
            "",
        ]
    )
    for grade in ("즉시 지원", "조건부 지원", "향후 지원"):
        lines.append(f"- **{grade}**: {data['grade_definitions'][grade]}")
    lines.extend(
        [
            "",
            "### 직군 코드",
            "",
            " · ".join(f"`{key}` {value}" for key, value in CATEGORY_NAMES.items()),
            "",
        ]
    )

    for grade in ("즉시 지원", "조건부 지원", "향후 지원"):
        jobs = sorted(
            (job for job in active if job["grade"] == grade),
            key=lambda job: (milestone_key(job["milestone"]), job["company"], job["title"]),
        )
        lines.extend(
            [
                f"## {grade}",
                "",
                "| 최소 PATH | 직군 | 공고 | 고용·지역 | 적합 근거 | 남은 공백 |",
                "|---|---|---|---|---|---|",
            ]
        )
        for job in jobs:
            categories = ", ".join(job["categories"])
            source = f"{job['source_type']}·{job['status']}"
            title = f"[{esc(job['company'])} — {esc(job['title'])}]({job['url']})<br><sub>{source} · {esc(job['experience'])}</sub>"
            work = f"{esc(job['employment'])}<br>{esc(job['location'])}<br>{esc(job['remote'])}"
            fit = esc(job["fit"])
            gap = esc(job["gap"])
            lines.append(
                f"| {esc(job['milestone'])} | {categories} | {title} | {work} | {fit} | {gap} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 만료·제외 확인 목록",
            "",
            "검색 결과에 나타났지만 기준일에 만료됐거나 활성 공고와 중복된 항목이다. 활성 후보 수에 포함하지 않는다.",
            "",
            "| 회사 | 공고 | 제외 사유 |",
            "|---|---|---|",
        ]
    )
    for job in sorted(expired, key=lambda item: (item["company"], item["title"])):
        lines.append(
            f"| {esc(job['company'])} | [{esc(job['title'])}]({job['url']}) | {esc(job['reason'])} |"
        )

    lines.extend(
        [
            "",
            "## 지원 직전 확인",
            "",
            "1. 공고 페이지가 열리고 `지원하기`, `상시채용` 또는 미래 마감일이 남아 있는지 확인한다.",
            "2. 같은 회사의 공식 채용 페이지가 생겼다면 플랫폼 링크를 공식 링크로 교체한다.",
            "3. 최소 PATH 마일스톤의 프로젝트가 실제로 완료·검증·공개됐는지 확인한다.",
            "4. 지원 직군에 맞는 대표 저장소만 이력서와 GitHub 상단에 배치한다.",
            "5. 경력 요구가 바뀌거나 영어·현장 경험이 필수로 강화됐으면 등급을 다시 판정한다.",
            "",
            "## 데이터 정본",
            "",
            "이 문서는 [`data/jobs-2026-08-03.json`](../data/jobs-2026-08-03.json)에서 생성한다. 직접 표를 수정하지 않고 JSON을 수정한 뒤 `make jobs`를 실행한다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the generated file is out of date")
    args = parser.parse_args()
    rendered = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print(f"out of date: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
