# 42·guides 검토·개선·확정 절차

## 목적

이 저장소에서 구조·명칭·PATH·L 작업·링크·정본·보안 정책을 확정한 뒤 `42/main`과 `guides/main`으로 옮긴다. 프로젝트·가이드 본문 전체는 복제하지 않는다.

## 순서

```text
1. inventory·Git 이력·현재 정본 후보 고정
2. branch/standalone 분류와 이름 고정
3. P/G PATH·하드 게이트·L trigger 검토
4. target README·LICENSE·SECURITY·CONTRIBUTING 검토
5. orphan branch 자체 완결성과 branch-local CI 검토
6. ruleset·Actions·secret scanning·vulnerability reporting 설정안 검토
7. 로컬 링크·정본 URL·license·개인정보·secret 검사
8. P0·P1 수정
9. target 문서를 실제 main으로 이전
10. branch를 수입하고 ruleset 적용
11. 이전 개별 저장소 archive/redirect
12. 이 임시 저장소 read-only archive
```

## 심각도

| 등급 | 의미 | 처리 |
|---|---|---|
| P0 | 코드·이력·라이선스·credential·개인정보·정본 유실/노출 | 게시 중단, credential 회전 후 즉시 수정 |
| P1 | 깨진 링크, 잘못된 선행 조건, 중복 정본, CI/검증 불가, 보호 설정 누락 | 해당 단계 종료 전 수정 |
| P2 | 표현·정렬·보충 설명 | backlog; 최종화를 막지 않음 |

## `main` 검토표

```text
[ ] 구현 코드가 main에 없음
[ ] 모든 branch·standalone이 정확히 한 번 등장
[ ] main 링크가 HTTPS 정본 URL을 가리킴
[ ] README·LICENSE·SECURITY·CONTRIBUTING이 존재
[ ] verify-main workflow가 read-only·full SHA pin을 사용
[ ] branch 삭제·force push·직접 push 방지 설정이 문서와 일치
[ ] secret·개인정보·제3자 원문이 없음
```

## orphan branch 검토표

```text
[ ] README·LICENSE와 검증 문서가 branch 내부에 존재
[ ] 단독 clone/archive에서 빌드·검증 가능
[ ] 다른 branch 파일에 상대 링크로 의존하지 않음
[ ] lockfile·dependency 기준이 branch 안에 있음
[ ] push/PR branch-local CI가 있음
[ ] scheduled security automation의 한계와 수동 점검 절차가 있음
[ ] 정상·실패 경로와 비보장 범위가 기록됨
[ ] branch ruleset·tag namespace·PR base 정책이 일치
```

## standalone 검토표

```text
[ ] 42/main에는 링크만 있고 전체 코드 복제가 없음
[ ] README·LICENSE·SECURITY·Issues·Release·CI의 유일 정본
[ ] 독립 secret/environment/deployment 권한이 분리됨
[ ] 공개 결과·검증·architecture·devlog가 독립적으로 이해 가능
[ ] vulnerability·dependency update가 default branch에서 정상 동작
```

## 변경 기록

```text
대상:
문제:
심각도:
근거:
결정:
수정 파일:
검증:
남은 P2:
```

여러 branch를 수정해야 하면 branch별 commit/PR로 나누고 이 저장소에는 공통 결정만 남긴다.

## 최종화 종료 조건

```sh
make build
make check
make package
```

추가 조건:

```text
P0·P1 0개
target 두 세트의 자체 검사 성공
ZIP을 새 디렉터리에 풀어 make check 재성공
42/guides 실제 ruleset·Security·Actions 설정 적용 확인
이전 정본의 archive/redirect 완료
```
