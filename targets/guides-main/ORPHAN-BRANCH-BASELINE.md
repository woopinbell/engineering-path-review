# Guide orphan branch baseline

각 `guide-*` branch는 단독 clone/archive에서 다음을 만족한다.

```text
README · LICENSE · 본문·reference
skeleton/workspace/reference 실습
정상·실패·전체 check/verify
dependency lockfile와 버전 기준
push/PR workflow
scope-prefixed tag
외부 전문·credential·개인정보 미포함
```

workflow는 해당 guide branch의 push와 그 branch를 base로 하는 PR을 검사한다. scheduled workflow와 security update의 non-default branch 제약을 전제로 수동 dependency 점검 명령·주기를 README에 기록한다.
