# Test Plan — FR-01 Input Size Validation (AC-01)

| 항목 | 내용 |
|---|---|
| Document ID | TP-MSQ-FR01-AC01-001 |
| Status | Draft |
| Version | 1.0 |
| Date | 2026-05-29 |
| Author Role | Senior QA Lead |
| Reference PRD | `docs/PRD_MagicSquare.md` — FR-01, AC-01, AC-05, AC-23, §12.1, §13 |
| Reference Contracts | `docs/contracts.md` — API Single Source of Truth |
| Sample Example | Null 입력 → `INPUT_SIZE_INVALID` (Boundary 조기 종료) |
| Stack | Python 3.13+, pytest, pydantic, unittest.mock |
| Terminology | Public parameter: **`matrix`** (not `grid`) |

---

## 1. Purpose & Scope

본 테스트 계획서는 **Dual-Track TDD Track A**의 선행 RED 범위인 **FR-01 Input Verification — AC-01(4×4 크기 검증)** 을 pytest 단위 테스트로 검증하기 위한 계획이다.

### 1.1 In-Scope

| Layer | Component | 검증 대상 |
|---|---|---|
| Boundary | `BoundaryValidator` | 입력 행렬 크기/존재 검증, 표준 에러 객체 반환 |
| Control | `SolveMagicSquareUseCase` | FR-01 실패 시 Domain chain 미호출 (AC-23) |
| Contract | Pydantic error model | `{ "error": { "code", "message" } }` 스키마 준수 |

### 1.2 Out-of-Scope (본 계획서)

| 항목 | 사유 |
|---|---|
| AC-02~04 (빈칸 개수, 값 범위, 중복) | 별도 TS-E-02~04 계획서로 분리 |
| **4×4 정상 입력 (TD-01, TD-02)** | AC-01 범위 외 — 본 계획에 **포함 금지** |
| Domain 로직 (FR-02~05a) | Track B 별도 계획 |
| ResultFormatter (FR-05b) | 입력 통과 후 Track A 후속 RED |

---

## 2. Traceability

| Concept | Business Rule | Feature | AC | Test Scenario | Component |
|---|---|---|---|---|---|
| 4×4 입력 | BR-01 | FR-01 | AC-01 | TS-E-01 | `BoundaryValidator` |
| 입력 실패 Domain 미호출 | BR-01 | FR-01, FR-06 | AC-05, AC-23 | TS-E-01 | `SolveMagicSquareUseCase` |

### 2.1 Sample Example (Baseline RED)

| Field | Value |
|---|---|
| **AC ID** | AC-01 (연계: AC-05, AC-23) |
| **PRD Reference** | FR-01, §12.1 Input Contract, §13 Error Policy |
| **Input** | `matrix = None` |
| **Expected Output** | `{ "error": { "code": "INPUT_SIZE_INVALID", "message": "Input matrix must be 4x4." } }` |
| **Side Effect** | Domain Resolver **0회** 호출 |

### 2.2 Test ID Mapping (README ↔ test_plan ↔ PRD)

| README | test_plan | PRD RED / TS | AC | Input (`matrix`) |
|---|---|---|---|---|
| TC-A-01 | TC-FR01-01 / BV-01 | (AC-01 extension) | AC-01 | `None` |
| TC-A-02 | TC-FR01-01 | — | AC-01 | code assertion |
| TC-A-03 | TC-FR01-01 | — | AC-01 | message assertion |
| TC-A-04 | TC-FR01-01 | — | AC-05,23 | `None` + Domain spy |
| TC-A-05 | TC-FR01-02 / BV-02 | (AC-01 extension) | AC-01 | `[]` |
| TC-A-06 | TC-FR01-03 / BV-03 | (AC-01 extension) | AC-01 | `[[]]*4` |
| TC-A-07 | TC-FR01-04~06 / BV-04~06 | TS-E-01, RED-BND-VAL-004 | AC-01 | 3×4, 4×3, 5×5, TD-03 |
| TC-A-08 | TC-FR01-01 | §13 | AC-01 | ErrorResponse schema |
| TC-A-09 | — | — | — | TD-01 excluded |
| TC-A2-01 | TC-FR01-01 | — | AC-05,23 | Control Domain 0-call |
| TC-A2-02 | TC-FR01-01 | — | AC-23 | ResultFormatter 0-call |

---

## 3. pytest Unit Test Scope & Priority

### 3.1 Test Pyramid (본 Sprint)

```
P0  BoundaryValidator 단위 (격리)     ← AC-01 직접 검증
P1  SolveMagicSquareUseCase + mock    ← AC-23 Domain 미호출 검증
P2  ErrorResponse Pydantic contract   ← §13 스키마 고정
P3  Parametrize 경계값 일괄 실행      ← 회귀·누락 방지
```

### 3.2 Recommended File Layout

| Priority | File | Target | Pattern |
|---|---|---|---|
| **P0** | `tests/boundary/test_boundary_validator_size.py` | `BoundaryValidator.validate()` | AAA, `@pytest.mark.parametrize` |
| **P1** | `tests/control/test_use_case_domain_isolation.py` | `SolveMagicSquareUseCase.execute()` | AAA + `unittest.mock` |
| **P2** | `tests/boundary/test_error_contract.py` | Pydantic `ErrorResponse` model | schema assertion |
| — | `tests/conftest.py` | 공통 fixture | function scope |

### 3.3 Execution Order (RED → GREEN)

1. **RED-1 (P0):** `matrix=None` 단일 케이스 — 최소 선행 조건 실패 확인
2. **RED-2 (P0):** 경계값 parametrize 전체 — AC-01 커버리지 확장
3. **RED-3 (P1):** UseCase + Domain mock — AC-05/AC-23 격리 검증
4. **GREEN:** `BoundaryValidator` 최소 구현 → P0 통과
5. **GREEN:** UseCase 조기 종료 분기 → P1 통과
6. **REFACTOR:** 검증 로직 추출, 테스트·계약 유지

### 3.4 pytest Markers (권장)

| Marker | Usage |
|---|---|
| `@pytest.mark.boundary` | Track A — Boundary layer tests |
| `@pytest.mark.control` | Control layer / orchestration tests |
| `@pytest.mark.p0` | Release gate — must pass |
| `@pytest.mark.parametrize("matrix", [...])` | AC-01 경계값 일괄 실행 |

---

## 4. Boundary Value Cases (AC-01)

> **공통 기대 결과:** 모든 케이스는 동일한 표준 에러를 반환한다.  
> `{ "error": { "code": "INPUT_SIZE_INVALID", "message": "Input matrix must be 4x4." } }`

| ID | Input (`matrix`) | Invalid Reason | AC | Included |
|---|---|---|---|---|
| **BV-01** | `None` | 명시적 None — 행렬 미제공 | AC-01 | ✅ |
| **BV-02** | `[]` | 빈 리스트 — 행 0개 | AC-01 | ✅ |
| **BV-03** | `[[]] * 4` | 행 4개 존재, 각 행 열 0개 | AC-01 | ✅ |
| **BV-04** | `3×4` 행렬 (행 3, 열 4) | 행 수 불일치 | AC-01 | ✅ |
| **BV-05** | `4×3` 행렬 (행 4, 열 3) | 열 수 불일치 | AC-01 | ✅ |
| **BV-06** | `5×5` 행렬 (행 5, 열 5) | 행·열 모두 불일치 | AC-01 | ✅ |
| **BV-07** | `4×4` 정상 입력 (TD-01) | 유효 입력 | — | ❌ **포함 금지** |

### 4.1 Concrete Input Fixtures

```text
BV-01:  None
BV-02:  []
BV-03:  [[], [], [], []]
BV-04:  [[1,2,3,4], [5,6,7,8], [9,10,11,12]]          # 3 rows × 4 cols
BV-05:  [[1,2,3], [4,5,6], [7,8,9], [10,11,12]]       # 4 rows × 3 cols
BV-06:  5×5 zero-padded or arbitrary int grid
BV-07:  TD-01 matrix (§16.4) — OUT OF SCOPE
```

### 4.2 PRD Cross-Reference

| Case | PRD Test Data | Notes |
|---|---|---|
| BV-04~06 | TD-03 (`[[1,2],[3,4]]`) 계열 | TD-03은 2×2; 본 계획은 3×4, 4×3, 5×5로 확장 |
| BV-01 | PRD 미명시 | null 입력 — AC-01 최선행 실패 케이스 |
| BV-02, BV-03 | PRD 미명시 | 구조적 degenerate case — 구현 방어 검증 |

---

## 5. Exception & Special Cases

| ID | Category | Input / Condition | Expected Behavior | Rationale |
|---|---|---|---|---|
| **EX-01** | Null reference | `matrix = None` | `INPUT_SIZE_INVALID`, Domain 0회 | Baseline RED (Sample Example) |
| **EX-02** | Empty container | `matrix = []` | `INPUT_SIZE_INVALID`, Domain 0회 | IndexError 방지, 조기 반환 |
| **EX-03** | Ragged row (empty cols) | `[[]] * 4` | `INPUT_SIZE_INVALID`, Domain 0회 | 행 수만 맞고 열 수 0 |
| **EX-04** | Ragged row (mixed col len) | `[[1,2,3,4], [1,2], [1,2,3,4], [1,2,3,4]]` | `INPUT_SIZE_INVALID`, Domain 0회 | 비직사각형 행렬 |
| **EX-05** | Non-list type | `matrix = "invalid"` | `INPUT_SIZE_INVALID`, Domain 0회 | 타입 계약 위반 |
| **EX-06** | Non-list row element | `matrix = [1, 2, 3, 4]` | `INPUT_SIZE_INVALID`, Domain 0회 | 1차원 리스트 |
| **EX-07** | Exception policy | 모든 EX 케이스 | **예외 throw 금지** — 에러 객체만 반환 | §13, FR-01 Error Policy |
| **EX-08** | Message determinism | 동일 code 반복 호출 | message 항상 동일 (영문 고정) | §13 Message policy |
| **EX-09** | Input immutability | invalid matrix 전달 후 | 원본 `matrix` 변경 없음 | BR-14, NFR-04 |
| **EX-10** | Idempotency | 동일 invalid matrix 2회 호출 | 동일 error code/message | NFR-03 replay |

---

## 6. Domain Solver Entry-Point Call Count Verification

### 6.1 Domain Entry Points (Spy Targets)

FR-01 실패 시 **아래 Domain 컴포넌트 및 ResultFormatter는 0회** 호출되어야 한다 (AC-05, AC-23).

| Spy Target | Layer | FR | Mock Path (예시) |
|---|---|---|---|
| `BlankFinder.find()` | Domain | FR-02 | `entity.blank_finder.BlankFinder.find` |
| `MissingNumberFinder.find()` | Domain | FR-03 | `entity.missing_number_finder.MissingNumberFinder.find` |
| `MagicSquareValidator.is_valid()` | Domain | FR-04 | `entity.magic_square_validator.MagicSquareValidator.is_valid` |
| `Solver.solve()` | Domain | FR-05a | `entity.solver.Solver.solve` |
| `ResultFormatter.format()` | Boundary | FR-05b | `boundary.result_formatter.ResultFormatter.format` |

Control 진입점:

| Spy Target | Layer | FR | Mock Path (예시) |
|---|---|---|---|
| `SolveMagicSquareUseCase.execute()` | Control | FR-06 | 테스트 대상 (Act) |

### 6.2 Strategy A — BoundaryValidator Unit (P0, No Spy)

- **대상:** `BoundaryValidator.validate(matrix)` 직접 호출
- **검증:** 반환값이 error 객체이며 `code == "INPUT_SIZE_INVALID"`
- **Domain spy:** 불필요 — Boundary 단독 호출로 Domain 의존 없음
- **적용 케이스:** BV-01 ~ BV-06 전체

### 6.3 Strategy B — UseCase Integration + Mock (P1, AC-23)

**목적:** Control 계층이 FR-01 실패 시 Domain chain을 **실제로 호출하지 않음**을 증명.

```python
# Pattern (conceptual — implementation in test files, not this document)
from unittest.mock import MagicMock, patch

# Arrange: inject mock Domain collaborators into UseCase
blank_finder = MagicMock()
missing_finder = MagicMock()
validator = MagicMock()
solver = MagicMock()

use_case = SolveMagicSquareUseCase(
    boundary_validator=BoundaryValidator(),
    blank_finder=blank_finder,
    missing_finder=missing_finder,
    validator=validator,
    solver=solver,
)

# Act
result = use_case.execute(matrix=None)

# Assert — error contract
assert result.error.code == "INPUT_SIZE_INVALID"

# Assert — Domain call count (AC-05, AC-23)
blank_finder.find.assert_not_called()
missing_finder.find.assert_not_called()
validator.is_valid.assert_not_called()
solver.solve.assert_not_called()
result_formatter.format.assert_not_called()
```

### 6.4 Strategy C — patch Spy at Import Site (Alternative)

- `@patch("src.control.solve_magic_square_use_case.BlankFinder")` 형태로 UseCase 내부 resolve 지점에 spy
- **call_count == 0** 또는 `assert_not_called()` 로 검증
- Strategy B(mock injection)가 **선호** — patch 경로 변경에 덜 취약

### 6.5 Verification Matrix

| Test Level | AC | Spy Required | Expected Domain Calls |
|---|---|---|---|
| BoundaryValidator unit | AC-01 | No | N/A (Domain 미참조) |
| UseCase integration | AC-05, AC-23 | Yes (4 Domain + ResultFormatter mocks) | **0** for all BV-01~06 |
| Error contract unit | §13 | No | N/A |

### 6.6 Failure Interpretation

| Observation | Likely Defect |
|---|---|
| Domain mock `call_count > 0` on invalid grid | FR-06 orchestration violation — Domain 호출 순서/조기 종료 누락 |
| Exception raised instead of error object | §13 Error Policy 위반 |
| Different message for same code | Message determinism 위반 (EX-08) |

---

## 7. Pydantic Error Contract Validation (P2)

§13 표준 에러 스키마를 테스트에서 고정 검증한다.

```python
# Conceptual model
class ErrorDetail(BaseModel):
    code: Literal["INPUT_SIZE_INVALID", ...]
    message: str

class ErrorResponse(BaseModel):
    error: ErrorDetail
```

| Assertion | Rule |
|---|---|
| `ErrorResponse.model_validate(result)` | 파싱 성공 |
| `result.error.code == "INPUT_SIZE_INVALID"` | AC-01 |
| `result.error.message == "Input matrix must be 4x4."` | §13 고정 message |

---

## 8. Coverage Targets

| Layer | Target | PRD Reference | Measurement Focus |
|---|---|---|---|
| **Domain** | **≥ 95%** | NFR-01 | Track B (FR-02~05a) — 본 Sprint 후속 |
| **Boundary** | **≥ 85%** | NFR-02 | `BoundaryValidator`, `ResultFormatter` |
| **Control** | ≥ 85% (권장) | FR-06 | `SolveMagicSquareUseCase` 조기 종료 분기 |

### 8.1 AC-01 Sprint Coverage Expectation

본 Sprint(AC-01 RED/GREEN) 완료 시 최소 달성:

| Module | Expected Coverage | Key Branches |
|---|---|---|
| `src/boundary/boundary_validator.py` | ≥ 85% | size check, null/empty/ragged paths |
| `src/control/solve_magic_square_use_case.py` | ≥ 85% | FR-01 fail → early return |
| `src/entity/*` | 0% 호출 (spy) | AC-01 범위 — Domain 코드 미실행 |

> Domain 95%+는 Track B FR-02~05a GREEN 이후 전체 스위트에서 달성한다.

---

## 9. pytest-cov Measurement Strategy

### 9.1 Setup

```bash
pip install pytest-cov
```

### 9.2 Standard Run (Full Suite)

```bash
pytest --cov=src --cov-report=term-missing
```

### 9.3 AC-01 Sprint Focused Run

```bash
# Boundary + Control only (Track A FR-01)
pytest tests/boundary/ tests/control/ \
  --cov=src/boundary \
  --cov=src/control \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### 9.4 Layer-Split Reports

```bash
# Boundary gate
pytest tests/boundary/ \
  --cov=src/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85

# Domain gate (Track B — post FR-02~05a)
pytest tests/entity/ \
  --cov=src/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 9.5 CI Gate Policy (권장)

| Gate | Command Suffix | Threshold |
|---|---|---|
| Boundary | `--cov=src/boundary --cov-fail-under=85` | 85% |
| Domain (Entity) | `--cov=src/entity --cov-fail-under=95` | 95% |
| Full | `--cov=src --cov-report=term-missing` | informational |

### 9.6 Coverage Interpretation Notes

- `term-missing` 출력으로 AC-01 미커버 분기( null vs empty vs ragged )를 RED 추가 대상으로 식별
- Domain 모듈이 AC-01 테스트에서 **실행되지 않음**은 정상 — spy `assert_not_called()` 와 함께 아키텍처 준수 증거
- 커버리지만으로 Pass 판정 금지 — AC-23 Domain 0-call 검증은 mock assertion 필수

---

## 10. Test Case Summary

| Test ID | Priority | Input | Expected Code | Domain Calls | AC |
|---|---|---|---|---|---|
| TC-FR01-01 | P0 | `None` | `INPUT_SIZE_INVALID` | 0 | AC-01,05,23 |
| TC-FR01-02 | P0 | `[]` | `INPUT_SIZE_INVALID` | 0 | AC-01,05,23 |
| TC-FR01-03 | P0 | `[[]]*4` | `INPUT_SIZE_INVALID` | 0 | AC-01,05,23 |
| TC-FR01-04 | P0 | 3×4 matrix | `INPUT_SIZE_INVALID` | 0 | AC-01,05,23 |
| TC-FR01-05 | P0 | 4×3 matrix | `INPUT_SIZE_INVALID` | 0 | AC-01,05,23 |
| TC-FR01-06 | P0 | 5×5 matrix | `INPUT_SIZE_INVALID` | 0 | AC-01,05,23 |
| TC-FR01-07 | P2 | ragged rows | `INPUT_SIZE_INVALID` | 0 | AC-01 |
| TC-FR01-08 | P2 | non-list grid | `INPUT_SIZE_INVALID` | 0 | AC-01 |
| TC-FR01-09 | P2 | repeat call | same code/message | 0 | EX-08, NFR-03 |
| TC-FR01-XX | — | 4×4 valid (TD-01) | success | >0 | **제외** |

---

## 11. Exit Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | BV-01~06 전체 Pass | `pytest tests/boundary/ tests/control/ -m p0` |
| 2 | Domain mock 0-call (AC-23) | P1 integration tests |
| 3 | Boundary coverage ≥ 85% | `pytest-cov --cov-fail-under=85` |
| 4 | 예외 throw 없음 (EX-07) | negative assertion — no `pytest.raises` for business errors |
| 5 | 4×4 정상 입력 테스트 **미포함** | test file grep / review checklist |

---

## 12. Revision History

| Version | Date | Summary |
|---|---|---|
| 1.0 | 2026-05-29 | Initial test plan — FR-01 AC-01 sample (matrix=None), boundary cases, mock strategy, pytest-cov |
| 1.1 | 2026-05-29 | contracts.md alignment: matrix terminology, ID mapping, ResultFormatter spy |
