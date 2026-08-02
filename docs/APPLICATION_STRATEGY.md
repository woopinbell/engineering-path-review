# 채용 지원 전략

## 판정 전제

```text
컴퓨터공학 학사
42 과정 수료
병역 만기 전역
입사 시점 제한 없음
해외근무 결격사유 없음
영어 업무 능력은 약한 편
각 PATH 마일스톤까지의 프로젝트를 실제 완료·검증·공개한 상태
```

코딩 테스트와 인터뷰의 완성은 첫 지원의 선행 완료 조건으로 두지 않는다. 지원 뒤 생기는 대기 기간에 `L` 레인으로 계속 보완한다.

## 첫 지원 시점

> **`P14 portfolio-site`를 production 검증·실제 배포까지 완료한 직후 첫 일반 지원을 시작한다.**

`P15`나 전체 PATH가 끝날 때까지 기다리지 않는다. 지원과 동시에 다음 프로젝트, 코딩 테스트, 인터뷰 회고를 계속한다.

`P11` 직후에는 C·C++ 시스템·네트워크 직무와 직접 맞는 공고만 제한적으로 먼저 지원할 수 있다.

## 지원 파동

| 파동 | 시작점 | 추가하는 공고 | 대표 증거 |
|---|---|---|---|
| 0 | `P11` | C·C++ 시스템, Linux·POSIX, 네트워크 서버 | `irc-relay-server`, `ray-scene-tracer`, `small-shell`, `thread-dining` |
| 1 | `P14` | React·Next.js 프런트엔드, 일반 웹, 주니어 소프트웨어 | `portfolio-site`, `web-boundary-inspector`, `container-stack` |
| 2 | `P15` | 풀스택, Node.js·TypeScript 백엔드, WebSocket 서비스 | `pong-pong`, `portfolio-site` |
| 3 | `P17` | Java·Spring Boot·JPA·PostgreSQL 백엔드 | `sportsbook-wallet-service`, `pong-pong` |
| 4 | `P20` | Kafka·Redis·Outbox·분산 멱등성·복구 workflow | `sportsbook-betting-service`, `wallet`, `risk`, `odds-feed` |
| 5 | `P22` | 인증·routing·API edge·실시간 전달을 포함한 일반 소프트웨어 | `sportsbook-gateway`, `sportsbook-settlement-service` |

P24까지의 전체 통합은 지원 시작점이 아니라 후속 면접과 더 넓은 공고에서 사용할 강화 근거다.

## 공고 등급

| 등급 | 판단 |
|---|---|
| 즉시 지원 | 해당 마일스톤에서 핵심 필수 요건을 직접 증명하며 명시적 경력 장벽이 낮다. |
| 조건부 지원 | 1~3년 또는 운영 경험을 요구하지만 프로젝트·문서·검증으로 대체 설명할 수 있다. |
| 향후 지원 | 영어, AI·가속기·현장 배포 등 PATH 밖의 핵심 장벽이 남아 있다. |

현재 공고별 판정은 [2026-08-03 정적 스냅숏](JOBS_2026-08-03.md)을 사용한다.

## 첫 지원 전 최소 준비

```text
portfolio-site 공개 URL과 production build 증거
한 장 이력서
직군별 대표 저장소 3~4개
대표 프로젝트 2개를 5분씩 설명할 수 있는 상태
제한 시간 혼합 코딩 테스트 최소 1회
자기소개·지원 이유·실패와 복구 사례의 기본 답변
```

코딩 테스트 6회 목표와 전체 인터뷰 질문 정리는 지원 이후 계속 채운다.

## 지원 운영

```text
지원 5~10건
→ 서류·과제·면접 반응 기록
→ 반복 탈락 원인을 기술·서류·직무 불일치로 분류
→ P/G/L 중 하나의 종료 가능한 수정만 수행
→ 다음 지원 묶음
```

최선호 기업을 첫 묶음에서 모두 소진하지 않는다. 같은 회사의 동일 공고는 1회만 기록하고, 재지원 제한을 원문에서 확인한다.

## 직군별 GitHub 상단 배치

| 직군 | 고정 우선순위 |
|---|---|
| 프런트엔드 | `portfolio-site` → `web-boundary-inspector` → `pong-pong` |
| 풀스택·Node | `pong-pong` → `web-boundary-inspector` → `container-stack` |
| Java·Spring | `sportsbook-wallet-service` → `betting-service` → `pong-pong` |
| C·C++ 시스템 | `irc-relay-server` → `ray-scene-tracer` → `small-shell` → `stl-container` |
| 일반 주니어 | 지원 공고의 주 스택에 맞춰 위 조합 중 3~4개만 선택 |

독립 저장소 수와 GitHub pinned repository 수를 같게 만들 필요는 없다.

## 영어가 약한 상태의 해외 원격

해외 원격을 검색 범위에 포함하지만 전문적인 영어 말하기·쓰기가 필수인 공고는 기술 적합성과 별도로 `향후 지원`으로 둔다. 우선순위는 국내 공고가 앞선다.
