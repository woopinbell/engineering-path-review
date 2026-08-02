# 근거 등록부

## 제공 자료

| 자료 | 사용 범위 |
|---|---|
| 병렬 학습·프로젝트 재구현 PATH 원문 | 레인 원자성, P/G/L 프레임, 프로젝트·가이드 범위, 감사·코딩 테스트 기준 |
| 그래프 중심 PATH 개선본 | 스윔레인 표현과 채용 마일스톤 배치 |
| 42·guides main 문서 세트 초안 | orphan branch 목록, standalone 분류, 라이선스·운영 정책 |
| 기존 engineering path review | P01~P24, G00~G14, 공고 데이터와 검토 구조 |
| 복습용 3트랙 병렬 PATH 논의 | C·C++·WEB 트랙 분리, 트랙 내부 G·P 선형 배치, P만 원자적 완료, 필수 G 비생략 원칙 |

프로젝트·가이드 명칭과 의존 방향은 제공 자료를 기준으로 유지했다. 이번 완전판에서 추가한 L01~L15는 기존의 “코딩 테스트 또는 제한 감사”를 실행 가능한 단위로 명시한 운영 설계다.

## GitHub 저장소 확인

- 저장소 목록: <https://github.com/woopinbell?tab=repositories>
- 프로젝트 표기는 공개 사례집 저장소인 `*-changelog`를 정본 후보로 사용한다.
- `42`와 `guides` branch URL은 최종 저장소 생성 뒤 사용할 예정 URL이다.
- 통합 뒤 과거 개별 저장소는 archive/redirect 후보이며 병렬 정본으로 유지하지 않는다.

## GitHub 보안·운영 공식 문서

| 주제 | 공식 문서 |
|---|---|
| Ruleset에서 사용할 수 있는 규칙 | <https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets> |
| GitHub Actions 허용 정책과 full SHA pin | <https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-github-actions-settings-for-a-repository> |
| Workflow 보안 강화 | <https://docs.github.com/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions> |
| Security policy | <https://docs.github.com/code-security/getting-started/adding-a-security-policy-to-your-repository> |
| Push protection | <https://docs.github.com/code-security/secret-scanning/protecting-pushes-with-secret-scanning> |
| Public repository secret scanning | <https://docs.github.com/code-security/secret-scanning/introduction/supported-secret-scanning-patterns> |
| Private vulnerability reporting | <https://docs.github.com/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository> |
| Dependabot target branch options | <https://docs.github.com/code-security/dependabot/working-with-dependabot/dependabot-options-reference> |
| Scheduled workflow의 default branch 동작 | <https://docs.github.com/actions/using-workflows/events-that-trigger-workflows#schedule> |
| Code scanning workflow와 branch | <https://docs.github.com/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/configuring-advanced-setup-for-code-scanning> |
| actions/checkout release | <https://github.com/actions/checkout/releases/tag/v6.0.2> |

보안 문서는 GitHub 설정이 바뀔 수 있으므로 실제 저장소 공개 직전에 다시 확인한다.

## 채용 공고 조사

채용 공고는 2026-08-03(Asia/Seoul) 기준 정적 스냅숏이다.

```text
공식 채용 페이지 우선
→ 공식 페이지를 확인할 수 없을 때 플랫폼 공고 사용
→ 지원하기/채용 중/상시채용/미래 마감일을 근거로 상태 기록
→ 과거 마감일·마감 버튼·삭제 페이지는 expired/removed로 이동
→ URL과 회사·직무 조합 중복 제거
→ 공고 전문·로고·연락처를 복제하지 않고 자체 요약만 저장
```

원문 URL과 판정 근거는 [`data/jobs-2026-08-03.json`](../data/jobs-2026-08-03.json)에 있다. 기준일 이후 상태는 보장하지 않는다.

## 분석 판단

다음은 외부 source가 직접 선언한 사실이 아니라 PATH·저장소·공고를 대조해 내린 운영 판단이다.

```text
P14를 일반 첫 지원 경계로 삼는 결정
공고별 최소 PATH와 즉시/조건부/향후 등급
L을 트리거 기반 작업 큐로 구체화한 설계
C·C++·WEB 3트랙 안에 가이드 구간과 프로젝트를 교차 배치한 복습용 실행 설계
orphan/standalone 분류와 보안 trade-off
review repository의 디렉터리·검사·패키징 구조
```

분석 판단은 source-derived 사실과 구분해 [결정 기록](10-DECISIONS.md)에 남긴다.
