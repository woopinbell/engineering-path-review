# GitHub 저장소·orphan branch 전략

## 정본 지도

```text
engineering-path-review       검토·개선·확정용 임시 저장소
├─ targets/42-main            42/main 문서·보안 설정 후보
└─ targets/guides-main        guides/main 문서·보안 설정 후보

woopinbell/42
├─ main                       과제 색인·정책·라이선스만
├─ orphan branches            작은·단일 개념 과제의 정본
└─ standalone links           독립 제품 저장소의 색인

woopinbell/guides
├─ main                       가이드 색인·정책·라이선스만
└─ guide-* orphan branches    17개 가이드 정본
```

## 42 분류

### orphan branch 정본

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

### 독립 저장소 정본

```text
small-shell-changelog
ray-scene-tracer-changelog
irc-relay-server-changelog
container-stack-changelog
web-boundary-inspector-changelog
pong-pong-changelog
```

`portfolio-site-changelog`는 42 과제가 아니라 전체 결과물의 공개 진입점으로 별도 유지한다.

## Guides 분류

17개 가이드를 `woopinbell/guides`의 서로 공통 조상이 없는 `guide-*` branch로 통합한다. 전체 목록은 [`guides/main` 후보 README](../targets/guides-main/README.md)에 있다.

## 단일 정본 규칙

```text
standalone이 정본인 프로젝트의 코드를 42 branch에 복제하지 않음
42/guides branch를 과거 개별 저장소와 병렬 수정하지 않음
review target과 실제 main을 동시에 수정하지 않음
```

과거 개별 저장소를 남길 때는 read-only archive 또는 새 정본 URL 안내만 둔다.

## 링크 규칙

1. `main`의 branch·standalone 링크는 GitHub HTTPS 절대 URL을 사용한다.
2. orphan branch 내부의 문서 링크는 branch 안에서 해결되는 상대 경로를 사용한다.
3. 다른 branch를 참조할 때는 상대 경로를 만들지 않고 정본 GitHub URL을 사용한다.
4. 같은 이름의 과거 저장소와 새 정본을 동시에 현재 링크로 노출하지 않는다.
5. 이름 변경과 링크 수정은 한 변경에서 처리한다.
6. `../../tree/<branch>`, `/mnt/data`, `file:`, `sandbox:` 같은 문맥·runtime 의존 링크를 게시하지 않는다.

## branch 자체 완결 조건

각 orphan branch는 `--single-branch` clone과 archive에서도 다음을 제공한다.

```text
README · LICENSE · SECURITY 또는 상위 보안 정책 링크
소스·설정·lockfile
정상·실패 검증 도구
architecture·docs·devlog
branch-local push/PR CI
해당 branch의 전체 Git 이력
```

다른 branch 파일이 있어야 빌드·검증·라이선스 확인이 가능한 구조는 허용하지 않는다.

## orphan branch의 운영·보안 한계

orphan branch는 파일과 Git 이력을 분리하지만 다음은 저장소 단위로 공유한다.

```text
Issues · Security 탭 · Actions 정책 · repository secret · 관리자 권한
release/tag namespace · vulnerability/Dependabot UI · 기본 branch 설정
```

또한 scheduled workflow는 기본 branch 중심으로 동작하고, non-default branch의 code scanning은 해당 branch에 맞는 workflow trigger가 필요하다. Dependabot도 non-default branch에서 기본 branch와 같은 security update 경험을 제공하지 않는다.

따라서 다음 조건이면 standalone 저장소를 유지한다.

```text
외부 배포·운영 수명과 독립 release가 있음
dependency와 vulnerability 대응이 활발함
독립 issue/PR/security advisory가 필요함
별도 environment·secret·deployment permission이 필요함
```

orphan branch에 남기는 범위는 branch-local CI와 수동 dependency 점검 일정을 문서화한다. 자세한 기준은 [보안·무결성](07-SECURITY-AND-INTEGRITY.md)을 따른다.

## namespace

| 대상 | 형식 | 예시 |
|---|---|---|
| 작업 branch | `work/<scope>/<topic>` | `work/c-foundation/rollback-docs` |
| 이슈·PR | `[scope] 제목` | `[guide-c] EOF 검증 보강` |
| 교차 이슈 | `[cross-guide] 제목` | `[cross-guide] TLB 용어 대조` |
| tag/release | `<scope>/vX.Y.Z` | `thread-dining/v1.1.0` |

한 Pull Request에 서로 다른 project/guide branch 변경을 섞지 않는다. base는 변경 대상 branch 또는 `main` 하나다.

## 최종 main 후보

### 42

- [README](../targets/42-main/README.md)
- [LICENSE](../targets/42-main/LICENSE.md)
- [SECURITY](../targets/42-main/SECURITY.md)
- [CONTRIBUTING](../targets/42-main/CONTRIBUTING.md)
- [권장 저장소 설정](../targets/42-main/REPOSITORY-SETTINGS.md)

### Guides

- [README](../targets/guides-main/README.md)
- [LICENSE](../targets/guides-main/LICENSE.md)
- [SECURITY](../targets/guides-main/SECURITY.md)
- [CONTRIBUTING](../targets/guides-main/CONTRIBUTING.md)
- [권장 저장소 설정](../targets/guides-main/REPOSITORY-SETTINGS.md)
