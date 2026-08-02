# Security policy

## 보고

공개 이슈에 secret·credential·악용 가능한 세부 정보를 쓰지 않는다. GitHub의 Private vulnerability reporting / Security advisory를 사용한다.

## 범위

- `main`과 `guide-*` branch의 workflow·script·실습 dependency
- 예제에 포함된 실제 token·host credential·개인정보
- 외부 명령·파일·archive를 다루는 실습의 path traversal·command injection
- 통합 전후 guide 정본 혼동

가이드 예제는 학습용이므로 운영 제품 보안을 보장하지 않는다. 발견한 문제는 해당 guide branch에서 수정하고 검증 범위와 비범위를 함께 갱신한다.
