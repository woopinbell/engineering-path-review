# Guides

언어·운영체제·컴퓨터과학·웹·백엔드 가이드를 하나의 저장소에서 관리하는 개인 학습 아카이브다.

```text
main                 전체 가이드 색인·학습 PATH·운영 정책만
guide-* branches     서로 공통 조상이 없는 각 가이드의 독립 Git 이력과 정본
```

가이드별 독립 정본 저장소를 병렬 운영하지 않는다.

## 가이드 지도

| 구분 | 가이드 | 한 줄 역할 |
|---|---|---|
| 기반 | [guide-git](https://github.com/woopinbell/guides/tree/guide-git) | Git 상태·branch·통합·복구를 격리 저장소에서 재현 |
| 기반 | [guide-c](https://github.com/woopinbell/guides/tree/guide-c) | C 메모리·소유권·빌드와 POSIX I/O·process·thread 연결 |
| 기반 | [guide-unix-systems](https://github.com/woopinbell/guides/tree/guide-unix-systems) | shell·filesystem·FD·process·socket·service를 사용자 공간에서 관찰 |
| 조건부 | [guide-python](https://github.com/woopinbell/guides/tree/guide-python) | CS 상태 모델·CLI·subprocess·재현 가능한 테스트 기반 |
| 선택 | [guide-shell-scripting](https://github.com/woopinbell/guides/tree/guide-shell-scripting) | POSIX `sh`/Bash 자동화의 인자·실패·정리·이식성 고정 |
| 기반 | [guide-cpp](https://github.com/woopinbell/guides/tree/guide-cpp) | C++ 객체·제네릭·socket/event loop 책임 확장 |
| CS | [guide-operating-systems](https://github.com/woopinbell/guides/tree/guide-operating-systems) | scheduler·동기화·VM·filesystem을 상태·정책·불변식으로 모델링 |
| CS | [guide-algorithms](https://github.com/woopinbell/guides/tree/guide-algorithms) | 문제 계약·정확성·복잡도·반례 검증 루프 확립 |
| CS | [guide-computer-architecture](https://github.com/woopinbell/guides/tree/guide-computer-architecture) | ISA·pipeline·cache·TLB·parallelism의 비용 모델 연결 |
| CS | [guide-computer-networks](https://github.com/woopinbell/guides/tree/guide-computer-networks) | Ethernet부터 TCP·DNS·HTTP·TLS·QUIC까지 종단 경로 연결 |
| 웹 | [guide-web-infrastructure](https://github.com/woopinbell/guides/tree/guide-web-infrastructure) | request→gateway→runtime→DB의 배치·초기화·복구 실습 |
| 웹 | [guide-web-applications](https://github.com/woopinbell/guides/tree/guide-web-applications) | browser·React·API·DB·auth·WebSocket을 한 서비스로 연결 |
| 웹 | [guide-frontend-react-nextjs](https://github.com/woopinbell/guides/tree/guide-frontend-react-nextjs) | URL·server/client state·접근성·성능·배포 심화 |
| 데이터 | [guide-database-systems](https://github.com/woopinbell/guides/tree/guide-database-systems) | 관계·page·index·transaction·MVCC·WAL·query cost 모델링 |
| 백엔드 | [guide-java](https://github.com/woopinbell/guides/tree/guide-java) | Java 17·JVM·값 객체·동시성·Maven·테스트 기반 |
| 백엔드 | [guide-backend-spring-boot](https://github.com/woopinbell/guides/tree/guide-backend-spring-boot) | Spring HTTP·JPA·Redis·Kafka·Outbox·관측 경계 구현 |
| 분산 | [guide-distributed-services](https://github.com/woopinbell/guides/tree/guide-distributed-services) | 서비스 경계·멱등성·부분 실패·복구·release evidence 연결 |

## 기본 PATH

```text
guide-git → guide-c → guide-unix-systems
→ [guide-python? / guide-shell-scripting?]
→ guide-cpp → guide-operating-systems → guide-algorithms
→ guide-computer-architecture → guide-computer-networks
→ guide-web-infrastructure → guide-web-applications
→ guide-frontend-react-nextjs → guide-database-systems
→ guide-java → guide-backend-spring-boot → guide-distributed-services
```

시작한 가이드 하나는 본문·실습·전체 검증까지 원자적으로 완료한다. 현재 가이드를 끝낸 뒤에는 아직 시작하지 않은 독립 가이드의 순서를 가장 가까운 프로젝트 hard gate에 맞춰 조정할 수 있다.

## 완료 기준

```text
준비 환경·버전 확인
→ 본문과 연결 실습 수행
→ skeleton/workspace 직접 구현
→ 정상·실패 경로 검사
→ reference와 상태·불변식·비보장 비교
→ 전체 check/verify
→ 완료 근거와 P0·P1 확인
```

## branch 사용

```sh
git clone --branch guide-operating-systems --single-branch \
  https://github.com/woopinbell/guides.git guide-operating-systems
```

각 branch는 단독 clone/archive에서 README, LICENSE, 본문, 실습과 검증 도구를 모두 제공해야 한다. guide branch를 `main`이나 다른 guide branch에 merge·rebase하지 않는다.

## 이슈·PR·태그

```text
[guide-c] record-stream EOF 검증 보강
[cross-guide] OS와 architecture의 TLB 용어 대조
[main] 가이드 지도 수정
guide-c/v1.0.0
```

Pull Request base는 변경 대상 guide branch다. 교차 이슈의 실제 수정은 guide별 Pull Request로 나눈다.

## 라이선스

직접 작성한 예제·실습·검증 코드는 MIT, 본문·도식은 CC BY 4.0을 따른다. 인용·번역·외부 명세와 제3자 자료에는 원 권리자의 조건이 적용된다. 자세한 내용은 [LICENSE.md](LICENSE.md)를 따른다.

## 관리 문서

- [보안 정책](SECURITY.md)
- [기여·변경 절차](CONTRIBUTING.md)
- [권장 GitHub 설정](REPOSITORY-SETTINGS.md)

`main` 자체 검사는 `python3 scripts/check_main.py`로 실행한다. 각 guide branch는 자신의 예제·실습·dependency 점검과 push/PR CI를 별도로 소유한다.

각 guide branch가 갖춰야 할 최소 구조는 [Guide orphan branch baseline](ORPHAN-BRANCH-BASELINE.md)에 고정한다.
