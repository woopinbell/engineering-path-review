# 권장 GitHub 저장소 설정

## 공개 전

```text
검토 중 private
Secret scanning·Push protection 활성화
Private vulnerability reporting 활성화
Dependabot alerts·Dependency graph 활성화
```

## Rulesets

`main`과 17개 `guide-*` 정본 branch에 각각 PR·status check·force push/deletion 차단 규칙을 적용한다. solo 운영이면 required approval은 0으로 시작할 수 있다.

## Actions와 dependency

```text
full commit SHA pin
read-only GITHUB_TOKEN
persist-credentials false
self-hosted runner 금지
fork PR secret 전달 금지
```

scheduled workflow는 default branch 중심이고, guide branch의 code scanning·검증은 해당 branch의 push/PR workflow가 소유해야 한다. Dependabot version update는 target branch를 지정할 수 있지만 security update의 non-default branch 경험에는 제약이 있으므로, dependency가 있는 guide는 lockfile과 수동 audit 절차를 함께 둔다.
