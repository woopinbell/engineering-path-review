# 42

42 과정 과제와 재구현 기록을 탐색하기 위한 개인 학습 아카이브다. 이 저장소는 하나의 코드베이스를 기능 branch로 개발하는 일반 저장소가 아니다.

```text
main                전체 과제 색인·정본 위치·운영 정책만
orphan branches     작은·단일 개념 과제의 독립 Git 이력
standalone repos    독립 제품으로 공개할 프로젝트의 유일한 정본
```

> 42, 42 Network 또는 특정 캠퍼스의 공식 저장소가 아니다. 아래 순서는 개인 재학습 PATH이며 공식 과제 배정·평가 순서를 주장하지 않는다.

## 프로젝트 지도

| 순서 | 프로젝트 | 위치 | 한 줄 역할 |
|---:|---|---|---|
| 1 | `c-foundation` | [branch](https://github.com/woopinbell/42/tree/c-foundation) | C 정적 라이브러리로 바이트·소유권·rollback·부분 출력을 고정 |
| 2 | `buffered-line-reader` | [branch](https://github.com/woopinbell/42/tree/buffered-line-reader) | 부분 `read`, EOF·오류·대기와 FD별 상태 수명 구현 |
| 3 | `format-printer` | [branch](https://github.com/woopinbell/42/tree/format-printer) | 가변 인자·포맷 parser·두 순회 출력 계약 구현 |
| 4 | `signal-message-bus` | [branch](https://github.com/woopinbell/42/tree/signal-message-bus) | signal·self-pipe·session·ACK 상태 머신 구현 |
| 5 | `small-shell` | [독립 정본](https://github.com/woopinbell/small-shell-changelog) | parser를 process·FD graph와 builtin·redirection으로 실행 |
| 6 | `thread-dining` | [branch](https://github.com/woopinbell/42/tree/thread-dining) | pthread 공유 상태·잠금 순서·terminal state·안전한 정리 구현 |
| 7 | `cpp-foundation` | [branch](https://github.com/woopinbell/42/tree/cpp-foundation) | C++98 객체 수명·값 의미론·다형성·예외 안전성 확립 |
| 8 | `stl-container` | [branch](https://github.com/woopinbell/42/tree/stl-container) | allocator·iterator·vector/stack/map·RB-tree 계약 구현 |
| 9 | `stack-sort` | [branch](https://github.com/woopinbell/42/tree/stack-sort) | 제한 명령 정렬과 독립 checker/oracle 분리 |
| 10 | `ray-scene-tracer` | [독립 정본](https://github.com/woopinbell/ray-scene-tracer-changelog) | BVH·shading·결정적 tile 병렬 CPU ray tracer |
| 11 | `irc-relay-server` | [독립 정본](https://github.com/woopinbell/irc-relay-server-changelog) | `epoll/kqueue` 논블로킹 연결·backpressure·timeout 서버 |
| 12 | `container-stack` | [독립 정본](https://github.com/woopinbell/container-stack-changelog) | Compose 웹 스택의 bootstrap·persistence·backup/restore 운영 |
| 13 | `web-boundary-inspector` | [독립 정본](https://github.com/woopinbell/web-boundary-inspector-changelog) | HTTP proxy와 브라우저 runtime의 상태·정책 경계 관찰 |
| 14 | `pong-pong` | [독립 정본](https://github.com/woopinbell/pong-pong-changelog) | Next.js·Fastify·PostgreSQL·WebSocket 서버 권위 실시간 서비스 |

`portfolio-site`는 42 과제가 아니라 전체 개발 결과물의 공개 진입점이므로 [별도 저장소](https://github.com/woopinbell/portfolio-site-changelog)에서 관리한다.

## 정본 규칙

- branch 프로젝트는 해당 orphan branch가 코드·문서·태그의 정본이다.
- 독립 프로젝트는 별도 저장소가 유일한 정본이다.
- 독립 프로젝트의 전체 코드를 42 orphan branch에 복제하지 않는다.
- 이전 개별 저장소를 보존하면 read-only archive 또는 새 정본 안내만 둔다.

## branch 사용

```sh
git clone --branch c-foundation --single-branch \
  https://github.com/woopinbell/42.git 42-c-foundation
```

이미 `main`을 clone했다면 별도 worktree를 사용한다.

```sh
git fetch origin c-foundation
git worktree add --detach ../42-c-foundation origin/c-foundation
```

각 branch는 단독 clone/archive에서 README, LICENSE, 소스, 테스트와 검증 문서를 모두 제공해야 한다. 과제 branch를 `main`이나 다른 과제 branch에 merge·rebase하지 않는다.

## 이슈·PR·태그

```text
[c-foundation] allocation rollback 설명 수정
[main] 프로젝트 지도 링크 수정
c-foundation/v1.0.0
```

Pull Request base는 `main` 또는 변경 대상 과제 branch 하나만 지정한다. 여러 과제 변경을 한 Pull Request에 섞지 않는다.

## 라이선스

직접 작성한 소프트웨어는 MIT, 문서·도식은 CC BY 4.0을 따른다. subject·평가표·로고와 제3자 자료에는 원 권리자의 조건이 적용된다. 자세한 내용은 [LICENSE.md](LICENSE.md)를 따른다.

## 관리 문서

- [보안 정책](SECURITY.md)
- [기여·변경 절차](CONTRIBUTING.md)
- [권장 GitHub 설정](REPOSITORY-SETTINGS.md)

`main` 자체 검사는 `python3 scripts/check_main.py`로 실행한다. 각 orphan branch는 자신의 빌드·테스트·dependency 점검을 별도로 소유한다.

각 orphan branch가 갖춰야 할 최소 구조는 [42 orphan branch baseline](ORPHAN-BRANCH-BASELINE.md)에 고정한다.
