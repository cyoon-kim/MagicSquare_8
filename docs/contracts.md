# API Contracts — Magic Square 4×4

| 항목 | 내용 |
|---|---|
| Document ID | CTR-MSQ-001 |
| Status | Active |
| Version | 1.0 |
| Authoritative PRD | `docs/PRD_MagicSquare.md` v1.1 |
| Supersedes | `Report/02_...md` §1.4 Domain `validateInput` (validation is **Boundary**) |

---

## 1. Terminology

| Term | Rule |
|---|---|
| Public input parameter | **`matrix`** — PRD §12.1 `int[4][4]` field name |
| Internal Domain parameter | `matrix` (same; avoid `grid` in public API) |
| Layer folders | `src/boundary/`, `src/control/`, `src/domain/` |
| Legacy samples | `legacy/entity/` — outside Magic Square RED scope |

---

## 2. Error Contract (PRD §13)

**Runtime type:** Pydantic models.  
**Serialization:** `model_dump()` must match `{ "error": { "code": string, "message": string } }`.  
**Policy:** Business failures return error objects — **no exception throw**.

### 2.1 Error Codes & Messages (fixed)

| Code | Message |
|---|---|
| `INPUT_SIZE_INVALID` | `Input matrix must be 4x4.` |
| `INPUT_BLANK_COUNT_INVALID` | `Input must contain exactly two blanks (0).` |
| `INPUT_VALUE_RANGE_INVALID` | `Input values must be 0 or between 1 and 16.` |
| `INPUT_DUPLICATE_NON_ZERO` | `Non-zero values must be unique.` |
| `OUTPUT_FORMAT_INVALID` | `Output must be an int array of length 6 with 1-index coordinates.` |
| `DOMAIN_NO_MAGIC_ASSIGNMENT` | `No valid magic-square assignment exists for the two missing numbers.` |

Constants live in `src/boundary/models.py` as `ErrorCode` and `ERROR_MESSAGES`.

---

## 3. Boundary API

### 3.1 `BoundaryValidator`

```python
def validate(matrix: list[list[int]] | None) -> ErrorResponse | None:
    """FR-01. Returns None when input passes size check chain entry;
    ErrorResponse on AC-01~04 failure."""
```

### 3.2 `ResultFormatter` (stub — FR-05b)

```python
def format(result: object) -> list[int] | ErrorResponse:
    ...
```

---

## 4. Control API

### 4.1 `SolveMagicSquareUseCase`

```python
def execute(matrix: list[list[int]] | None) -> list[int] | ErrorResponse:
    """FR-06. Order: BoundaryValidator → Domain chain → ResultFormatter."""
```

**Dependencies (constructor injection):**

- `boundary_validator: BoundaryValidator`
- `blank_finder: BlankFinder`
- `missing_number_finder: MissingNumberFinder`
- `magic_square_validator: MagicSquareValidator`
- `solver: Solver`
- `result_formatter: ResultFormatter`

**AC-01 fail path:** return `ErrorResponse` immediately; Domain + ResultFormatter **must not** be called.

---

## 5. Domain API (stubs — Track B)

| Component | Method | FR |
|---|---|---|
| `BlankFinder` | `find(matrix: list[list[int]]) -> ...` | FR-02 |
| `MissingNumberFinder` | `find(matrix: list[list[int]]) -> ...` | FR-03 |
| `MagicSquareValidator` | `is_valid(matrix: list[list[int]]) -> bool` | FR-04 |
| `Solver` | `solve(matrix, ...) -> ...` | FR-05a |

---

## 6. AC-01 Defensive Inputs (test_plan extension)

Included in Sprint AC-01 RED (PRD §22 closed):

| Input | Expected |
|---|---|
| `None` | `INPUT_SIZE_INVALID` |
| `[]` | `INPUT_SIZE_INVALID` |
| `[[]] * 4` | `INPUT_SIZE_INVALID` |
| 3×4, 4×3, 5×5 | `INPUT_SIZE_INVALID` |
| TD-03 `[[1,2],[3,4]]` (2×2) | `INPUT_SIZE_INVALID` |

P2 (optional same sprint): ragged rows, non-list type, 1D list — all `INPUT_SIZE_INVALID`.

---

## 7. Sprint Coverage Expectations

| Sprint | Boundary | Domain | Control |
|---|---|---|---|
| AC-01 (current) | ≥ 85% | 0 calls (stub OK) | ≥ 85% |
| FR-02~05a (next) | — | ≥ 95% | — |
