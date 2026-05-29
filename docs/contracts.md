# API Contracts — Magic Square 4×4

| 항목 | 내용 |
|---|---|
| Document ID | CTR-MSQ-001 |
| Status | Active |
| Version | 1.1 |
| Date | 2026-05-29 |
| Authoritative PRD | `docs/PRD_MagicSquare.md` v1.1 |
| Code SSOT | `src/contracts/errors.py` (re-export: `src/boundary/models.py`) |

---

## 1. Terminology

| Term | Rule |
|---|---|
| Public input parameter | **`matrix`** — PRD §12.1 `int[4][4]` field name |
| Internal Domain payload | 0-index `[r,c,n,r,c,n]` from `Solver.solve()` |
| External success output | 1-index `int[6]` from `ResultFormatter.format()` |
| Layer folders | `src/contracts/`, `src/boundary/`, `src/control/`, `src/entity/` |
| Legacy samples | `legacy/entity/` — outside Magic Square RED scope |

---

## 2. Error Contract (PRD §13)

**Runtime type:** Pydantic models in `src/contracts/errors.py`.  
**Serialization:** `model_dump()` → `{ "error": { "code": string, "message": string } }`.  
**Policy:** Business failures return `ErrorResponse` — **no exception throw** on public paths.

### 2.1 Error Codes & Messages (SSOT)

| Code | Message | Layer |
|---|---|---|
| `INPUT_SIZE_INVALID` | `Input matrix must be 4x4.` | Boundary |
| `INPUT_BLANK_COUNT_INVALID` | `Input must contain exactly two blanks (0).` | Boundary |
| `INPUT_VALUE_RANGE_INVALID` | `Input values must be 0 or between 1 and 16.` | Boundary |
| `INPUT_DUPLICATE_NON_ZERO` | `Non-zero values must be unique.` | Boundary |
| `OUTPUT_FORMAT_INVALID` | `Output must be an int array of length 6 with 1-index coordinates.` | Boundary |
| `DOMAIN_BLANK_COUNT` | `Domain blank count invariant violated.` | Domain |
| `DOMAIN_MISSING_COUNT` | `Domain missing number count invariant violated.` | Domain |
| `DOMAIN_NO_MAGIC_ASSIGNMENT` | `No valid magic-square assignment exists for the two missing numbers.` | Domain |

**Python constants:** `{CODE}_CODE` and `{CODE}_MESSAGE` pairs in `contracts.errors`.  
**Backward import:** `from boundary.models import ErrorResponse` re-exports from contracts.

---

## 3. Boundary API

### 3.1 `BoundaryValidator`

```python
def validate(matrix: list[list[int]] | None) -> ErrorResponse | None:
    """FR-01. Returns None when valid; ErrorResponse on AC-01~04 failure."""
```

### 3.2 `ResultFormatter` (FR-05b)

```python
def format(result: list[int] | ErrorResponse) -> list[int] | ErrorResponse:
    """Validate domain int[6] (0-index coords) and convert to external 1-index int[6].
    Returns OUTPUT_FORMAT_INVALID when AC-19~21 violated."""
```

---

## 4. Control API

### 4.1 `SolveMagicSquareUseCase`

```python
def execute(matrix: list[list[int]] | None) -> list[int] | ErrorResponse:
    """FR-06. Order: BoundaryValidator → Solver → ResultFormatter."""
```

**Dependencies (constructor injection):**

- `boundary_validator: MatrixValidatorPort`
- `solver: Solver`
- `result_formatter: ResultFormatterPort`

**Composition root:** `control.factory.build_solve_magic_square_use_case()`

**AC-01 fail path:** return `ErrorResponse` immediately; Solver + ResultFormatter **must not** be called.

---

## 5. Domain API

| Component | Method | Returns | FR |
|---|---|---|---|
| `BlankFinder` | `find(matrix) -> list[tuple[int, int]]` | 0-index blanks, row-major | FR-02 |
| `MissingNumberFinder` | `find(matrix) -> list[int]` | missing 1..16 ascending | FR-03 |
| `MagicSquareValidator` | `is_valid(matrix) -> bool` | complete grid check | FR-04 |
| `Solver` | `solve(matrix) -> list[int] \| ErrorResponse` | 0-index int[6] or domain error | FR-05a |

**Solver policy:** single public method `solve()`; domain failures return `ErrorResponse` (no raise).

---

## 6. Success Output Contract

| Field | Rule |
|---|---|
| Shape | `int[6]` — `[r1,c1,n1,r2,c2,n2]` |
| Coordinates | 1-index, range 1..4 (after `ResultFormatter`) |
| Values | `n1`, `n2` from missing-number assignment |

---

## 7. Regression Gates (REFACTOR merge)

```bash
python -m pytest tests/boundary/ tests/control/ tests/entity/ tests/contracts/ -m p0 -v
python -m pytest tests/test_gm_01_magic_square_golden_master.py -v
python -m pytest tests/entity/ --cov=src/entity --cov-fail-under=95
python -m coverage run --source=src/boundary --omit="src/boundary/screen/*" -m pytest tests/boundary/ -q
python -m coverage report --fail-under=85
```

---

## Revision History

| Version | Date | Summary |
|---|---|---|
| 1.0 | 2026-05-29 | Initial AC-01 sprint contract |
| 1.1 | 2026-05-29 | R12: contracts SSOT, FR-05b/FR-06/R5 parity with implementation |
