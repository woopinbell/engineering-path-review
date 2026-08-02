# 권장 GitHub 저장소 설정

## 공개 전

```text
검토 중 private
2FA/passkey와 recovery code 확인
Secret scanning·Push protection 활성화
Private vulnerability reporting 활성화
Dependabot alerts·Dependency graph 활성화
```

## Rulesets

### main

```text
PR 필수
verify-main status check 필수
force push·deletion 차단
linear history 권장
solo 운영 중 required approval 0, reviewer가 생기면 1로 변경
```

### orphan branch

각 정본 branch 이름에 ruleset을 만들고 branch-local CI를 필수 check로 둔다. 최초 이력 수입 뒤 force push와 deletion을 차단한다.

## Actions

```text
허용 action 제한
full commit SHA pin 요구
workflow token read-only 기본값
fork PR workflow approval 사용
self-hosted runner 사용 안 함
```

scheduled workflow와 Dependabot security update는 non-default branch에서 기본 branch와 같은 보장을 하지 않는다. 각 orphan branch는 push/PR CI와 lockfile을 소유하고, dependency audit를 수동 일정으로 실행한다. 배포·독립 보안 대응이 필요한 프로젝트는 standalone 정본을 유지한다.
