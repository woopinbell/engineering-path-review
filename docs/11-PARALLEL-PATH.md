# 복습용 C·C++·WEB 3트랙 병렬 PATH

이 문서는 [기본 선형·병렬 PATH](01-PATH.md)를 대체하지 않는 **복습·재구현 전용 가속 실행 모드**다. 이미 42 과정을 수료했고 핵심 개념을 한 번 학습했다는 전제에서, C·C++·WEB 프로젝트를 세 개의 독립 트랙으로 병렬 진행한다.

가이드도 저장소 전체를 한 번에 끝내지 않는다. 현재 프로젝트에 필요한 장·실습을 **의존성이 닫힌 개념 패킷**으로 선택해 완료한다.

> 이 문서의 “체리피킹”은 Git의 `cherry-pick` 명령이 아니다. 가이드 branch의 commit을 옮기는 작업이 아니라, 가이드 내부의 장·실습 묶음을 필요한 시점에 선택해 복습하는 운영 방식이다.

## 이 모드를 선택하는 조건

다음 조건을 모두 충족할 때 사용한다.

- C 메모리·포인터·소유권의 기본 모델을 설명할 수 있다.
- C++ 객체 수명·복사·예외의 기본 모델을 설명할 수 있다.
- browser·HTTP·JavaScript/TypeScript·React의 기본 용어를 기억한다.
- 같은 기간에 프로젝트 세 개를 유지해도 검증과 기록이 흐려지지 않는다.
- 기억이 불확실한 개념을 `VERIFIED`로 추정하지 않고 `MISSING`으로 표시할 수 있다.

위 조건이 깨지거나 같은 실패를 반복하면 [기본 PATH](01-PATH.md)로 돌아간다.

## 실행 그래프

[전체 SVG](../assets/path/parallel-path.svg) · [전체 PNG](../assets/path/parallel-path.png) · [Mermaid](../assets/path/parallel-path.mmd) · [Graphviz DOT](../assets/path/parallel-path.dot) · [텍스트](../assets/path/parallel-path.txt) · [가이드 패킷 SVG](../assets/path/parallel-guide-packets.svg)

![복습용 3트랙 병렬 PATH](../assets/path/parallel-path.svg)

## 핵심 운영 규칙

| 단위 | 원자성 | 동시에 활성화할 수 있는 수 | 이동 조건 |
|---|---|---:|---|
| C 프로젝트 트랙 | 프로젝트 단위 | 1개 | 구현·정상/실패 검증·완료 근거·P0/P1 확인 완료 |
| C++ 프로젝트 트랙 | 프로젝트 단위 | 1개 | 구현·정상/실패 검증·완료 근거·P0/P1 확인 완료 |
| WEB 프로젝트 트랙 | 프로젝트 단위 | 1개 | 구현·정상/실패 검증·완료 근거·P0/P1 확인 완료 |
| 가이드 풀 | 개념 패킷 단위 | 활성 프로젝트별 1개 이하 | 패킷의 선행·본문·실습·증거가 닫힘 |
| L 작업 큐 | 한 회차 단위 | 1회 | 지정 trigger·산출물·종료 조건 충족 |

프로젝트가 가이드 패킷 때문에 막히면 같은 트랙의 다음 프로젝트를 열지 않는다. 필요한 패킷을 완료한 뒤 현재 프로젝트로 돌아간다.

```text
C 현재 프로젝트: ________
C++ 현재 프로젝트: ________
WEB 현재 프로젝트: ________
활성 가이드 패킷: ________ / ________ / ________
이번 L: ________
다음 합류 장벽: ________
```

## 가이드 패킷 상태

| 상태 | 의미 | 프로젝트 진입에 사용 가능 |
|---|---|---|
| `DONE` | 지정 본문·실습·검사를 이번 복습에서 다시 완료 | 가능 |
| `VERIFIED` | 기억 점검과 프로젝트·실습 증거로 같은 계약을 재검증 | 가능 |
| `DEFERRED` | 특정 장벽 전까지 의도적으로 연기 | 불가능 |
| `MISSING` | 아직 근거가 없음 | 불가능 |
| `N/A` | 최종 범위 밖임을 근거와 함께 확정 | 해당 요구에만 적용 |

`VERIFIED`는 단순히 “기억난다”는 표시가 아니다. 다음 세 조건을 모두 만족해야 한다.

1. 상태·소유권·실패·검증 한계를 자료 없이 설명한다.
2. 관련 실습 또는 현재 프로젝트의 좁은 검사를 실행한다.
3. 결과를 패킷 ledger에 경로·명령·결론으로 기록한다.

## 프로젝트 트랙

### C 트랙

```text
P01 c-foundation
→ P02 buffered-line-reader
→ P03 format-printer
→ P04 signal-message-bus
→ P05 small-shell
→ P06 thread-dining
```

| 프로젝트 | 한 줄 역할 | 진입 패킷 | 완료 전 패킷 | 완료 결과 |
|---|---|---|---|---|
| P01 `c-foundation` | 바이트·포인터·소유권·부분 실패를 정적 라이브러리에 고정 | `GG-WORKSPACE`, `GC-BASE` | `GC-IO` | API·rollback·부분 `write`·배포 검증 재현 |
| P02 `buffered-line-reader` | 호출 사이 입력 상태와 FD별 context 수명 구현 | P01, `GC-IO`, `GU-BASE` | 없음 | `LINE/EOF/AGAIN/ERROR`, remainder·reset 검증 |
| P03 `format-printer` | 가변 인자와 포맷 문법을 출력 계약으로 변환 | P02, `GC-FORMAT` | `GC-IO` | parser·길이·부분 출력·`EINTR/EPIPE` 검증 |
| P04 `signal-message-bus` | handler와 main 문맥을 분리한 IPC 상태 머신 구현 | P03, `GC-SIGNAL`, `GU-PROCESS` | 없음 | self-pipe·session·ACK·확정 모호성 검증 |
| P05 `small-shell` | 문법을 프로세스·FD 그래프로 실행 | P04, `GC-PROCESS`, `GU-PROCESS` | `GOS-PROCESS` | lexer/parser·pipeline·builtin·redirection·status 검증 |
| P06 `thread-dining` | 공유 주소 공간의 동기화·종료·파괴 수명 구현 | P05, `GC-THREAD`, `GOS-CONCURRENCY` | 없음 | barrier·잠금 순서·terminal state·join/destroy 검증 |

#### C 교차 프로젝트

P09 `stack-sort`는 구현 언어와 직접 선행 기준상 C 트랙 작업이다. 기존 P 번호는 유지하되 C 트랙의 빈 슬롯에서 실행한다.

```text
진입:
P01 + GA-CORE

권장 배치:
P06 완료 뒤
또는 C 트랙이 먼저 비고 GA-CORE가 닫힌 시점

최종 폐쇄:
P08 stl-container + P10 ray-scene-tracer + GA-CORE/GA-TREE와 알고리즘 연결 감사
```

P08 완료를 P09의 **시작 조건**으로 사용하지 않는다. 자료구조 불변식·복잡도·독립 oracle을 대조하는 최종 감사 조건으로 사용한다.

### C++ 트랙

```text
P07 cpp-foundation
→ P08 stl-container
→ P10 ray-scene-tracer
→ P11 irc-relay-server
```

| 프로젝트 | 한 줄 역할 | 진입 패킷 | 완료 전 패킷 | 완료 결과 |
|---|---|---|---|---|
| P07 `cpp-foundation` | 객체 수명·값 의미론·다형성·예외 계약 확립 | `GC-BASE`가 `DONE/VERIFIED`, `GCPP-OBJECT` | 없음 | 깊은 복사·factory·예외 안전성·template 입문 검증 |
| P08 `stl-container` | raw storage 안의 container·iterator·RB-tree 구현 | P07, `GCPP-GENERIC` | `GA-TREE` | allocator·무효화·예외·복잡도·차등 검사 통과 |
| P10 `ray-scene-tracer` | BVH와 결정적 병렬 렌더링 구현 | P08, `GA-CORE`, `GCA-MEMORY` | `GCA-PARALLEL` | linear/BVH 동치·shading·tile checksum 검증 |
| P11 `irc-relay-server` | 논블로킹 연결을 portable event loop로 관리 | P07, `GCPP-NET`, `GNET-TRANSPORT` | `GU-SERVICE` | framing·partial I/O·backpressure·timeout·shutdown 검증 |

P11은 P10의 코드나 산출물에 의존하지 않는다. 한 트랙에서 프로젝트 하나만 활성화한다는 운영 규칙 때문에 위 순서를 기본으로 사용하지만, P07과 필요한 패킷이 닫혔다면 P10과 P11의 순서를 교환할 수 있다.

### WEB 트랙

```text
P12 container-stack
→ P13 web-boundary-inspector
→ P14 portfolio-site
→ P15 pong-pong
```

| 프로젝트 | 한 줄 역할 | 진입 패킷 | 완료 전 패킷 | 완료 결과 |
|---|---|---|---|---|
| P12 `container-stack` | 웹 스택 초기화·영속성·복구를 운영 절차로 구현 | `GWI-RUNTIME` | `GWI-STATE`, `GWI-OPS` | TLS·bootstrap·readiness·backup/restore·rotation 검증 |
| P13 `web-boundary-inspector` | HTTP proxy와 browser runtime의 상태·정책 경계 관찰 | P12, `GWEB-RUNTIME`, `GWEB-SECURITY`, `GNET-WEB` | 없음 | request·DOM·Fetch·History·storage·CORS/CSP 검증 |
| P14 `portfolio-site` | 콘텐츠를 Next.js renderer와 배포 gate로 표현 | P13, `GFRONT-RUNTIME`, `GFRONT-ARCH` | `GFRONT-QUALITY`, `GWEB-QUALITY` | 공개 production build·접근성·성능 근거 확보 |
| P15 `pong-pong` | browser·API·DB·WebSocket을 서버 권위 서비스로 통합 | P12~P14, `GWEB-API-DB`, `GWEB-SECURITY`, `GWEB-REALTIME`, `GDB-RELATIONAL`, `GDB-TX` | `GDB-QUERY`는 DB 감사 전 | session·room·scheduler·reconnect·transaction·배포 검증 |

기본 PATH의 P11→P12는 이 모드에서 시작 장벽으로 사용하지 않는다. C/C++ 프로젝트의 process·FD·event-loop 문서는 WEB 문서가 재사용하는 비교 근거지만, P12의 build/runtime 직접 의존성은 아니다. 대신 시스템·네트워크 연결 감사 전까지 관련 패킷과 프로젝트를 완료한다.

## 트랙 간 의존성

| 방향 | 강도 | 이 모드의 처리 |
|---|---:|---|
| C → C++ | 기초 개념은 중간, 프로젝트 의존은 약함 | `GC-BASE`를 `DONE/VERIFIED`하면 P07 시작 가능 |
| C → WEB | 약함 | process·FD·signal은 시작 gate가 아니라 시스템 감사에서 대조 |
| C++ → WEB | 약함~중간 | 객체 수명·event loop·partial I/O는 시작 gate가 아니라 네트워크 감사에서 대조 |
| WEB → C/C++ | 거의 없음 | 별도 시작 gate를 만들지 않음 |
| WEB 내부 → P15 | 강함 | P12~P14와 DB·auth·realtime 패킷을 실제 hard gate로 유지 |

## 합류 장벽

### B1 — 시스템·네트워크 폐쇄 감사

```text
대상:
P05 small-shell
P06 thread-dining
P11 irc-relay-server
P12 container-stack
P13 web-boundary-inspector

필수 패킷:
GU-PROCESS
GU-SERVICE
GOS-PROCESS
GOS-CONCURRENCY
GNET-TRANSPORT
GNET-WEB
```

확인 범위는 process/thread, FD/socket, readiness, partial I/O, signal, cancellation, graceful shutdown이다. 이 장벽은 프로젝트 시작을 막지 않고 관련 문서의 최종 확정을 막는다.

연결되는 L 작업은 L04, L05, L06, L08이다.

### B2 — 알고리즘·구조 폐쇄 감사

```text
대상:
P09 stack-sort
P08 stl-container
P10 ray-scene-tracer

필수 패킷:
GA-CORE
GA-TREE
GCA-MEMORY
GCA-PARALLEL
```

정확성 불변식, 논리 연산 수와 실제 자료 표현 비용, tree/BVH, cache·data layout, 차등 검사와 oracle 한계를 대조한다.

연결되는 L 작업은 L07과 L09이다.

### B3 — WEB 종합 프로젝트 진입 장벽

```text
P12 + P13 + P14
+ GWEB-API-DB
+ GWEB-SECURITY
+ GWEB-REALTIME
+ GDB-RELATIONAL
+ GDB-TX
→ P15 pong-pong
```

이 장벽은 실제 hard gate다. 다른 두 장벽과 달리 비교 감사가 아니라 WEB04의 구현 입력을 구성한다.

### B4 — 전체 가이드 폐쇄

세 트랙의 프로젝트가 끝난 뒤 필수 가이드 범위의 모든 패킷은 `DONE`, `VERIFIED`, `N/A` 중 하나여야 한다. `DEFERRED`와 `MISSING`이 남으면 이 모드의 전체 완료가 아니다.

## 가이드 패킷 카탈로그

아래 장 범위는 각 guide branch의 번호 체계를 따른다. 누적 실습은 중간 단계부터 적용하지 않고 해당 실습의 선행 단계를 순서대로 수행한다.

### 작업 기반·C·Unix

| 패킷 | 원본 범위 | 한 줄 역할 | 완료 결과 |
|---|---|---|---|
| `GG-WORKSPACE` | `guide-git` 01~02 | 작업 공간·branch·diff·commit 경계 고정 | 안전한 작업 시작과 목적별 commit 가능 |
| `GG-INTEGRATION` | `guide-git` 03~04 | remote·PR·merge/rebase·conflict 처리 | 통합 방식 선택과 충돌 복구 가능 |
| `GG-RECOVERY` | `guide-git` 05~06 | reflog·revert·reset·외부 기여 복구 | 잘못된 변경과 이력 이동 복구 가능 |
| `GC-BASE` | `guide-c` 01~04 | 프로그램·메모리·소유권·빌드·테스트 | P01/P07 공통 기초를 설명·검증 |
| `GC-FORMAT` | `guide-c` 05 | 가변 인자와 형식 기반 API | P03 인자·문법·길이 계약 검증 |
| `GC-IO` | `guide-c` 06 | POSIX I/O·부분 read/write·record stream | P01~P03의 I/O 실패 경계 검증 |
| `GC-PROCESS` | `guide-c` 07·09 | process·FD·pipe·parser/executor | P05 실행 그래프 설명 가능 |
| `GC-SIGNAL` | `guide-c` 08 | signal·비동기 사건·handler 경계 | P04 handler/main 분리 검증 |
| `GC-THREAD` | `guide-c` 10 | pthread·동기화·시간 | P06 thread 수명과 시간 계약 검증 |
| `GU-BASE` | `guide-unix-systems` 01~03 | terminal·path·stream·FD 관찰 | 사용자 공간 I/O 증거 수집 가능 |
| `GU-PROCESS` | `guide-unix-systems` 04~06 | process/thread/signal·memory·권한 | P04~P06 실행 문맥 대조 가능 |
| `GU-SERVICE` | `guide-unix-systems` 07~09 | socket·service·log·진단 | P11~P13 runtime 장애 경로 추적 가능 |

### C++·운영체제·알고리즘·컴퓨터구조

| 패킷 | 원본 범위 | 한 줄 역할 | 완료 결과 |
|---|---|---|---|
| `GCPP-OBJECT` | `guide-cpp` 01~05 | 타입·객체 수명·책임·다형성·오류 | P07 객체·예외 계약 검증 |
| `GCPP-GENERIC` | `guide-cpp` 06~07 | template·iterator·STL 문제 해결 | P08 generic contract 진입 가능 |
| `GCPP-NET` | `guide-cpp` 08~09 | POSIX socket·event loop·HTTP 책임 | P11 객체·I/O 수명 진입 가능 |
| `GOS-PROCESS` | `guide-operating-systems` 01~03 | kernel 경계·process·scheduler | P05와 runtime 상태 대조 가능 |
| `GOS-CONCURRENCY` | `guide-operating-systems` 04~06 | atomicity·동기화·deadlock·progress | P06 불변식·진행 보장 검증 |
| `GOS-MEMORY-STORAGE` | `guide-operating-systems` 07~10 | VM·paging·filesystem·device I/O | 시스템 감사의 memory/storage 범위 폐쇄 |
| `GA-CORE` | `guide-algorithms` 01~10 | 문제 계약·기본 자료구조·복잡도·정렬·상환 | P09/P10과 L01 코딩 테스트 개방 |
| `GA-TREE` | `guide-algorithms` 11 | BST·red-black tree 불변식 | P08 tree 구조·복잡도 검증 |
| `GA-ADVANCED` | `guide-algorithms` 12~16 | graph·shortest path·string·reduction·flow | 전체 알고리즘 범위 폐쇄 |
| `GCA-EXECUTION` | `guide-computer-architecture` 01~05 | 표현·ISA·성능식·pipeline | 명령 실행 비용 설명 가능 |
| `GCA-MEMORY` | `guide-computer-architecture` 06~07 | cache·locality·TLB·VM | P08/P10 data layout 비용 대조 가능 |
| `GCA-PARALLEL` | `guide-computer-architecture` 08~10 | OoO·SIMD·multicore·coherence | P10 병렬 결정성과 성능 한계 검증 |

### 네트워크·웹·프런트엔드·데이터베이스

| 패킷 | 원본 범위 | 한 줄 역할 | 완료 결과 |
|---|---|---|---|
| `GNET-PATH` | `guide-computer-networks` 01~07 | link·IP·routing·middlebox 경로 | packet 경로와 실패 위치 설명 가능 |
| `GNET-TRANSPORT` | `guide-computer-networks` 08~11 | UDP/TCP·state·retransmission·flow/congestion | P11 stream·연결·backpressure 검증 |
| `GNET-WEB` | `guide-computer-networks` 12 | DNS·HTTP·TLS·QUIC 연결 | P12/P13 application 경계 검증 |
| `GWI-RUNTIME` | `guide-web-infrastructure` 01~04 | request·container·Compose·Nginx/TLS | P12 초기 runtime 진입 가능 |
| `GWI-STATE` | `guide-web-infrastructure` 05~06 | DB lifecycle·멱등 bootstrap | P12 persistent state 검증 |
| `GWI-OPS` | `guide-web-infrastructure` 07 | 장애 진단·backup·restore | P12 운영 완료 근거 확보 |
| `GWEB-RUNTIME` | `guide-web-applications` 00~03 | JS/TS·browser·React/Next runtime | P13/P14 화면·실행 경계 진입 가능 |
| `GWEB-API-DB` | `guide-web-applications` 04~05 | HTTP API·runtime validation·PostgreSQL | P15 API/DB 수직 기능 진입 가능 |
| `GWEB-SECURITY` | `guide-web-applications` 06 | cookie·authorization·CORS·CSRF·XSS | P13/P15 browser/API 보안 경계 검증 |
| `GWEB-REALTIME` | `guide-web-applications` 07 | WebSocket·snapshot·reconnect·conflict | P15 실시간 상태 진입 가능 |
| `GWEB-QUALITY` | `guide-web-applications` 08~09 | test 계층·종합 요구사항 | P14/P15 품질 gate 폐쇄 |
| `GFRONT-RUNTIME` | `guide-frontend-react-nextjs` 00~01 | browser/React/App Router 최소 모델 | P14 첫 수직 기능 진입 가능 |
| `GFRONT-ARCH` | `guide-frontend-react-nextjs` 02~03 | component·state·data·effect 경계 | P14 renderer/client island 설계 가능 |
| `GFRONT-QUALITY` | `guide-frontend-react-nextjs` 04 | 접근성·성능·build·배포 | P14 공개 완료 근거 확보 |
| `GDB-RELATIONAL` | `guide-database-systems` 01~03 | 관계·SQL·schema·constraint | P15 데이터 모델 진입 가능 |
| `GDB-STORAGE` | `guide-database-systems` 04~06 | page·record·index·buffer pool | DB 내부 비용 설명 가능 |
| `GDB-TX` | `guide-database-systems` 07~08 | transaction·isolation·MVCC·WAL | P15 동시 수정·복구 경계 검증 |
| `GDB-QUERY` | `guide-database-systems` 09~12 | join·cost·tuning·review | DB 연결 감사 폐쇄 |

### 조건부 지원 패킷

| 패킷 | 원본 범위 | 사용하는 조건 | 완료 결과 |
|---|---|---|---|
| `GPY-BASE` | `guide-python` 01~03 | Python 상태 모델의 타입·collection 수정이 어려움 | 기본 Python 구현을 독립 수정 가능 |
| `GPY-AUTOMATION` | `guide-python` 04~08 | CLI·subprocess·test harness를 수정해야 함 | CS 실습·자동화의 실패를 직접 진단 가능 |
| `GSH-CORE` | `guide-shell-scripting` 01~04 | 여러 저장소·명령 조합 자동화가 어려움 | quoting·status·loop·부분 실패 처리 가능 |
| `GSH-ROBUST` | `guide-shell-scripting` 05~08 | release·검사·정리 script를 작성함 | interface·trap·이식성·검증 계약 확보 |

## 가이드 패킷 선택 그래프

[SVG](../assets/path/parallel-guide-packets.svg) · [PNG](../assets/path/parallel-guide-packets.png) · [Mermaid](../assets/path/parallel-guide-packets.mmd) · [Graphviz DOT](../assets/path/parallel-guide-packets.dot) · [텍스트](../assets/path/parallel-guide-packets.txt)

![가이드 패킷 선택 구조](../assets/path/parallel-guide-packets.svg)

## 패킷 선택 규칙

1. 뒤 장이 앞 장의 상태 모델과 용어를 요구하면 하나의 패킷으로 묶거나 `requires`를 기록한다.
2. 누적 실습의 patch·stage는 중간부터 적용하지 않는다.
3. 현재 프로젝트 진입에 필요한 패킷만 먼저 닫고 나머지는 `DEFERRED`로 둔다.
4. 프로젝트에서 문제가 드러나면 현재 패킷을 확장하되 다른 가이드로 무작위 이동하지 않는다.
5. 최종 완료 전에는 필수 범위의 `DEFERRED`와 `MISSING`을 모두 해소한다.

권장 ledger 형식은 다음과 같다.

```yaml
packet: GNET-TRANSPORT
status: VERIFIED
requires:
  - GU-SERVICE
used_by:
  - P11
  - P13
evidence:
  - command: make event-test
  - path: irc-relay-server/tests
  - conclusion: partial read/write와 EAGAIN 상태를 재현함
next_review: B1
```

## L 작업 큐와 채용 마일스톤

- `GA-CORE`가 닫히면 G05 전체 완료를 기다리지 않고 L01 코딩 테스트를 열 수 있다.
- B1에서 L04·L05·L06·L08을 필요한 조합으로 한 번씩 수행한다.
- B2에서 L07·L09를 수행한다.
- P14가 공개·production 검증되면 L14 첫 지원 준비를 연다.
- P15 이후의 지원 파동과 P16~P24는 [기본 PATH](01-PATH.md)와 [채용 지원 전략](04-APPLICATION-STRATEGY.md)을 따른다.

P14 시점에 C/C++ 트랙이 미완료여도 일반 WEB 지원을 시작할 수 있다. 다만 C/C++ 시스템 직무에 제출할 때는 해당 트랙과 관련 감사를 완료한 증거를 사용한다.

## 실행 예시

### 초기 병렬 상태

```text
C: P01 c-foundation + GC-BASE
C++: P07 cpp-foundation + GCPP-OBJECT
WEB: P12 container-stack + GWI-RUNTIME
L: 비활성
```

C++ 트랙의 `GC-BASE`가 이미 기억 점검과 좁은 실습으로 `VERIFIED`된 경우에만 위 조합을 사용한다. 그렇지 않으면 C++ 트랙은 `GC-BASE`가 닫힐 때까지 비운다.

### 중간 병렬 상태

```text
C: P04 signal-message-bus + GC-SIGNAL
C++: P08 stl-container + GCPP-GENERIC / GA-TREE
WEB: P13 web-boundary-inspector + GWEB-SECURITY / GNET-WEB
L: L01 코딩 테스트 한 회차
```

L을 수행하는 날에도 세 프로젝트의 완료 기준을 낮추지 않는다. 작업량이 과하면 L을 닫고 프로젝트 세 트랙을 우선한다.

### 합류 전 상태

```text
C: P09 stack-sort 완료
C++: P10 ray-scene-tracer 완료
WEB: P14 portfolio-site 공개 완료

B2 알고리즘·구조 감사
L14 첫 지원 준비
WEB은 B3 패킷을 닫은 뒤 P15 진입
```

## 완료 기준

이 대체 PATH의 3트랙 구간은 다음을 모두 만족하면 끝난다.

```text
C:
P01~P06 + P09 완료

C++:
P07 + P08 + P10 + P11 완료

WEB:
P12~P15 완료

Guide packets:
필수 범위가 DONE / VERIFIED / N/A
DEFERRED / MISSING 0개

Barriers:
B1 시스템·네트워크 감사 완료
B2 알고리즘·구조 감사 완료
B3 WEB 종합 진입·P15 완료
P0·P1 해결
```

P16~P24 Java·Spring·스포츠북 구간은 이 문서에서 재배치하지 않는다. 3트랙 합류 뒤 [기본 PATH](01-PATH.md)의 P16부터 이어서 진행한다.

## 기본 PATH로 복귀하는 조건

다음 중 하나가 반복되면 가속 모드를 중단한다.

- 같은 트랙에서 현재 프로젝트를 두고 다음 프로젝트를 열었다.
- `VERIFIED` 패킷의 설명과 실제 코드가 반복해서 모순된다.
- 세 프로젝트의 failure evidence와 문서 기록이 누락된다.
- 공유 패킷 하나 때문에 두 개 이상의 트랙이 장기간 재작업한다.
- 링크·개념 소유권·완료 상태가 어느 저장소의 정본인지 불명확해진다.

복귀할 때 완료한 프로젝트와 패킷의 증거는 유지한다. 미완료 트랙만 [기본 선형·병렬 PATH](01-PATH.md)의 다음 하드 게이트에 맞춰 재배치한다.
