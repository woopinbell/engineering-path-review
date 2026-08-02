# Security policy

## 범위

이 저장소는 문서·정적 데이터·생성 스크립트만 포함한다. 실행 서비스나 사용자 데이터를 처리하지 않지만 다음 문제는 보안 이슈로 취급한다.

- secret, token, private key, 개인 식별정보의 커밋
- 링크나 생성기 입력을 통한 script/HTML 주입
- GitHub Actions 권한 확대 또는 신뢰되지 않은 코드 실행
- symlink·경로 탈출·ZIP 오염으로 저장소 밖 파일을 패키징하는 문제
- 채용 공고 데이터에 원문·연락처·민감정보를 과도하게 복제하는 문제
- orphan branch 정본을 다른 위치에서 덮어써 공급망·정본을 혼동시키는 문제

## 보고 방법

공개 이슈에 secret이나 악용 가능한 세부 정보를 적지 않는다. GitHub 저장소의 **Private vulnerability reporting / Security advisory** 기능으로 비공개 보고한다. 해당 기능이 아직 활성화되지 않았다면 저장소를 공개하기 전에 먼저 활성화하고, 활성화 전에는 보안 세부 정보를 게시하지 않는다.

## 대응 원칙

1. 노출된 credential은 문서 삭제보다 **폐기·회전**을 먼저 수행한다.
2. 영향 branch와 package manifest를 확인한다.
3. 공개 이력에서 제거가 필요한 경우 별도의 이력 재작성 절차를 사용하고, 사용자가 다시 fetch/clone해야 하는 범위를 공지한다.
4. 수정 뒤 `make build`, `make check`, `make package`를 다시 실행한다.
5. 보안 이슈의 원인과 재발 방지 설정을 `docs/10-DECISIONS.md`에 일반화해 남기되 secret 자체는 기록하지 않는다.

## 지원 범위

이 임시 저장소는 최종 확정 뒤 read-only archive가 된다. archive 이후 발견한 문제는 실제 정본인 `42`, `guides` 또는 독립 프로젝트 저장소에서 처리한다.
