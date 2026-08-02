# License policy

Copyright © 2026 woopinbell

이 문서는 `42` 저장소에서 직접 작성한 자료의 라이선스 범위와 예외를 정한다. 저장소는 서로 공통 조상이 없는 여러 Git branch를 포함하므로, 아래 정책은 명시한 모든 ref의 원저작물에 적용된다. 다만 하나의 branch만 archive 또는 `--single-branch` clone으로 배포해도 조건을 확인할 수 있도록 각 과제 branch 루트에 이 문서의 사본 또는 더 구체적인 branch 전용 라이선스를 함께 두어야 한다.

## 1. 적용 범위

### 1.1 문서 — CC BY 4.0

별도 표시가 없는 직접 작성 문서는 **Creative Commons Attribution 4.0 International (`CC-BY-4.0`)**로 제공한다.

문서에는 일반적으로 다음이 포함된다.

```text
README와 Markdown·MDX 본문
architecture·docs·devlog·reference 문서
직접 작성한 다이어그램과 설명용 이미지
프로젝트의 설계·검증·실패 분석 기록
main branch의 색인과 운영 정책
```

이 라이선스는 공유와 변경을 허용하며, 이용자는 적절한 저작자 표시, 라이선스 링크와 변경 여부를 표시해야 한다. 요약문과 법적 조건이 다를 경우 Creative Commons가 제공하는 정식 legal code가 우선한다.

- 정식 라이선스: <https://creativecommons.org/licenses/by/4.0/>
- 한국어 legal code: <https://creativecommons.org/licenses/by/4.0/legalcode.ko>
- SPDX identifier: `CC-BY-4.0`

권장 표시는 다음과 같다.

```text
Based on work by woopinbell, licensed under CC BY 4.0.
Changes were made: <변경 내용 또는 변경본 링크>.
```

### 1.2 소프트웨어 — MIT

별도 표시가 없는 직접 작성 소프트웨어는 아래의 **MIT License (`MIT`)**로 제공한다.

소프트웨어에는 일반적으로 다음이 포함된다.

```text
제품 소스 코드와 공개 헤더
테스트, fixture와 fault-injection 도구
빌드·검증·자동화 스크립트
Makefile, CMake, Compose와 CI 설정
학습용 skeleton·reference 구현
```

파일별 표기가 필요할 때는 다음 SPDX header를 사용할 수 있다.

```text
SPDX-License-Identifier: MIT
```

## 2. branch별 우선순위

- `main`의 직접 작성 문서에는 `CC-BY-4.0`이 적용된다.
- 과제 branch의 직접 작성 소프트웨어에는 `MIT`가 적용된다.
- 과제 branch의 직접 작성 설명 문서에는 `CC-BY-4.0`이 적용된다.
- branch에 더 구체적인 `LICENSE`, `COPYING`, `NOTICE` 또는 파일별 라이선스 표시가 있으면 그 표시가 해당 자료에 우선한다.
- 별도 정본 저장소의 자료에는 이 문서가 아니라 해당 저장소의 라이선스가 적용된다.

## 3. 적용되지 않는 자료

다음 자료에는 이 문서가 새로운 이용 허락을 부여하지 않는다.

- 42 또는 다른 교육기관이 제공한 subject, 평가표, 내부 안내와 원문
- 42, 캠퍼스, 회사, 프로젝트 또는 제3자의 명칭·로고·상표
- 외부 라이브러리, vendored source, font, image, dataset과 sample asset
- 다른 기여자가 별도 조건으로 제공한 코드와 문서
- 공개 저장소에 포함할 권한이 확인되지 않은 자료

이러한 자료가 포함될 수 있는 경우 원본의 저작권 표시와 라이선스를 보존하고, 필요한 `NOTICE`를 함께 제공해야 한다. 라이선스가 확인되지 않거나 재배포 권한이 없다면 저장소에서 제외한다.

## 4. 기여

별도 합의가 없는 한 이 저장소에 제출한 기여는 기여한 자료의 종류에 따라 다음 조건으로 제공하는 데 동의한 것으로 본다.

- 소프트웨어 기여: MIT License
- 문서·도식 기여: CC BY 4.0

기여자는 자신이 해당 기여를 제공할 권한이 있으며 제3자 조건을 침해하지 않는지 확인해야 한다. 다른 라이선스가 필요한 기여는 제출 전에 명시적으로 합의해야 한다.

## 5. MIT License 전문

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
