# PRD — Magic Square 4x4 TDD Practice

| 항목 | 내용 |
|---|---|
| Document ID | PRD-MSQ-4X4-001 |
| Target Path | `docs/PRD_MagicSquare.md` |
| Status | Reviewed Draft |
| Version | 1.1 |

---

## 1. Executive Summary

Magic Square 4x4 TDD Practice는 정답 생성 알고리즘 경쟁이 아니라, **불변식 기반 사고**, **입력/출력 계약 고정**, **Boundary/Domain 분리**, **Dual-Track UI + Logic TDD**, **RED-GREEN-REFACTOR**, **Concept-to-Code Traceability**를 훈련하는 구현 전 기준 문서이다. 본 PRD는 4x4 정수 행렬(빈칸 2개)을 입력으로 받아, 누락 숫자 2개를 두 가지 배치 순서로 시도한 뒤 마방진 조건을 만족하는 결과를 `int[6]`(1-index 좌표)로 반환하거나, 계약 위반·해 없음 시 표준 에러를 반환하는 동작을 정의한다.

---

## 2. Background

학습자는 구현을 먼저 시작하고 테스트 기준을 나중에 정의하는 패턴을 반복한다. 그 결과 다음 문제가 발생한다.

- 성공 기준이 “합이 맞음”으로 축소되어 숫자 집합·중복·좌표 규칙이 누락된다.
- Boundary 검증과 Domain 판정이 혼합되어 리팩토링 시 계약이 깨진다.
- 동일 입력에 대한 출력이 실행마다 달라질 수 있다.

본 프로젝트는 UI/DB/Web 없이 순수 로직과 테스트로 위 문제를 통제한다.

---

## 3. Problem Statement

본 프로젝트의 문제는 “4x4 마방진을 만든다”가 아니다. 문제는 다음이다.

1. 4x4 입력에 대한 **검증 가능한 불변식 집합**을 정의한다.
2. 입력 계약 위반을 **Boundary에서 차단**한다.
3. Domain은 **순수 판정·탐색·조합 시도**만 수행한다.
4. 출력 계약(`int[6]`, 1-index, Attempt 순서)을 고정한다.
5. 실패 응답을 **단일 표준 에러 스키마**로 고정한다.

---

## 4. Why Now / Why Chain

| Why | 학습자 문제 | 본 PRD가 닫는 것 |
|---|---|---|
| Why #1 | “완성” 정의가 합 일치만으로 축소됨 | 다중 불변식(크기, 빈칸, 범위, 중복, 합 34)을 분리 정의 |
| Why #2 | 수기 검증은 누락·중복·대각선 혼동 발생 | 결정적 자동 판정 계약 고정 |
| Why #3 | 구현 중 요구가 표류함 | 테스트 가능 AC와 Traceability로 명세 선행 |
| Why Now | Boundary/Domain 혼합, 리팩토링 회귀 | Dual-Track TDD와 계층 분리 강제 |

---

## 5. Target Users

| User Type | Goal | Environment |
|---|---|---|
| TDD 학습자 | RED-GREEN-REFACTOR 습관 확립 | `pytest` 실행 |
| 코드 리뷰어 | 계약·불변식·책임 분리 검증 | PR/리뷰 |
| Architecture 학습자 | ECB + Clean Architecture 경계 훈련 | 콘솔 또는 테스트 러너 |

**범위 밖 환경:** UI 화면, DB, Web/API, 외부 서비스.

---

## 6. Vision & Epic Goal

**Vision:** 불변식 기반 사고와 계약 기반 개발을 반복 가능하게 학습하는 훈련 시스템.

**Epic Goal:** `입력 계약 → Domain 불변식 판정 → 출력 계약` 흐름을 Dual-Track TDD로 고정하고, REFACTOR 이후에도 계약·검증 기준이 변하지 않게 한다.

---

## 7. Persona

### P-01 TDD Beginner Developer
- Pain: 구현 선행, 테스트 사후 작성
- Need: 실패 테스트를 요구사항 명세로 사용

### P-02 Architecture Learner
- Pain: Boundary/Domain 책임 혼합
- Need: 의존 방향 `Boundary → Control → Domain` 유지

### P-03 Refactoring-focused Practitioner
- Pain: 리팩토링 후 출력/에러 회귀
- Need: Concept→Test→Component 추적성

---

## 8. User Journey Summary

| Stage | Pain Point | Learning Outcome |
|---|---|---|
| 1. 문제 인식 | “정답만 맞으면 됨” | 불변식 집합으로 문제 재정의 |
| 2. 계약 정의 | I/O가 구현 중 변경됨 | 입력/출력/에러 계약 선고정 |
| 3. 도메인 분리 | 검증·포맷·판정 혼합 | Boundary vs Domain 책임 분리 |
| 4. Dual-Track TDD | UI/Logic 테스트 혼선 | Track A/B 병렬 RED 운용 |
| 5. 회귀 보호 | 리팩토링 후 스펙 흔들림 | Traceability + 회귀 테스트 유지 |

---

## 9. Scope

### 9.1 In-Scope
- 빈칸 좌표 탐색 (row-major)
- 누락 숫자 탐색 (2개, 오름차순)
- 마방진 판정 (행/열/두 대각선, 상수 34)
- 두 조합 시도 및 결과 반환
- Boundary 입력 검증 및 출력 포맷 검증
- Dual-Track TDD 검증 가능 요구사항

### 9.2 Out-of-Scope
- UI 화면, DB, Web/API, N×N 일반화
- 완전 생성 알고리즘, 인증/권한, 네트워크, QR, 외부 연동

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary / Track A)

- **Description:** 입력 행렬 계약 위반을 Boundary에서 판정하고 Domain 호출을 차단한다.
- **Layer:** Boundary
- **Input:** `int[][] matrix`
- **Processing Rules:** BR-01~BR-04 검사
- **Output:** `pass` 또는 표준 에러 객체
- **Acceptance Criteria:**
  - **AC-01:** 행 또는 열 수가 4가 아니면 `INPUT_SIZE_INVALID`를 반환한다.
  - **AC-02:** `0` 개수가 2가 아니면 `INPUT_BLANK_COUNT_INVALID`를 반환한다.
  - **AC-03:** `0` 또는 `1~16` 밖 값이 있으면 `INPUT_VALUE_RANGE_INVALID`를 반환한다.
  - **AC-04:** `0` 제외 값이 중복되면 `INPUT_DUPLICATE_NON_ZERO`를 반환한다.
  - **AC-05:** AC-01~04 실패 시 Domain Resolver를 호출하지 않는다.
- **Error / Exception Policy:** 표준 에러 객체 반환 (예외 throw 금지)
- **Related Business Rules:** BR-01, BR-02, BR-03, BR-04
- **Related Test Direction:** TS-E-01~04, Track A
- **Component Candidate:** `BoundaryValidator`

### FR-02 Blank Coordinate Discovery (Domain / Track B)

- **Description:** 두 빈칸 좌표를 row-major 순서로 탐색한다.
- **Layer:** Domain
- **Input:** FR-01을 통과한 `matrix` (원본 불변)
- **Processing Rules:** BR-05
- **Output:** 내부 좌표 2쌍 — **0-index**
- **Acceptance Criteria:**
  - **AC-06:** `0`인 칸이 정확히 2개이면 2좌표를 반환한다.
  - **AC-07:** 첫 번째 빈칸은 row-major 스캔에서 최초 발견 `0` 좌표이다.
  - **AC-08:** 두 번째 빈칸은 row-major 스캔에서 두 번째 발견 `0` 좌표이다.
- **Error / Exception Policy:** `DOMAIN_BLANK_COUNT`
- **Related Business Rules:** BR-02, BR-05
- **Related Test Direction:** TS-B-03, `RED-DOM-BLK-001`
- **Component Candidate:** `BlankFinder`

### FR-03 Missing Number Discovery (Domain / Track B)

- **Description:** 누락 숫자 2개를 계산하고 오름차순으로 반환한다.
- **Layer:** Domain
- **Input:** FR-01 통과 `matrix`
- **Processing Rules:** BR-06, BR-07
- **Output:** `[small, large]`
- **Acceptance Criteria:**
  - **AC-09:** 누락 숫자 개수는 정확히 2이다.
  - **AC-10:** 반환 순서는 오름차순이다 (`small < large`).
- **Error / Exception Policy:** `DOMAIN_MISSING_COUNT`
- **Related Business Rules:** BR-06, BR-07
- **Related Test Direction:** TS-B-01, TS-B-02, `RED-DOM-MIS-001`, `RED-DOM-MIS-002`
- **Component Candidate:** `MissingNumberFinder`

### FR-04 Magic Square Validation (Domain / Track B)

- **Description:** 0이 없는 후보 격자의 마방진 여부를 판정한다.
- **Layer:** Domain
- **Input:** `0`이 없는 `4x4` 후보 행렬
- **Processing Rules:** BR-08, BR-09
- **Output:** `true` 또는 `false`
- **Acceptance Criteria:**
  - **AC-11:** 4개 행 합이 모두 34이면 행 조건을 만족한다.
  - **AC-12:** 4개 열 합이 모두 34이면 열 조건을 만족한다.
  - **AC-13:** 주대각선·부대각선 합이 각각 34이면 대각선 조건을 만족한다.
  - **AC-14:** AC-11, AC-12, AC-13을 모두 만족할 때만 `true`를 반환한다.
  - **AC-15:** `0`이 1개 이상 포함되면 `false`를 반환하고 `DOMAIN_MAGIC_UNCHECKABLE`로 처리한다.
- **Error / Exception Policy:** AC-15는 Domain 내부 실패 코드
- **Related Business Rules:** BR-08, BR-09
- **Related Test Direction:** `RED-DOM-VAL-001~003`
- **Component Candidate:** `MagicSquareValidator`

### FR-05a Two-Combination Solver (Domain / Track B)

- **Description:** Attempt 1(small-first) 후 실패 시 Attempt 2(reverse)를 수행한다.
- **Layer:** Domain
- **Input:** FR-01 통과 `matrix`, FR-02 좌표, FR-03 `[small, large]`
- **Processing Rules:** BR-10, BR-11
- **Output (Domain 내부):** `(row0, col0, n1, row1, col1, n2)` — **0-index**
- **Acceptance Criteria:**
  - **AC-16:** Attempt 1이 마방진이면 Attempt 1 배치를 선택한다.
  - **AC-17:** Attempt 1 실패, Attempt 2 성공이면 Attempt 2 배치를 선택한다.
  - **AC-18:** Attempt 1·2 모두 실패하면 `DOMAIN_NO_MAGIC_ASSIGNMENT`를 반환한다.
- **Error / Exception Policy:** AC-18은 Domain 실패 코드; Boundary가 표준 에러로 변환
- **Related Business Rules:** BR-10, BR-11
- **Related Test Direction:** TS-N-01, TS-N-02, TS-E-05
- **Component Candidate:** `Solver`

### FR-05b Result Format Validation (Boundary / Track A)

- **Description:** Domain 성공 결과를 외부 출력 계약 `int[6]`(1-index)로 변환·검증한다.
- **Layer:** Boundary
- **Input:** FR-05a Domain 성공 결과(0-index)
- **Processing Rules:** BR-12, BR-13; `external = internal + 1`
- **Output:** `[r1, c1, n1, r2, c2, n2]`
- **Acceptance Criteria:**
  - **AC-19:** 반환 배열 길이는 6이다.
  - **AC-20:** `r1,c1,r2,c2`는 각각 1~4 범위이다.
  - **AC-21:** `n1,n2`는 FR-03의 누락 숫자 2개와 일치한다.
  - **AC-22:** AC-19~21 위반 시 `OUTPUT_FORMAT_INVALID`를 반환한다.
- **Error / Exception Policy:** 포맷 위반은 Boundary 에러; Domain 재호출 금지
- **Related Business Rules:** BR-12, BR-13
- **Related Test Direction:** TS-B-04, TS-B-05, `RED-BND-OUT-001`, `RED-BND-OUT-002`
- **Component Candidate:** `ResultFormatter`

### FR-06 Orchestration (Control)

- **Description:** 호출 순서 고정: `BoundaryValidator → Domain chain → ResultFormatter`.
- **Layer:** Control
- **Acceptance Criteria:**
  - **AC-23:** FR-01 실패 시 Domain 컴포넌트를 호출하지 않는다.
  - **AC-24:** FR-05a 실패 시 `int[6]` 성공 포맷을 반환하지 않는다.
- **Component Candidate:** `SolveMagicSquareUseCase`

---

## 11. Business Rules / Domain Rules

| ID | Rule (항상 참) |
|---|---|
| BR-01 | 입력은 항상 4x4 `int` 행렬이다. |
| BR-02 | `0`(빈칸)은 항상 정확히 2개이다. |
| BR-03 | 각 값은 항상 `0` 또는 `1~16`이다. |
| BR-04 | `0` 제외 숫자는 항상 중복되지 않는다. |
| BR-05 | 첫 번째 빈칸은 row-major 최초 `0`이다. |
| BR-06 | 누락 숫자는 항상 정확히 2개이다. |
| BR-07 | 누락 숫자 반환 순서는 항상 오름차순이다. |
| BR-08 | Magic Constant는 항상 `34`이다 (`MAGIC_CONSTANT_4X4`). |
| BR-09 | 4행, 4열, 주대각선, 부대각선의 각 합은 항상 34이다. |
| BR-10 | Solver는 항상 Attempt 1을 먼저 수행한다. |
| BR-11 | Attempt 1 실패 시 Solver는 항상 Attempt 2를 수행한다. |
| BR-12 | 외부 출력 좌표는 항상 1-index이다. |
| BR-13 | 외부 출력 형식은 항상 `int[6]`이다. |
| BR-14 | 처리 중 입력 `matrix` 원본은 항상 변경하지 않는다. |

**좌표 체계:** Domain 내부 0-index, 외부 출력 1-index (`ResultFormatter` 변환).

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field | Type | Rule | Valid | Invalid | Error Code |
|---|---|---|---|---|---|
| `matrix` | `int[4][4]` | 4행 4열 | TD-01 | TD-03 | `INPUT_SIZE_INVALID` |
| blank count | derived | `0` = 2 | TD-01 | TD-04 | `INPUT_BLANK_COUNT_INVALID` |
| value range | cell | `0` or `1~16` | TD-01 | TD-05 | `INPUT_VALUE_RANGE_INVALID` |
| uniqueness | derived | non-zero unique | TD-01 | TD-06 | `INPUT_DUPLICATE_NON_ZERO` |

### 12.2 Output Contract

| Field | Type | Rule | Valid | Invalid | Policy |
|---|---|---|---|---|---|
| success | `int[6]` | `[r1,c1,n1,r2,c2,n2]` | TD-01 | len≠6 | `OUTPUT_FORMAT_INVALID` |
| coordinates | `int` | 1~4 | TD-01 | r=0 | `OUTPUT_FORMAT_INVALID` |
| failure | error object | 표준 스키마 | TD-07 | mixed | §13 |

---

## 13. Error / Failure Policy

**스키마:** `{ "error": { "code": string, "message": string } }`  
**Message:** 영문 고정, 동일 code = 동일 message.

| Failure Case | Error Code | Message | Origin | Presentation | Domain 호출 | AC |
|---|---|---|---|---|---|---|
| 4x4 아님 | `INPUT_SIZE_INVALID` | `Input matrix must be 4x4.` | Boundary | Boundary | 금지 | AC-01,05,23 |
| 빈칸 2개 아님 | `INPUT_BLANK_COUNT_INVALID` | `Input must contain exactly two blanks (0).` | Boundary | Boundary | 금지 | AC-02,05,23 |
| 값 범위 위반 | `INPUT_VALUE_RANGE_INVALID` | `Input values must be 0 or between 1 and 16.` | Boundary | Boundary | 금지 | AC-03,05,23 |
| 0 제외 중복 | `INPUT_DUPLICATE_NON_ZERO` | `Non-zero values must be unique.` | Boundary | Boundary | 금지 | AC-04,05,23 |
| 두 조합 실패 | `DOMAIN_NO_MAGIC_ASSIGNMENT` | `No valid magic-square assignment exists for the two missing numbers.` | Domain | Boundary | 허용 | AC-18,24 |
| 출력 포맷 위반 | `OUTPUT_FORMAT_INVALID` | `Output must be an int array of length 6 with 1-index coordinates.` | Boundary | Boundary | 금지 | AC-22 |
| Domain blank 불일치 | `DOMAIN_BLANK_COUNT` | `Domain blank count invariant violated.` | Domain | Boundary | 허용 | AC-06 |
| Domain missing 불일치 | `DOMAIN_MISSING_COUNT` | `Domain missing number count invariant violated.` | Domain | Boundary | 허용 | AC-09 |
| Magic check 불가 | `DOMAIN_MAGIC_UNCHECKABLE` | `Magic validation requires a grid without blanks.` | Domain | Boundary | 허용 | AC-15 |

**두 조합 실패:** 예외 throw 없이 `DOMAIN_NO_MAGIC_ASSIGNMENT` 에러 객체 반환.

---

## 14. Non-Functional Requirements

| ID | Requirement | Verification |
|---|---|---|
| NFR-01 | Domain coverage ≥ 95% | coverage report |
| NFR-02 | Boundary coverage ≥ 85% | coverage report |
| NFR-03 | 동일 입력 → 동일 출력/에러 | replay test |
| NFR-04 | 입력 matrix 원본 불변 | mutation test |
| NFR-05 | 단일 실행 ≤ 50ms | perf smoke |
| NFR-06 | Boundary/Domain 분리 | arch review |
| NFR-07 | unnamed magic number 금지 | static review |
| NFR-08 | `34` = `MAGIC_CONSTANT_4X4` | code review |

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
- FR-01, FR-05b, FR-06 RED
- 입력 실패 시 Domain 미호출 RED 필수

### 15.2 Track B — Domain / Logic TDD
- FR-02~05a RED
- TS-N-01, TS-N-02, TS-E-05 RED 필수

### 15.3 Parallel Progression Rules
- UI/Logic RED 분리, GREEN 최소 구현, REFACTOR만 구조 개선
- Domain 완성 후 Boundary 일괄 연결 금지
- 테스트 약화·삭제 금지

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios

| ID | Description | Data | Expected |
|---|---|---|---|
| TS-N-01 | small-first 성공 | TD-01 | `[1,2,3,1,4,13]` |
| TS-N-02 | reverse 성공 | TD-02 | `[1,1,16,1,2,3]` |

### 16.2 Exception Scenarios

| ID | Description | Data | Expected Error |
|---|---|---|---|
| TS-E-01 | 4x4 아님 | TD-03 | `INPUT_SIZE_INVALID` |
| TS-E-02 | 빈칸 개수 | TD-04 | `INPUT_BLANK_COUNT_INVALID` |
| TS-E-03 | 값 범위 | TD-05 | `INPUT_VALUE_RANGE_INVALID` |
| TS-E-04 | 중복 | TD-06 | `INPUT_DUPLICATE_NON_ZERO` |
| TS-E-05 | dual fail | TD-07 | `DOMAIN_NO_MAGIC_ASSIGNMENT` |

### 16.3 Boundary Scenarios

| ID | Description | Data |
|---|---|---|
| TS-B-01 | min value 1 | TD-01 |
| TS-B-02 | max value 16 | TD-02 |
| TS-B-03 | `0` = blank only | TD-01 |
| TS-B-04 | 1-index coords | TD-01, TD-02 |
| TS-B-05 | array length 6 | TD-01 |

### 16.4 Representative Test Data

**TD-01 — small-first 성공**

```text
[[16, 0,  2,  0 ],
 [ 5, 10, 11,  8 ],
 [ 9,  6,  7, 12 ],
 [ 4, 15, 14,  1 ]]
Blanks (0-index): (0,1), (0,3)
Missing: [3, 13]
Expected: [1, 2, 3, 1, 4, 13]
```

**TD-02 — reverse 성공**

```text
[[ 0,  0,  2, 13 ],
 [ 5, 10, 11,  8 ],
 [ 9,  6,  7, 12 ],
 [ 4, 15, 14,  1 ]]
Blanks: (0,0), (0,1)
Missing: [3, 16]
Expected: [1, 1, 16, 1, 2, 3]
```

**TD-03:** `[[1,2],[3,4]]`  
**TD-04:** 완성 격자(0 없음)  
**TD-05:** `17` 포함  
**TD-06:** `8` 중복  
**TD-07 — dual fail (두 조합 모두 non-magic)**

```text
[[14,  1,  5,  9 ],
 [ 8,  7, 16, 12 ],
 [ 6, 10,  2, 11 ],
 [ 0, 13,  4,  0 ]]
Row-major blanks (0-index): (3,0), (3,3)
Missing: [3, 15]
Expected: error DOMAIN_NO_MAGIC_ASSIGNMENT
```

---

## 17. Architecture Overview

| Layer | Responsibility | Must Not |
|---|---|---|
| Boundary | 입력 검증, 에러/출력, 1-index 변환 | Domain 규칙 직접 구현 |
| Control | 호출 순서, 조기 종료 | 마방진 판정 |
| Domain | blank/missing/validate/solve | Boundary/UI/DB/Web/File |

**의존:** `Boundary → Control → Domain`

---

## 18. Component Candidates

| Component | Layer | Related FR | Related Test |
|---|---|---|---|
| `BoundaryValidator` | Boundary | FR-01 | TS-E-01~04 |
| `BlankFinder` | Domain | FR-02 | TS-B-03 |
| `MissingNumberFinder` | Domain | FR-03 | TS-B-01,02 |
| `MagicSquareValidator` | Domain | FR-04 | RED-DOM-VAL-* |
| `Solver` | Domain | FR-05a | TS-N-01,02, TS-E-05 |
| `ResultFormatter` | Boundary | FR-05b | TS-B-04,05 |
| `SolveMagicSquareUseCase` | Control | FR-06 | AC-23,24 |

---

## 19. Risks & Ambiguities

| Risk | Impact | Mitigation |
|---|---|---|
| 0/1-index 혼동 | 좌표 오류 | BR-14, AC-20, TD-01/02 |
| row-major 누락 | Attempt 오류 | BR-05, AC-07/08 |
| TD 혼용 | 분기 무력화 | TS-N-01/02 분리 |
| side effect | 비결정 | NFR-04 |
| Layer 혼합 | 구조 붕괴 | FR-05a/05b 분리 |
| `34` 하드코딩 | 의미 손실 | NFR-08 |

---

## 20. Engineering Principles

- PEP8, Python 3.13+, line length 88
- type hints + Google docstring (public)
- pytest + AAA
- Coverage: Domain 95%+, Boundary 85%+
- ECB: `Boundary → Control → Entity(Domain)`
- RED-GREEN-REFACTOR
- `print()`, bare `except`, 테스트 약화, unnamed magic number 금지

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | AC-01 | TS-E-01 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-02 | TS-E-02 | BoundaryValidator |
| 값 범위 | BR-03 | FR-01 | AC-03 | TS-E-03 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | AC-04 | TS-E-04 | BoundaryValidator |
| 입력 실패 Domain 미호출 | BR-01~04 | FR-01,06 | AC-05,23 | TS-E-01~04 | BoundaryValidator |
| row-major 첫 빈칸 | BR-05 | FR-02 | AC-07 | TS-B-03 | BlankFinder |
| row-major 둘째 빈칸 | BR-05 | FR-02 | AC-08 | TS-B-03 | BlankFinder |
| 누락 2개 | BR-06 | FR-03 | AC-09 | TS-N-01,02 | MissingNumberFinder |
| 누락 오름차순 | BR-07 | FR-03 | AC-10 | TS-N-01,02 | MissingNumberFinder |
| 행 합 34 | BR-09 | FR-04 | AC-11 | TS-N-01,02 | MagicSquareValidator |
| 열 합 34 | BR-09 | FR-04 | AC-12 | TS-N-01,02 | MagicSquareValidator |
| 대각선 합 34 | BR-09 | FR-04 | AC-13 | TS-N-01,02 | MagicSquareValidator |
| small-first | BR-10 | FR-05a | AC-16 | TS-N-01 | Solver |
| reverse | BR-11 | FR-05a | AC-17 | TS-N-02 | Solver |
| dual fail | BR-10,11 | FR-05a | AC-18 | TS-E-05 | Solver |
| int[6] | BR-13 | FR-05b | AC-19 | TS-B-05 | ResultFormatter |
| 1-index | BR-12 | FR-05b | AC-20 | TS-B-04 | ResultFormatter |
| 출력 값 일치 | BR-06,07 | FR-05b | AC-21 | TS-N-01,02 | ResultFormatter |
| 포맷 실패 | BR-12,13 | FR-05b | AC-22 | RED-BND-OUT-001 | ResultFormatter |
| 입력 불변 | BR-14 | FR-06 | NFR-04 | mutation | UseCase |

---

## 22. Open Questions / Decision Needed

현재 본문 요구사항에 Decision Needed 항목 없음 (v1.1).

**Closed (v1.1 — AC-01 extension):** FR-01 AC-01 size validation explicitly includes defensive inputs beyond TD-03: `matrix=None`, `matrix=[]`, `matrix=[[]]*4`, and non-4×4 rectangular matrices (3×4, 4×3, 5×5). See `docs/test_plan.md` BV-01~06 and `docs/contracts.md` §6.

향후 재오픈 가능:
- Message i18n
- TD-07 대체 반례 행렬
- AC-01 P2 defensive checks (ragged rows, non-list type) — see `docs/contracts.md` §6

---

## 23. Appendix

### A. Reference Documents
- `Report/01_MagicSquare_ProblemDefinition_STEP1-5.md`
- `Report/02_MagicSquare_DualTrack_UI_Logic_TDD_CleanArchitecture.md`
- `Report/03_MagicSquare_CursorRules_UserEntity_Progress_Report.md`
- `Report/05_Level5_Scenario_Verification_and_Summary.md`
- `Report/06_MagicSquare_PRD_PreImplementation_Report.md`
- `.cursorrules`, `.cursor/rules/*.mdc`

### B. Gherkin Summary

```gherkin
Scenario: Boundary rejects invalid input without Domain call
  Given a matrix that violates input contract
  When BoundaryValidator validates the matrix
  Then an error code is returned
  And Domain resolver is not invoked

Scenario: small-first success (TD-01)
  Given TD-01 matrix
  When SolveMagicSquareUseCase runs
  Then result equals [1,2,3,1,4,13]

Scenario: reverse success (TD-02)
  Given TD-02 matrix
  When SolveMagicSquareUseCase runs
  Then result equals [1,1,16,1,2,3]

Scenario: dual assignment failure (TD-07)
  Given TD-07 matrix
  When SolveMagicSquareUseCase runs
  Then error code is DOMAIN_NO_MAGIC_ASSIGNMENT
```

### C. RED Test ID ↔ Test Data

| RED ID | Track | Data |
|---|---|---|
| RED-BND-VAL-001 | A | TD-04 |
| RED-BND-VAL-002 | A | TD-06 |
| RED-BND-VAL-003 | A | TD-05 |
| RED-BND-VAL-004 | A | TD-03 |
| RED-DOM-SOL-001 | B | TD-02 |
| RED-DOM-SOL-002 | B | TD-01 |
| RED-DOM-SOL-003 | B | TD-07 |
| RED-BND-OUT-001 | A | malformed output |
| RED-DOM-BLK-001 | B | TD-01 |
| RED-DOM-MIS-001 | B | TD-01 |
| RED-DOM-MIS-002 | B | TD-02 |
| RED-DOM-VAL-001~003 | B | TD-01 completed |

---

## Revision History

| Version | Date | Summary |
|---------|------|---------|
| 1.0 | 2026-05-29 | Initial PRD draft |
| 1.1 | 2026-05-29 | Review fixes: FR split, AC/Matrix, TD data, error policy |
