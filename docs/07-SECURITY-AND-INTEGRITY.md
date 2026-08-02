# 보안·무결성 기준

## 1. 저장소 공개 전 계정 기준

```text
GitHub 2단계 인증 또는 passkey 활성화
복구 코드 오프라인 보관
세션·OAuth App·Personal Access Token 정기 점검
사용하지 않는 deploy key와 token 폐기
저장소 검토 중에는 private 유지
```

개인 연락처·주소·생년월일·군번·신분증·이력서 원본·채용 계정 정보는 이 검토 저장소에 커밋하지 않는다. 공고 판정에는 공개해도 안전한 비식별 전제만 남긴다.

## 2. GitHub 보안 기능

공개 전 다음 기능을 활성화한다.

```text
Secret scanning
Push protection
Private vulnerability reporting
Dependabot alerts
Dependency graph
```

문서·스크립트 저장소라도 실수로 token이나 key가 커밋될 수 있으므로 secret scanning을 끄지 않는다.

## 3. ruleset 권장값

### `main`

```text
Pull Request만 허용
필수 status check: verify
force push·branch deletion 차단
linear history 권장
가능하면 signed commit 또는 vigilant mode 사용
```

혼자 운영하는 동안 필수 승인 인원은 0으로 둘 수 있다. 다른 reviewer가 생기면 승인 1명과 stale approval dismissal을 추가한다.

### orphan branch

각 정본 branch에도 별도 ruleset을 적용한다.

```text
branch 이름 정확 일치
branch별 verify workflow 필수
force push·삭제 차단
직접 push 대신 PR 사용
```

초기 Git 이력 수입이 끝난 뒤에는 branch를 다시 orphan으로 만들거나 이력을 교체하지 않는다.

## 4. GitHub Actions 기준

- workflow token은 `contents: read`를 기본값으로 둔다.
- third-party action은 tag가 아니라 **full commit SHA**로 고정한다.
- checkout은 `persist-credentials: false`로 설정한다.
- `pull_request_target`, `workflow_run`, `issue_comment`에서 PR 코드를 실행하지 않는다.
- fork PR에 secret을 전달하지 않는다.
- self-hosted runner를 사용하지 않는다.
- `timeout-minutes`와 concurrency cancellation을 설정한다.
- 배포·write 권한이 필요한 workflow는 검증 workflow와 분리하고 environment 보호 규칙을 둔다.

이 패키지의 workflow는 네트워크 설치 없이 저장소 자체 검사만 실행한다.

## 5. orphan branch의 보안 한계

orphan branch는 저장소를 줄이는 정리 방식이지 보안 격리 장치가 아니다.

- 저장소 관리자·Actions·Issues·Security 설정은 branch가 아니라 저장소 단위다.
- scheduled workflow는 기본 branch에 있는 workflow 정의를 기준으로 실행된다.
- non-default branch의 code scanning은 그 branch에도 맞는 workflow와 push/PR trigger가 있어야 한다.
- Dependabot version update는 target branch를 지정할 수 있지만 security update는 기본 branch 중심 제약이 있다.
- 한 저장소의 vulnerability·release·tag namespace가 여러 독립 프로젝트에 공유된다.

따라서 dependency가 많고 외부 배포·운영·보안 대응이 독립적으로 필요한 프로젝트는 standalone 저장소를 정본으로 유지한다. orphan branch에 남기는 프로젝트·가이드는 branch 내부에 lockfile·검증 명령·branch-local CI를 소유하며, 주기적 dependency 점검은 사람이 명시적으로 실행한다.

## 6. 정본·공급망 무결성

```text
같은 구현을 두 정본에 복제하지 않음
release/tag는 scope prefix 사용
외부 action·dependency 버전 고정
빌드·검증 명령과 비보장 기록
ZIP 내부 MANIFEST.sha256 제공
ZIP 자체 SHA-256 별도 제공
```

이 패키지의 생성기는 symlink, `.git`, secret 후보, repository 밖 경로, 위험한 URL scheme, 허용되지 않은 binary를 거부한다.

## 7. 링크·외부 데이터

- 로컬 링크는 저장소 밖으로 빠져나갈 수 없다.
- 외부 링크는 HTTPS만 허용한다.
- `javascript:`, `data:`, `file:`, `sandbox:`와 절대 로컬 경로를 거부한다.
- 공고 데이터는 원문 전문이 아니라 자체 요약과 링크만 저장한다.
- URL·ID·회사/직무 중복과 active/expired 충돌을 검사한다.
- 공고 상태는 정적 스냅숏이며 자동으로 최신이라고 주장하지 않는다.

## 8. 공개 뒤 사고 대응

1. credential 노출이면 즉시 폐기·회전한다.
2. 영향 branch·workflow·release package를 식별한다.
3. 정본을 수정하고 필요할 때만 이력을 재작성한다.
4. 기존 clone과 archive가 영향을 받는지 공지한다.
5. `make build`, `make check`, `make package`로 새 package를 만든다.
