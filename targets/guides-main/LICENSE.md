# License policy

Copyright © 2026 woopinbell

이 문서는 `guides` 저장소에서 직접 작성한 자료의 라이선스 범위와 예외를 정한다. 저장소는 서로 공통 조상이 없는 여러 `guide-*` branch를 포함하며, 아래 정책은 명시한 모든 ref의 원저작물에 적용된다. 하나의 guide branch만 archive 또는 `--single-branch` clone으로 배포해도 조건을 확인할 수 있도록 각 branch 루트에 이 문서의 사본 또는 더 구체적인 branch 전용 라이선스를 함께 둔다.

## 1. 문서 — CC BY 4.0

별도 표시가 없는 직접 작성 문서와 설명 자료는 **Creative Commons Attribution 4.0 International (`CC-BY-4.0`)**로 제공한다.

일반적으로 다음 자료가 포함된다.

```text
README, docs, reference와 Markdown·MDX 본문
학습 경로, 용어집, 점검표와 문제 해결 문서
직접 작성한 다이어그램·표·설명용 이미지
예제와 실습의 설명, 상태·불변식·검증 분석
main branch의 가이드 색인과 운영 정책
```

이 라이선스는 공유와 변경을 허용하며, 이용자는 적절한 저작자 표시, 라이선스 링크와 변경 여부를 표시해야 한다. 요약과 정식 조건이 다를 경우 Creative Commons의 legal code가 우선한다.

- 정식 라이선스: <https://creativecommons.org/licenses/by/4.0/>
- 한국어 legal code: <https://creativecommons.org/licenses/by/4.0/legalcode.ko>
- SPDX identifier: `CC-BY-4.0`

권장 표시는 다음과 같다.

```text
Based on work by woopinbell, licensed under CC BY 4.0.
Changes were made: <변경 내용 또는 변경본 링크>.
```

## 2. 소프트웨어 — MIT

별도 표시가 없는 직접 작성 코드와 실행 자료는 아래의 **MIT License (`MIT`)**로 제공한다.

일반적으로 다음 자료가 포함된다.

```text
examples와 projects의 소스 코드
exercises의 skeleton·reference·workspace 생성기
test, fixture, benchmark와 fault-injection 도구
build·verify·automation script
Makefile, CMake, package 설정, Compose와 CI 설정
```

파일별 표기가 필요할 때는 다음 SPDX header를 사용할 수 있다.

```text
SPDX-License-Identifier: MIT
```

## 3. branch별 우선순위

- `main`의 직접 작성 문서에는 `CC-BY-4.0`이 적용된다.
- 각 `guide-*` branch의 직접 작성 설명 자료에는 `CC-BY-4.0`이 적용된다.
- 각 `guide-*` branch의 직접 작성 코드·실습·검증 도구에는 `MIT`가 적용된다.
- branch에 더 구체적인 `LICENSE`, `COPYING`, `NOTICE` 또는 파일별 라이선스 표시가 있으면 그 표시가 해당 자료에 우선한다.

## 4. 인용과 제3자 자료

다음 자료에는 이 문서가 새로운 이용 허락을 부여하지 않는다.

- 표준·RFC·공식 문서·교재·논문에서 인용하거나 번역한 부분
- 외부 라이브러리, vendored source와 generated code
- font, image, icon, dataset, fixture와 sample asset
- 상표, 로고와 제품 명칭
- 다른 기여자가 별도 조건으로 제공한 자료

인용과 제3자 자료에는 가능한 범위에서 출처, 저작권자와 적용 라이선스를 가까운 문서 또는 `NOTICE`에 표시한다. 재배포가 허용되지 않는 원문은 저장소에 복제하지 않고 공식 출처를 연결한다. 라이선스가 확인되지 않은 자료는 이 저장소의 CC BY 또는 MIT 조건으로 다시 허가하지 않는다.

## 5. 기여

별도 합의가 없는 한 이 저장소에 제출한 기여는 자료의 종류에 따라 다음 조건으로 제공하는 데 동의한 것으로 본다.

- 문서·도식 기여: CC BY 4.0
- 코드·예제·실습·자동화 기여: MIT License

기여자는 기여할 권한이 있는 자료만 제출하고, 인용·번역·제3자 코드의 조건을 명시해야 한다. 다른 라이선스가 필요한 기여는 제출 전에 명시적으로 합의한다.

## 6. MIT License 전문

MIT License

Copyright (c) 2026 woopinbell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
