# C·C++·WEB 3트랙 병렬 PATH

이 문서는 42 과정을 한 번 수료한 뒤 프로젝트와 가이드를 다시 구현·복습할 때 사용하는 실행안이다. C, C++, WEB을 세 개의 병렬 트랙으로 진행하되, **각 트랙 안에서 G와 P를 선형으로 교차 배치한다.**

> **프로젝트만 원자적으로 완료한다. 가이드는 저장소 전체의 원자성을 해제해 필요한 장·실습을 시점별로 나누어 진행하지만, 필수 범위는 생략하지 않고 최종적으로 모두 이수한다.**

여기서 “체리피킹”은 Git의 `cherry-pick`이 아니다. 가이드의 commit을 옮기는 작업이 아니라, 가이드 내부의 장과 실습을 현재 프로젝트에 맞는 시점으로 재배치하는 운영 방식이다.

## 실행 원칙

| 대상 | 실행 규칙 |
|---|---|
| 세 트랙 | C, C++, WEB은 서로 기다리지 않고 동시에 진행할 수 있다. |
| 프로젝트 `P` | 같은 트랙에서 하나만 활성화한다. 시작한 프로젝트는 구현·검증·문서·P0/P1 처리까지 마친 뒤 다음 단계로 이동한다. |
| 가이드 `G` | 필요한 장·실습 구간만 현재 위치에 배치할 수 있다. 선택한 구간의 내부 선행 순서와 누적 실습 순서는 유지한다. |
| 필수 가이드 범위 | “이미 아는 내용”이라는 이유로 제거하지 않는다. 빠르게 복습할 수는 있지만 읽기·실습·검증 범위에서 삭제할 수 없다. |
| 트랙 간 의존성 | 실제 선행 관계만 동기화 장벽으로 둔다. 개념 재사용은 다른 트랙 전체를 기다리게 하지 않는다. |
| `L` 작업 | 코딩 테스트·연결 감사·지원 준비는 세 트랙 밖의 이벤트성 작업 큐다. 상세 규칙은 [L 작업 레인](02-L-LANE.md)을 따른다. |

같은 트랙에서는 다음 순서를 지킨다.

```text
필요한 G 구간 완료
→ P 시작
→ P를 원자적으로 완료
→ 다음 G 구간
→ 다음 P
```

다른 트랙에서는 동시에 다음과 같은 상태가 가능하다.

```text
C TRACK    : G 또는 P 한 단계
C++ TRACK  : G 또는 P 한 단계
WEB TRACK  : G 또는 P 한 단계
```

## 전체 그래프

[SVG](../assets/path/parallel-path.svg) · [PNG](../assets/path/parallel-path.png) · [Mermaid](../assets/path/parallel-path.mmd) · [Graphviz DOT](../assets/path/parallel-path.dot) · [텍스트](../assets/path/parallel-path.txt) · [가이드 커버리지 SVG](../assets/path/parallel-guide-packets.svg)

![C·C++·WEB 3트랙 병렬 PATH](../assets/path/parallel-path.svg)

## 공통 시작점

세 트랙을 열기 전에 `guide-git` 01~06을 완료한다.

```text
G00 guide-git 01~06
→ C TRACK ∥ C++ TRACK ∥ WEB TRACK
```

완료 결과는 다음과 같다.

```text
작업 공간·branch·diff·commit
→ remote·PR·merge/rebase·conflict
→ reflog·revert·reset·외부 기여 복구
```

## C 트랙

```text
C-G01 → P01 → C-G02 → P02 → C-G03 → P03
→ C-G04 → P04 → C-G05 → P05 → C-G06 → P06
→ C-G07 → [C++-G02 동기화] → P09
```

| 순서 | 유형 | 범위 또는 프로젝트 | 역할·진입 조건 | 완료 결과 |
|---:|:---:|---|---|---|
| C-G01 | G | `guide-c` 01~04·06 | 프로그램 모델, 메모리·문자열·소유권, API·빌드·테스트, POSIX I/O를 먼저 복습 | P01의 바이트·할당·rollback·정적 라이브러리·부분 `write`를 설명할 수 있음 |
| P01 | P | `c-foundation` | C-G01 완료 뒤 시작 | 공개 API·소유권·실패 경로·배포 검증을 원자적으로 완료 |
| C-G02 | G | `guide-unix-systems` 01~03 | terminal·path·stream·FD와 부분 입출력을 관찰 | P02의 descriptor·remainder 상태를 운영체제 관점에서 추적 가능 |
| P02 | P | `buffered-line-reader` | P01 + C-G02 | `LINE/EOF/AGAIN/ERROR`, FD별 context, reset·수명 검증 완료 |
| C-G03 | G | `guide-c` 05 | 가변 인자와 형식 기반 API를 복습 | P03의 인자 타입·문법·길이·출력 계약을 설명 가능 |
| P03 | P | `format-printer` | P02 + C-G03 | parser·두 순회·부분 출력·`EINTR/EPIPE` 검증 완료 |
| C-G04 | G | `guide-c` 08 + `guide-unix-systems` 04 | signal, async-signal-safe 처리, process/thread 문맥을 복습 | handler와 main 문맥, signal 전달·상태 전이를 구분 가능 |
| P04 | P | `signal-message-bus` | P03 + C-G04 | self-pipe·session·ACK·출력 확정의 모호성 검증 완료 |
| C-G05 | G | `guide-c` 07·09 + `guide-unix-systems` 05~06 | process·FD·pipe·명령 실행기, memory·권한·환경을 복습 | shell의 parser/executor와 부모·자식·FD 수명을 설명 가능 |
| P05 | P | `small-shell` | P04 + C-G05 | lexer/parser·pipeline·builtin·redirection·종료 상태 검증 완료 |
| C-G06 | G | `guide-c` 10 + `guide-operating-systems` 01~06 | pthread·시간, kernel 경계·scheduler·atomicity·동기화·deadlock을 복습 | 공유 상태 불변식과 진행 보장을 구분 가능 |
| P06 | P | `thread-dining` | P05 + C-G06 | barrier·잠금 순서·terminal state·join/destroy 검증 완료 |
| C-G07 | G | `guide-unix-systems` 07~09 + `guide-operating-systems` 07~10 | socket·service·진단, VM·paging·filesystem·device I/O까지 남은 필수 범위를 완료 | C·Unix·OS 필수 가이드 범위 전체 이수 |
| C-S01 | 동기화 | C++-G02의 `guide-algorithms` 01~10 | P09 시작 전에 알고리즘 기본·분석·정렬·상환 범위가 완료되어야 함 | 트랙 간 실제 의존성 한 곳만 대기 |
| P09 | P | `stack-sort` | P01 + C-G07 + C-S01 | rank·radix·명령 비용·독립 checker/oracle 검증 완료 |

C-G07은 P09의 직접 구현 지식만을 위한 구간이 아니다. 필수인 Unix·운영체제 가이드의 남은 범위를 C 트랙 안에서 빠뜨리지 않고 폐쇄하기 위해 배치한다.

## C++ 트랙

```text
CPP-G01 → P07 → CPP-G02 → P08
→ CPP-G03 → P10 → CPP-G04 → P11
```

| 순서 | 유형 | 범위 또는 프로젝트 | 역할·진입 조건 | 완료 결과 |
|---:|:---:|---|---|---|
| CPP-G01 | G | `guide-cpp` 01~05 | 타입·객체 수명·값 의미론·책임·다형성·오류를 복습 | P07의 복사·소유권·예외 계약을 설명 가능 |
| P07 | P | `cpp-foundation` | CPP-G01 완료 뒤 시작. C 트랙의 기초 개념은 복습 전제이므로 전체 C 트랙 완료를 기다리지 않음 | 깊은 복사·factory·다형성·예외 안전성·template 입문 검증 완료 |
| CPP-G02 | G | `guide-cpp` 06~07 + `guide-algorithms` 01~11 | template·iterator·STL, 문제 해결 루프·기본 자료구조·분석·정렬·상환·RB-tree를 순서대로 완료 | P08과 C 트랙 P09의 알고리즘 선행 범위 확보 |
| P08 | P | `stl-container` | P07 + CPP-G02 | allocator·raw storage·iterator·RB-tree·예외·복잡도·차등 검사 완료 |
| CPP-G03 | G | `guide-algorithms` 12~16 + `guide-computer-architecture` 01~10 | 고급 graph·문자열·환원·flow와 ISA·pipeline·cache·TLB·parallelism을 완료 | 알고리즘·컴퓨터구조 필수 범위 전체 이수, P10 비용·병렬 모델 확보 |
| P10 | P | `ray-scene-tracer` | P08 + CPP-G03 | linear/BVH 동치·shading·tile 병렬성·checksum 검증 완료 |
| CPP-G04 | G | `guide-cpp` 08~09 + `guide-computer-networks` 01~11 | POSIX socket·event loop·HTTP 책임과 link·IP·routing·TCP 상태·재전송·흐름/혼잡 제어를 완료 | C++ 필수 범위 전체 이수, network 12장을 제외한 기반 완료 |
| P11 | P | `irc-relay-server` | P10 + CPP-G04 | framing·partial I/O·backpressure·timeout·portable event loop·shutdown 검증 완료 |

P10과 P11은 코드 의존성이 약하지만 이 PATH에서는 C++ 트랙의 선형성을 위해 위 순서를 고정한다. 순서 최적화가 필요해도 한 프로젝트를 시작한 뒤 다른 프로젝트로 점프하지 않는다.

## WEB 트랙

```text
WEB-G01 → P12 → WEB-G02 → P13
→ WEB-G03 → P14 → [C++-G04 동기화]
→ WEB-G04 → P15
```

| 순서 | 유형 | 범위 또는 프로젝트 | 역할·진입 조건 | 완료 결과 |
|---:|:---:|---|---|---|
| WEB-G01 | G | `guide-web-infrastructure` 01~07 | request·container·Compose·Nginx/TLS·DB lifecycle·bootstrap·운영/복구를 모두 완료 | P12에 필요한 웹 인프라 가이드 전체 이수 |
| P12 | P | `container-stack` | WEB-G01 완료 뒤 시작 | TLS·bootstrap·readiness·영속성·backup/restore·rotation·diagnostics 검증 완료 |
| WEB-G02 | G | `guide-web-applications` 00~06 | JS/TS·browser·React/Next·HTTP API·PostgreSQL·인증/보안을 순서대로 완료 | P13의 HTTP/browser/security 경계와 P14의 runtime 기초 확보 |
| P13 | P | `web-boundary-inspector` | P12 + WEB-G02 | request 변환·DOM·task/microtask·Fetch·History·storage·cookie·CORS/CSP 검증 완료 |
| WEB-G03 | G | `guide-frontend-react-nextjs` 00~04 | browser/React 기초, onboarding, UI·state/data/effect, 접근성·성능·배포를 모두 완료 | P14 프런트엔드 가이드 전체 이수 |
| P14 | P | `portfolio-site` | P13 + WEB-G03 | production build·공개 배포·runtime validation·접근성·성능 근거 확보 |
| WEB-S01 | 동기화 | C++-G04의 `guide-computer-networks` 01~11 | network 12장을 진행하기 전에 앞 장의 전송·경로 범위가 완료되어야 함 | 가이드 내부 순서를 트랙 간에도 보존 |
| WEB-G04 | G | `guide-computer-networks` 12 + `guide-web-applications` 07~09 + `guide-database-systems` 01~12 | DNS·HTTP·TLS·QUIC, WebSocket·테스트·종합 요구사항, 관계·저장·index·transaction·MVCC·WAL·query cost를 완료 | network·web applications·database 필수 범위 전체 이수 |
| P15 | P | `pong-pong` | P12~P14 + WEB-G04 | session·API·DB·WebSocket·room·scheduler·reconnect·transaction·배포 검증 완료 |

WEB 트랙은 P14까지 C/C++ 트랙을 기다리지 않는다. C++-G04와의 동기화는 `guide-computer-networks` 12장의 내부 선행 순서를 보존하기 위해 P15 직전에만 발생한다.

## 트랙 간 의존성

| 연결 | 종류 | 처리 방식 |
|---|---|---|
| C-G01 → CPP-G01 | 개념 재사용 | C 메모리·소유권은 C++ 객체 수명의 기반이지만 복습 과정이므로 C 트랙 전체 완료를 기다리지 않는다. 부족한 항목만 CPP-G01에서 다시 확인한다. |
| CPP-G02 → P09 | 하드 동기화 | `guide-algorithms` 01~10이 끝나야 C 트랙의 `stack-sort`를 시작한다. |
| CPP-G04 → WEB-G04 | 하드 동기화 | `guide-computer-networks` 01~11 뒤에 WEB 트랙에서 12장을 진행한다. |
| P05·P06·P11·P12·P13 | 최종 연결 감사 | process/thread·FD/socket·partial I/O·signal·shutdown을 한 번 대조하되 프로젝트 시작 장벽으로 만들지 않는다. |
| P08·P09·P10 | 최종 연결 감사 | invariant·complexity·tree/BVH·oracle을 한 번 대조한다. |

따라서 세 트랙 사이의 강한 의존성은 두 개뿐이다.

```text
CPP-G02 → P09
CPP-G04 → WEB-G04
```

나머지는 다른 트랙의 시작을 막지 않는 개념 연결 또는 최종 감사다.

## 가이드 체리피킹과 필수 커버리지

[SVG](../assets/path/parallel-guide-packets.svg) · [PNG](../assets/path/parallel-guide-packets.png) · [Mermaid](../assets/path/parallel-guide-packets.mmd) · [Graphviz DOT](../assets/path/parallel-guide-packets.dot) · [텍스트](../assets/path/parallel-guide-packets.txt)

![가이드 체리피킹과 필수 커버리지](../assets/path/parallel-guide-packets.svg)

가이드의 저장소 전체 원자성만 해제한다. 다음 규칙은 해제하지 않는다.

1. 필수 가이드의 모든 지정 장은 PATH 어딘가에 정확히 배치한다.
2. 선택한 구간 안에서 앞 장이 뒤 장의 상태 모델을 정의하면 그 순서를 유지한다.
3. 누적 실습은 중간 stage부터 적용하지 않는다.
4. 한 가이드의 장을 여러 트랙으로 나눈 경우 앞 구간 완료를 뒤 구간의 동기화 조건으로 둔다.
5. 프로젝트 경험이나 기억 점검만으로 필수 장의 이수를 대체하지 않는다.
6. “복습”은 읽기와 실습 속도를 높이는 근거일 뿐, 필수 범위를 삭제하는 근거가 아니다.

## 필수 가이드 커버리지 표

| 필수 가이드 | 배치 위치 | 최종 커버리지 |
|---|---|---|
| `guide-git` | 공통 G00 | 01~06 |
| `guide-c` | C-G01·03·04·05·06 | 01~10 전체 |
| `guide-unix-systems` | C-G02·04·05·07 | 01~09 전체 |
| `guide-operating-systems` | C-G06·07 | 01~10 전체 |
| `guide-cpp` | CPP-G01·02·04 | 01~09 전체 |
| `guide-algorithms` | CPP-G02·03 | 01~16 전체 |
| `guide-computer-architecture` | CPP-G03 | 01~10 전체 |
| `guide-computer-networks` | CPP-G04 + WEB-G04 | 01~12 전체 |
| `guide-web-infrastructure` | WEB-G01 | 01~07 전체 |
| `guide-web-applications` | WEB-G02·04 | 00~09 전체 |
| `guide-frontend-react-nextjs` | WEB-G03 | 00~04 전체 |
| `guide-database-systems` | WEB-G04 | 01~12 전체 |

### 조건부·선택 가이드

- `guide-python`은 Python 기반 CS 상태 모델·CLI·테스트를 독립적으로 수정하기 어렵다면 조건부 필수가 된다. 조건이 성립하면 첫 Python 실습 전에 01~08을 적절한 구간으로 나누어 모두 완료한다.
- `guide-shell-scripting`은 여러 저장소 자동화·검사·release script를 직접 수정하는 범위를 선택했을 때 01~08을 완료한다. 조건이 성립하지 않으면 선택 범위 밖으로 명시한다.

## 현재 위치 기록

```text
C TRACK    : ____________________
C++ TRACK  : ____________________
WEB TRACK  : ____________________
이번 L     : ____________________
다음 동기화: ____________________
```

G 단계는 장 번호까지 기록한다.

```text
예: CPP-G02 / guide-algorithms 08~11 진행 중
```

P 단계는 완료 전까지 다음 G 또는 P로 이동하지 않는다.

## 채용과 L 작업

- P14가 production 배포까지 완료되면 C/C++ 트랙의 종료를 기다리지 않고 첫 일반 WEB 지원을 시작할 수 있다.
- P15 완료 뒤 풀스택·Node.js·TypeScript 백엔드로 지원 범위를 넓힌다.
- C/C++ 시스템 직무는 해당 트랙 프로젝트와 연결 감사가 완료된 범위만 제출 근거로 사용한다.
- 코딩 테스트·연결 감사·지원 준비는 [L 작업 레인](02-L-LANE.md)에서 한 회차씩 열고 닫는다.

## 3트랙 구간 완료 조건

다음을 모두 충족해야 P16 이후 Java·Spring·스포츠북 구간으로 넘어간다.

```text
C TRACK:
P01~P06 + P09 완료

C++ TRACK:
P07 + P08 + P10 + P11 완료

WEB TRACK:
P12~P15 완료

필수 가이드:
커버리지 표의 모든 범위 이수
조건부 가이드는 조건 판정과 결과 기록

연결 감사:
시스템·네트워크 감사 완료
알고리즘·구조 감사 완료
P0·P1 해결
```

P16~P24는 [기본 선형·병렬 PATH](01-PATH.md)의 Java·Spring·스포츠북 순서를 따른다.
