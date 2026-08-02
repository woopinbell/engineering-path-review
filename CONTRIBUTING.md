# Contributing

## 변경 단위

한 Pull Request는 다음 중 하나만 다룬다.

```text
PATH 또는 L 레인
42/main 후보
Guides/main 후보
저장소·보안 정책
채용 전략·공고 스냅숏
생성·검사·패키징 도구
```

구현 프로젝트나 가이드 본문 전체를 이 저장소로 복제하지 않는다.

## 작업 순서

```sh
git status --short --branch
make check
# 필요한 파일만 수정
make build
make check
git diff --check
git diff --stat
```

채용 공고는 `data/jobs-2026-08-03.json`만 직접 수정하고 생성된 Markdown은 수동 편집하지 않는다. 그래프는 DOT·Mermaid·텍스트 원본을 먼저 수정한 뒤 `make graphs`로 렌더링한다.

## 보안 규칙

- token, cookie, private key, 이메일·전화번호·주소·생년월일·신분증·이력서 원본을 추가하지 않는다.
- 외부 텍스트를 그대로 HTML이나 shell 명령에 삽입하지 않는다.
- workflow action은 full commit SHA로 고정하고 기본 `GITHUB_TOKEN` 권한을 read-only로 유지한다.
- `pull_request_target`, `workflow_run`, `issue_comment` 기반 코드 실행을 추가하지 않는다.
- symlink, submodule, Git LFS pointer를 이 문서 패키지에 추가하지 않는다.
- 공고 전문·기업 로고·42 subject·평가표를 복제하지 않는다.

## 완료 조건

```sh
make build
make check
make package
```

패키지를 임시 디렉터리에 풀고 그 안에서도 `make check`가 성공해야 한다.
