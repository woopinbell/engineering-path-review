# 42 orphan branch baseline

각 과제 branch는 단독 clone/archive에서 다음을 만족한다.

```text
README · LICENSE · 검증/비보장 문서
소스·설정·필요한 lockfile
정상·실패·sanitizer 검사
push/PR workflow
scope-prefixed tag
secret·개인정보·42 subject/평가표 미포함
```

workflow는 해당 branch의 push와 그 branch를 base로 하는 PR을 대상으로 한다. read-only token, full SHA action pin, timeout, `persist-credentials: false`를 사용한다. scheduled workflow의 non-default branch 제약 때문에 dependency 점검 날짜와 명령을 README에 기록한다.

standalone 정본이 있는 프로젝트에는 orphan branch를 만들지 않는다.
