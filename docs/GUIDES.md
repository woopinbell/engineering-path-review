# 가이드 PATH — 필수 15개 + 조건부 2개

가이드 레인은 한 번에 하나만 활성화한다. 아직 시작하지 않은 가이드만 다음 프로젝트 하드 게이트에 맞춰 재정렬할 수 있다.

| ID | branch | 한 줄 역할 | 진입 조건 | 완료 결과 | 직접 여는 장벽 |
|---|---|---|---|---|---|
| G00 | `guide-git` | 작업 공간·commit·원격·충돌·이력 복구를 안전한 개발 절차로 만든다. | 없음 | 임시 저장소에서 branch 게시, merge/rebase, reflog·revert·reset 복구를 재현한다. | 전체 작업 기반 |
| G01 | `guide-c` | C 메모리·소유권·빌드와 POSIX I/O·process·signal·thread를 연결한다. | G00 완료 | 누적 예제의 정상·실패 경로와 C/POSIX 계약을 직접 구현·검증한다. | P01 |
| G02 | `guide-unix-systems` | shell·filesystem·FD·process·memory·permission·socket·service를 실제 환경에서 관찰한다. | G01 완료 | `system-probe`로 실행 계층과 진단 순서를 재현한다. | 후속 시스템 설명 기반 |
| G03 | `guide-cpp` | C++ 객체 수명·값·다형성·예외·generic programming·event loop를 연결한다. | G02 완료 | object model, mini-container, line/HTTP server 실습을 C++98로 검증한다. | P07 |
| G04 | `guide-operating-systems` | kernel 상태·정책·불변식으로 scheduling·sync·VM·filesystem·I/O를 설명한다. | G03 완료 | C 예제와 결정적 kernel model의 전체 검증을 통과한다. | OS 연결 감사 |
| G05 | `guide-algorithms` | 문제 계약·정확성·복잡도·자료구조·그래프·DP·문자열·유량을 검증한다. | G04 완료 | 기준 풀이·반례·동치 검사로 핵심 유형을 제한 시간 안에 구현한다. | 코딩 테스트 레인 |
| G06 | `guide-computer-architecture` | ISA·pipeline·cache·TLB·OoO·SIMD·multicore의 비용 모델을 연결한다. | G05 완료 | processor model과 C 관찰 예제로 성능 주장의 경계를 검증한다. | 구조 연결 감사 |
| G07 | `guide-computer-networks` | Ethernet부터 IP·routing·TCP·DNS·HTTP·TLS·QUIC까지 종단 경로를 설명한다. | G06 완료 | protocol inspector와 packet/routing 실습으로 상태·재전송·경로를 검증한다. | 네트워크 연결 감사 |
| G08 | `guide-web-infrastructure` | request·container·Compose·TLS·DB lifecycle·bootstrap·recovery를 실습한다. | G07 완료 | 작은 웹 스택의 build·영속성·장애 진단·복구 검증을 통과한다. | P12 |
| G09 | `guide-web-applications` | browser·React·Next·Fastify·PostgreSQL·auth·WebSocket을 한 서비스로 연결한다. | G08 완료 | 협업 보드의 UI·API·DB·실시간·테스트 경계를 구현한다. | P14 일부 |
| G10 | `guide-frontend-react-nextjs` | URL·server/client state·비동기 효과·접근성·성능·배포 판단을 심화한다. | G09 완료 | 프로젝트 목록 실습의 typecheck·build·browser gate를 통과한다. | P14 완전 개방 |
| G11 | `guide-database-systems` | 관계·page·index·buffer·transaction·MVCC·WAL·query plan을 DBMS 관점에서 연결한다. | G10 완료 | 다섯 상태 모델 실습과 선택 PostgreSQL 실험의 경계를 설명한다. | P15 |
| G12 | `guide-java` | Java 17·JVM·domain type·collection·numeric·concurrency·Maven·test를 정리한다. | G11 완료 | 값 객체·동시성·executor·multi-repo Maven·effect test를 검증한다. | P16 |
| G13 | `guide-backend-spring-boot` | Spring runtime·HTTP·JPA·Flyway·Redis·Kafka·Outbox·resilience·observability를 구현한다. | G12 완료 | Testcontainers 기반의 application·locking·idempotency·Kafka·HTTP 실습을 통과한다. | P17 |
| G14 | `guide-distributed-services` | service boundary·idempotency·Saga·event order·retry·release·chaos 근거를 정리한다. | G13 완료 | 중복·역순·계약 drift·broker 장애·release manifest를 재현한다. | P20 |

## 조건부 branch

| branch | 사용할 조건 | 완료 결과 |
|---|---|---|
| `guide-python` | Python 상태 모델·CLI·테스트 도구를 독립 수정하기 어렵다. | 객체·collection·file·subprocess·test runner를 직접 구현하고 관련 CS 실습을 수정할 수 있다. |
| `guide-shell-scripting` | 여러 저장소 검사, 컨테이너 초기화, CI entrypoint와 cleanup을 직접 수정한다. | POSIX `sh`/Bash 경계, quoting, 부분 실패, 임시 자원과 multi-target 자동화를 검증한다. |

## 저장소 위치

17개 가이드는 모두 `guides` 저장소의 서로 공통 조상이 없는 orphan branch에 둔다. 별도 가이드 정본 저장소는 운영하지 않는다.
