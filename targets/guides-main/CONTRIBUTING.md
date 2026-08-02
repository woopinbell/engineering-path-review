# Contributing

## 변경 대상

- `main`: 가이드 지도·PATH·정본 정책·라이선스·보안 설정만
- `guide-*`: 해당 가이드의 본문·예제·실습·검증만

교차 개념은 `[cross-guide]` 이슈로 기록하되 실제 수정은 guide별 PR로 나눈다. PR base는 변경 대상 guide branch다.

## 확인

```sh
python3 scripts/check_main.py  # main 변경
```

각 guide branch는 README의 `check`/`verify`를 실행한다.

## 금지

- 개별 guide 저장소와 branch를 병렬 정본으로 수정
- secret·개인정보·제3자 전문·비허가 asset 커밋
- 외부 입력을 shell/HTML로 그대로 실행·렌더링
- guide branch를 main이나 다른 guide branch와 merge
