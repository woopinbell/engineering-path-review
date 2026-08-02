# Contributing

## 변경 대상

- `main`: 프로젝트 지도·정본 정책·라이선스·보안 설정만
- orphan branch: 해당 과제의 코드·문서·검증만
- standalone 프로젝트: 해당 독립 저장소에서만 변경

한 PR에 서로 다른 과제 branch를 섞지 않는다. base는 변경 대상 branch 하나다.

## 확인

```sh
python3 scripts/check_main.py  # main 변경
```

과제 branch는 그 branch README가 지정한 전체 검증을 실행한다.

## 금지

- standalone 코드의 main/orphan 복제
- secret·개인정보·42 subject·평가표·로고 커밋
- mutable action tag와 write 권한 workflow
- branch 간 merge/rebase로 이력 결합
