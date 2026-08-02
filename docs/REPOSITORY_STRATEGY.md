# GitHub 저장소·orphan branch 전략

이 문서는 최종 코드 저장소가 아니라 `42`와 `guides`의 구조를 검토·확정하기 위한 임시 정본이다.

## 목표 구조

```text
42
├─ main                 과제 지도·정본 정책·운영 규칙·라이선스만
└─ orphan branches      작은 42 과제 각각의 완전한 독립 이력

guides
├─ main                 가이드 지도·학습 경로·운영 규칙·라이선스만
└─ orphan branches      모든 가이드 각각의 완전한 독립 이력

standalone repositories 독립 제품성이 충분한 프로젝트의 유일한 코드 정본
```

## 정본 원칙

1. 하나의 프로젝트·가이드는 정확히 하나의 정본만 가진다.
2. 독립 저장소로 승격한 프로젝트의 코드를 `42` orphan branch에 복제하지 않는다.
3. `main`은 색인과 정책만 소유하며 개별 구현·실습을 포함하지 않는다.
4. orphan branch는 다른 과제·가이드 branch와 merge·rebase하지 않는다.
5. branch 단독 clone·archive에서도 README와 라이선스를 확인할 수 있어야 한다.

## `42` 저장소

### `main` 문서 세트

```text
README.md       전체 순서, 한 줄 설명, branch·독립 저장소 지도
LICENSE.md      문서 CC BY 4.0, 코드 MIT, 제3자 자료 제외
```

개별 과제의 장문 설명·코드·빌드 결과는 `main`에 두지 않는다.

### orphan branch

```text
c-foundation
buffered-line-reader
format-printer
signal-message-bus
thread-dining
cpp-foundation
stl-container
stack-sort
```

각 branch 루트는 최소한 다음을 갖는다.

```text
README.md
LICENSE 또는 LICENSE.md
소스·테스트·문서
branch 자체 검증 진입점
```

### 독립 정본 저장소

```text
small-shell
ray-scene-tracer
irc-relay-server
container-stack
pong-pong
```

`42/main`에는 역할·학습 순서·정본 링크만 둔다. `portfolio-site`와 `web-boundary-inspector`는 42 과제 branch가 아니라 별도의 독립 정본으로 관리한다.

## `guides` 저장소

### `main` 문서 세트

```text
README.md       가이드 지도, 선행·병렬 경로, branch 운영 규칙
LICENSE.md      문서 CC BY 4.0, 코드 MIT, 인용·외부 자료 예외
```

### orphan branch

```text
guide-git
guide-c
guide-unix-systems
guide-python
guide-shell-scripting
guide-cpp
guide-operating-systems
guide-algorithms
guide-computer-architecture
guide-computer-networks
guide-web-infrastructure
guide-web-applications
guide-frontend-react-nextjs
guide-database-systems
guide-java
guide-backend-spring-boot
guide-distributed-services
```

가이드는 별도 정본 저장소로 분리하지 않는다.

## clone·worktree 사용

한 branch만 받을 때:

```sh
git clone --branch c-foundation --single-branch \
  https://github.com/woopinbell/42.git 42-c-foundation
```

이미 `main`을 clone했다면 격리된 worktree를 만든다.

```sh
git fetch origin c-foundation
git worktree add --detach ../42-c-foundation origin/c-foundation
cd ../42-c-foundation
git switch -c work/c-foundation/docs
```

가이드도 동일하게 `guides` 저장소와 해당 `guide-*` branch를 사용한다.

## 이슈·PR·태그 namespace

저장소 단위 목록이 공유되므로 제목과 태그에 대상을 포함한다.

```text
[c-foundation] allocation rollback 설명 수정
[guide-database-systems] WAL 실습 검증 보강
[main] branch 지도 갱신
[cross-guide] OS·architecture TLB 용어 대조
```

```text
c-foundation/v1.0.0
guide-operating-systems/v1.2.0
```

Pull Request의 base는 변경 대상 branch 하나만 사용하고 여러 독립 이력을 한 PR에 섞지 않는다.

## CI 원칙

- 각 orphan branch와 독립 저장소가 자신의 toolchain·workflow를 소유한다.
- `main`은 README·LICENSE·branch 목록·링크 정도만 검사한다.
- 서로 다른 언어와 환경의 전체 build를 `main`의 거대 workflow 하나로 합치지 않는다.
- 현재 임시 검토 저장소의 [`make check`](../Makefile)는 문서 구조·링크·PATH·공고 snapshot만 검사한다.

## 이전 저장소 정리

이전 개별 `guide-*`·과제 저장소가 존재하면 다음 중 하나만 선택한다.

```text
1. 새 정본으로 완전 이전 후 archive + 새 위치 안내
2. 기록 보존이 필요하지 않으면 삭제
```

두 위치에서 계속 수정하는 상태는 허용하지 않는다.
