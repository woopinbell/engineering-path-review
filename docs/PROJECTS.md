# 프로젝트 PATH — 24개 원자 블록

프로젝트 레인은 아래 순서를 바꾸지 않는다. 각 행은 **한 줄 역할 → 진입 조건 → 완료 결과**만 남긴 실행 색인이다.

| ID | 프로젝트 | 한 줄 역할 | 진입 조건 | 완료 결과 | 공개 위치 |
|---|---|---|---|---|---|
| P01 | `c-foundation` | C 바이트·문자열·할당·리스트·출력 계약을 정적 라이브러리로 고정한다. | `G01 guide-c` 완료 | 공개 API, 소유권·실패 경로, 테스트·새니타이저·배포 산출물 검증이 닫힌다. | `42` orphan branch |
| P02 | `buffered-line-reader` | 부분 `read`, EOF·대기·오류와 호출 간 버퍼 상태를 분리한다. | P01 완료 | legacy 함수와 명시적 context API의 fd·버퍼 수명 및 비용 검증이 닫힌다. | `42` orphan branch |
| P03 | `format-printer` | 가변 인자와 포맷 문법을 측정·출력의 두 순회 계약으로 구현한다. | P02 완료 | 지원 문법, 출력 길이·오류·`SIGPIPE` 경계와 release 검사가 닫힌다. | `42` orphan branch |
| P04 | `signal-message-bus` | signal과 Unix datagram을 결합한 세션·ACK 기반 로컬 메시지 전달을 만든다. | P03 완료 | handler/main 분리, self-pipe, timeout·손실·확정 모호성과 프로세스 검증이 닫힌다. | `42` orphan branch |
| P05 | `small-shell` | 제한된 shell 문법을 parser, process와 FD graph로 실행한다. | P04 완료 | quote·확장·pipeline·조건식·redirection·builtin과 자원 정리 검증이 닫힌다. | 독립 정본 저장소 |
| P06 | `thread-dining` | pthread 공유 상태의 동기화·교착 회피·종료 수명을 검증한다. | P05 완료 | 시작 barrier, fork·meal·terminal state, join·destroy 안전성과 동시성 검사가 닫힌다. | `42` orphan branch |
| P07 | `cpp-foundation` | C++ 객체 수명·값 의미론·다형성·예외·template의 기본 계약을 확립한다. | P06 및 `G03 guide-cpp` 완료 | 여섯 CLI와 정적 라이브러리의 객체·예외·검증 계약이 닫힌다. | `42` orphan branch |
| P08 | `stl-container` | allocator·iterator·vector·red-black tree의 내부 불변식을 직접 구현한다. | P07 완료 | `vector`, `stack`, `map`의 예외·무효화·복잡도·차등 검증이 닫힌다. | `42` orphan branch |
| P09 | `stack-sort` | 제한된 11개 명령으로 정렬하고 독립 checker·oracle로 상태 전이를 검증한다. | P08 완료 | parser, small/radix 전략, 명령 수·실제 비용·fault 검증이 닫힌다. | `42` orphan branch |
| P10 | `ray-scene-tracer` | 장면 파싱부터 BVH·재귀 shading·결정적 타일 병렬 렌더링까지 연결한다. | P09 완료 | linear/BVH 동치, 이미지 checksum, 병렬 소유권과 실패 경계가 닫힌다. | 독립 정본 저장소 |
| P11 | `irc-relay-server` | epoll/kqueue 기반 논블로킹 IRC relay와 연결별 상태·backpressure를 구현한다. | P10 완료 | framing, connection lifecycle, timeout·rate limit·shutdown과 TCP 검증이 닫힌다. | 독립 정본 저장소 |
| P12 | `container-stack` | Nginx·PHP-FPM·MariaDB 스택의 초기화·영속성·복구·운영 수명을 관리한다. | P11 및 `G08 guide-web-infrastructure` 완료 | build, readiness, backup·restore, secret rotation, diagnostics와 장애 수렴이 닫힌다. | 독립 정본 저장소 |
| P13 | `web-boundary-inspector` | HTTP proxy 왕복과 browser runtime의 요청·상태·보안 경계를 관찰한다. | P12 완료 | request trace와 DOM·Fetch·History·storage·CORS·CSP의 다중 브라우저 검증이 닫힌다. | 독립 정본 저장소 |
| P14 | `portfolio-site` | 콘텐츠 하나를 다섯 Next.js renderer로 표현하고 공개 배포 품질을 검증한다. | P13, `G09`, `G10` 완료 | production 콘텐츠, SSR·hydration, 접근성·성능·standalone 산출물과 실제 공개 URL이 준비된다. | 독립 정본 저장소 |
| P15 | `pong-pong` | Next.js·Fastify·PostgreSQL·WebSocket을 서버 권위 실시간 게임으로 통합한다. | P14 및 `G11 guide-database-systems` 완료 | 인증·매칭·방·재접속·결과 영속화·drain·E2E가 닫힌 풀스택 서비스가 된다. | 독립 정본 저장소 |
| P16 | `sportsbook-shared-protocol` | Java 값 객체·JSON·Avro의 서비스 공통 wire 계약을 고정한다. | P15 및 `G12 guide-java` 완료 | Maven artifact, 금액·배당·ID·이벤트 schema와 호환성 검사가 닫힌다. | 독립 정본 저장소 |
| P17 | `sportsbook-wallet-service` | 계좌 snapshot과 복식부기 원장으로 멱등 자금 이동을 처리한다. | P16 및 `G13 guide-backend-spring-boot` 완료 | Spring·JPA·Flyway·lock·outbox·대사와 PostgreSQL 통합 검증이 닫힌다. | 독립 정본 저장소 |
| P18 | `sportsbook-risk-service` | Redis Lua 기준 상태로 한도·예약·commit·release를 원자 전이한다. | P17 완료 | keyspace, lease·tombstone·capacity 경쟁과 Kafka 재전달 검증이 닫힌다. | 독립 정본 저장소 |
| P19 | `sportsbook-odds-feed-service` | provider 입력을 Redis projection과 서로 다른 Kafka 전달 경로로 정규화한다. | P18 완료 | 일반 가격·critical Stream·운영자 명령의 보장 차이와 복구 검증이 닫힌다. | 독립 정본 저장소 |
| P20 | `sportsbook-betting-service` | risk 예약·wallet 차감·배당 확인을 복구 가능한 베팅 접수 상태로 조정한다. | P19 및 `G14 guide-distributed-services` 완료 | `PENDING`, idempotency, compensation, recovery와 수락 outbox가 닫힌다. | 독립 정본 저장소 |
| P21 | `sportsbook-settlement-service` | 결과 read model과 영속 attempt로 wallet 효과와 종료 이벤트를 조정한다. | P20 완료 | 계산·wallet plan·lease/fencing·outbox·DLT·복구 경계가 닫힌다. | 독립 정본 저장소 |
| P22 | `sportsbook-gateway` | 사용자 JWT·rate limit·REST routing·STOMP 전달의 data plane 경계를 만든다. | P21 완료 | trusted header 재작성, 공개 route, 실시간 fan-out과 보안·운영 제한이 닫힌다. | 독립 정본 저장소 |
| P23 | `sportsbook-admin-api` | 운영자 인증·권한·내부 위임·감사 로그의 control plane을 만든다. | P22 완료 | 역할·IP 제한, delegation, PostgreSQL 감사와 Kafka 보조 복제 검증이 닫힌다. | 독립 정본 저장소 |
| P24 | `sportsbook-orchestration` | 아홉 저장소의 build·Compose·cold E2E·chaos·관측 근거를 하나로 통합한다. | P23 완료 | 전체 릴리스 조합, 초기 상태 수렴, 장애 증거와 최종 연결 감사가 닫힌다. | 독립 정본 저장소 |

## 레인 규칙

- 프로젝트 블록은 한 번에 하나만 활성화한다.
- 현재 행의 완료 결과를 충족하기 전에는 다음 행을 시작하지 않는다.
- 가이드가 하드 게이트를 막으면 프로젝트 레인을 비우고 가이드 레인만 진행한다.
- 독립 정본 저장소의 코드를 `42` orphan branch에 복제하지 않는다.
