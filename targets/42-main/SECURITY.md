# Security policy

## 보고

공개 이슈에 secret·credential·악용 가능한 세부 정보를 쓰지 않는다. GitHub의 Private vulnerability reporting / Security advisory를 사용한다. 기능이 비활성화돼 있으면 저장소 공개 전에 먼저 활성화한다.

## 범위

- `main`과 `42` orphan branch의 workflow·script·dependency·링크
- accidentally committed token, private key, 개인정보
- standalone 정본과 orphan branch 사이의 정본 혼동
- branch 보호 우회, force push, 잘못된 base PR

standalone 프로젝트의 런타임 취약점은 각 독립 저장소에서 보고한다.

## credential 노출

노출된 값은 즉시 폐기·회전하고 영향 branch와 package를 확인한다. Git 이력 삭제만으로 credential이 안전해졌다고 판단하지 않는다.
