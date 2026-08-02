# 결정 기록

## D01 — 저장소 역할

- **결정:** 저장소 이름은 `engineering-path-review`로 하고 `42`·`guides` 최종 확정을 위한 임시 작업 공간으로 사용한다.
- **결과:** 구현 코드를 두지 않으며 최종 이전 뒤 read-only archive로 전환한다.

## D02 — 레인 모델

- **결정:** `P`와 `G`는 선형 spine, `L`은 트리거 기반 한정 작업 큐다.
- **결과:** L01~L15에 진입 조건·한 회차 범위·산출물·반복 여부를 부여한다.

## D03 — 42 정본

- **결정:** 작은·단일 개념 과제 8개는 `42` orphan branch, 독립 제품 6개는 standalone 저장소로 둔다.
- **결과:** 동일 코드 복제를 금지하고 `42/main`은 색인만 소유한다.

## D04 — Guides 정본

- **결정:** 가이드 17개는 모두 `guides` orphan branch로 통합한다.
- **결과:** 각 branch가 README·LICENSE·실습·검증·branch-local CI를 자체 소유한다.

## D05 — 첫 지원 시점

- **결정:** P14 `portfolio-site` 공개·production 검증 직후 일반 첫 지원을 시작한다.
- **결과:** P15/P17/P20/P22에서 지원 직군을 순차 확대하고 코딩 테스트는 지원과 병행한다.

## D06 — 채용 공고

- **결정:** 2026-08-03 정적 스냅숏으로만 제공한다.
- **결과:** 공식 페이지 우선, 플랫폼 보조, active/expired 분리, 전문 미복제, 지원 직전 재확인을 요구한다.

## D07 — 라이선스

- **결정:** 직접 작성한 문서·도식은 CC BY 4.0, 코드·스크립트·설정은 MIT로 제공한다.
- **결과:** 제3자 공고·로고·42 원문에는 새 권리를 부여하지 않는다.

## D08 — 보안

- **결정:** 검토 중 private, 공개 전 secret scanning·push protection·private vulnerability reporting·ruleset을 설정한다.
- **결과:** workflow 최소 권한, action full SHA, symlink/secret/path traversal 검사와 결정론적 package manifest를 사용한다.

## 변경 기록 형식

```text
ID:
기존 결정:
변경 이유:
새 결정:
영향 파일:
재검증:
```
