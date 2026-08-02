# Engineering Path Review

`42`와 `guides`의 최종 구조·문서·PATH를 확정하기 위한 **임시 검토 저장소**다. 프로젝트·가이드 코드는 이 저장소에 넣지 않는다.

![P/G/L 선형·병렬 PATH](assets/path/path-overview.svg)

## 실행 결론

```text
한 번에 P 1개 + G 1개 + L 1세션
P14 완료·배포 직후 첫 일반 지원
P15·P17·P20에서 지원 직군을 순차 확대
42/guides main은 색인·정책만
각 orphan branch와 독립 저장소는 정본을 하나만 유지
```

## 문서 지도

| 문서 | 단일 책임 |
|---|---|
| [PATH](docs/PATH.md) | P/G/L 선형·병렬 구조, 하드 게이트, 지원 마일스톤 |
| [프로젝트 24개](docs/PROJECTS.md) | 한 줄 역할·진입 조건·완료 결과·공개 위치 |
| [가이드 17개](docs/GUIDES.md) | 필수·조건부 가이드의 역할·진입·완료·장벽 |
| [저장소 전략](docs/REPOSITORY_STRATEGY.md) | `42`·`guides` main, orphan branch, 독립 정본 정책 |
| [채용 지원 전략](docs/APPLICATION_STRATEGY.md) | 첫 지원 시점, 지원 파동, 공고 등급, 대표 저장소 |
| [현재 공고](docs/JOBS_2026-08-03.md) | 2026-08-03 기준 공고중·만료 정적 snapshot |
| [최종 확정 체크리스트](docs/REVIEW_CHECKLIST.md) | 실제 `42/main`·`guides/main` 반영 전 검사 |
| [결정 기록](docs/DECISIONS.md) | 합의된 조건과 마지막 미확정 항목 |

## 검사

```sh
make check
```

검사 범위:

```text
필수 파일
상대 링크
P01~P24·G00~G14 표
그래프 원본·렌더링 파일
공고 ID·URL 중복과 상태 분류
JSON 정본과 Markdown snapshot의 일치
```

공고 JSON을 수정한 경우:

```sh
make jobs
make check
```

## 이 저장소가 끝나는 시점

[`REVIEW_CHECKLIST.md`](docs/REVIEW_CHECKLIST.md)가 모두 닫히고 승인된 내용이 `42/main`과 `guides/main`에 반영되면 이 저장소는 archive한다.

## 라이선스

범위와 제3자 예외는 [LICENSE.md](LICENSE.md)를 따른다.
