# 위협 모델

## 보호 대상

```text
P/G/L PATH의 정확한 의존 관계
42/guides/standalone의 단일 정본
README·LICENSE·SECURITY와 branch 자체 완결성
채용 공고 정적 데이터의 출처·상태·중복 판정
생성된 그래프·Markdown·ZIP의 무결성
GitHub Actions와 repository 설정의 최소 권한
개인정보·credential의 비노출
```

## 신뢰 경계

| 경계 | 신뢰하는 것 | 신뢰하지 않는 것 |
|---|---|---|
| 제공 PATH | 프로젝트·가이드 명칭과 학습 프레임 | 이후 임의로 추가된 일반 지식 |
| 공개 GitHub 저장소 | 현재 source·README·branch 이름 | 과거 문서의 최신성, 이름만 같은 정본 |
| 채용 공고 | 기준일 당시 원문 표시 | 검색 snippet, 기준일 이후 모집 상태 |
| JSON 데이터 | schema를 통과한 자체 요약 | HTML·script·shell로 실행될 외부 문자열 |
| ZIP 생성 | 검사 통과한 regular file | symlink, `.git`, secret, local cache |
| GitHub Actions | full SHA로 고정한 공식 action과 read-only token | fork 코드에 secret을 주는 workflow, mutable tag |

## 주요 위협과 통제

| 위협 | 결과 | 통제 |
|---|---|---|
| orphan branch와 standalone에 같은 코드 복제 | 수정·보안 패치·링크의 정본 분열 | 단일 정본 표와 중복 금지 검사 |
| `main`이 다른 branch 파일에 상대 의존 | 단독 clone·archive에서 깨짐 | main은 절대 GitHub URL, branch는 내부 상대 링크만 사용 |
| workflow 공급망 변조 | PR 검사 과정에서 token·코드 노출 | action full SHA, read-only permissions, 위험 trigger 금지 |
| secret·개인정보 커밋 | 계정·개인 안전 침해 | `.gitignore`, filename/content 검사, push protection, private reporting |
| Markdown/공고 문자열 주입 | HTML·링크·표 구조 오염 | schema·control character 검사, HTML escaping, HTTPS allowlist |
| path traversal·symlink ZIP | 저장소 밖 파일 포함 | symlink·absolute path·`.git` 거부, deterministic file list |
| 오래된 공고를 활성으로 표시 | 잘못된 지원 판단 | 기준일·status_basis·expired 목록, 지원 직전 재확인 문구 |
| 생성물 수동 편집 | JSON/DOT 정본과 Markdown/SVG 불일치 | `--check`, 생성물 header, atomic write |
| 거대한 binary·cache 포함 | 검토 어려움·악성 payload 은닉 | 크기 상한·binary allowlist·cache/secret 이름 차단 |
| L 레인의 무제한 확장 | 숨은 작업·PATH 지연 | L ID·트리거·회차 범위·P/G 후속 owner 강제 |

## 비범위

- GitHub, 채용 플랫폼 또는 외부 사이트 자체의 침해 대응
- 링크 대상 페이지의 장기 보존
- standalone 프로젝트 코드의 런타임 보안 검토
- 실제 이력서·면접 답변·지원 계정 데이터의 보관
- 법률 자문이나 라이선스 적합성의 최종 법적 판단

비범위가 발견되면 이 저장소에서 해결했다고 주장하지 않고 실제 정본 또는 별도 보안 검토로 이관한다.
