# Engineering Path Review

`42`와 `guides`의 구조·PATH·공개 정책·보안 설정·채용 전략을 **검토하고 확정하기 위한 임시 저장소**다. 프로젝트와 가이드 구현의 정본은 이 저장소에 두지 않는다.

![P·G·L 선형·병렬 PATH](assets/path/master-path.svg)

## 먼저 읽을 문서

| 순서 | 문서 | 결정 대상 |
|---:|---|---|
| 1 | [선형·병렬 PATH](docs/01-PATH.md) | 보수적 기본 P·G 진행, 하드 게이트, 채용 마일스톤 |
| 2 | [복습용 3트랙 병렬 PATH](docs/11-PARALLEL-PATH.md) | C·C++·WEB 동시 진행, 트랙 내부 G·P 선형 배치, 필수 가이드 분할 이수 |
| 3 | [L 작업 레인](docs/02-L-LANE.md) | 코딩 테스트·감사·지원 준비를 언제 한 회차씩 여는지 |
| 4 | [저장소·orphan branch 전략](docs/03-REPOSITORY-STRATEGY.md) | `42`, `guides`, 독립 저장소의 단일 정본과 보안 한계 |
| 5 | [채용 지원 전략](docs/04-APPLICATION-STRATEGY.md) | P14 첫 지원과 이후 직군 확장 |
| 6 | [채용 공고 스냅숏](docs/05-JOBS-2026-08-03.md) | 기준일 당시 공고중·만료·등급·최소 PATH |
| 7 | [검토·확정 절차](docs/06-REVIEW-PROCESS.md) | P0/P1 처리와 최종 이전 순서 |
| 8 | [보안·무결성 기준](docs/07-SECURITY-AND-INTEGRITY.md) | 계정·ruleset·Actions·secret·release 설정 |
| 9 | [위협 모델](docs/08-THREAT-MODEL.md) | 이 구조에서 실제로 방어할 실패와 비범위 |
| 10 | [근거 등록부](docs/09-SOURCES.md) | 제공 자료·GitHub·웹 조사·분석 판단의 구분 |
| 11 | [결정 기록](docs/10-DECISIONS.md) | 확정 사항과 변경이 필요한 조건 |

## 최종 저장소로 옮길 후보 문서 세트

| 대상 | 후보 문서 |
|---|---|
| `42/main` | [`targets/42-main/`](targets/42-main/README.md) |
| `guides/main` | [`targets/guides-main/`](targets/guides-main/README.md) |

각 후보 세트는 README·LICENSE뿐 아니라 SECURITY·CONTRIBUTING·권장 저장소 설정·main 전용 검증 workflow까지 포함한다.

## 레인 규칙

> **복습용 3트랙 모드에서는 C·C++·WEB을 병렬 진행하고, 각 트랙 안에 필요한 G 구간과 P를 선형으로 교차 배치한다. P만 원자적으로 완료하며, G는 시점별로 나누어 진행하되 필수 범위를 생략하지 않는다.**

```text
P: 프로젝트 1개
G: 가이드 1개
L: 조건이 충족됐을 때 여는 한정 작업 1회
```

`L`은 세 번째 장기 학습 spine이 아니다. 코딩 테스트, 연결 감사, 지원 준비처럼 **명시된 트리거가 생겼을 때만 열고 한 회차에서 닫는 작업 큐**다. 복습용 3트랙 모드의 정확한 G·P 순서와 가이드 커버리지는 [3트랙 병렬 PATH](docs/11-PARALLEL-PATH.md)를 따른다.

```text
C: ________ | C++: ________ | WEB: ________ | 이번 L: ________ | 다음 동기화: ________
```

## 정본 원칙

- 구현은 orphan branch 또는 독립 저장소 **한 곳**만 정본으로 둔다.
- `42/main`과 `guides/main`은 색인·정책·라이선스만 소유한다.
- 이 임시 저장소의 문서와 최종 저장소 문서를 병렬 수정하지 않는다.
- 채용 공고 전문·로고·교육기관 원문은 복제하지 않는다.
- 개인 연락처·주소·식별정보·인증정보는 커밋하지 않는다.

## 생성·검사·패키징

```sh
make build
make check
make package
```

| 명령 | 수행 내용 |
|---|---|
| `make build` | 공고 문서와 SVG·PNG 그래프를 정본 데이터에서 재생성 |
| `make check` | 구조·링크·anchor·PATH ID·L ID·공고·workflow·secret·symlink 검사 |
| `make package` | 결정론적 ZIP, 내부 `MANIFEST.sha256`, 외부 ZIP SHA-256 생성 |

검사기는 네트워크에 의존하지 않는다. 외부 공고 상태는 정적 스냅숏이므로 실제 지원 직전에 원문을 다시 확인해야 한다.

## 라이선스

직접 작성한 문서·도식은 CC BY 4.0, 코드·스크립트·설정은 MIT License를 따른다. 제3자 자료에는 원 권리자의 조건이 적용된다. 자세한 내용은 [LICENSE.md](LICENSE.md)를 따른다.
