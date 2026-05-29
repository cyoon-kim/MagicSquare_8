# RED Implementation Checklist — Pending Code Sprint

> 문서 동기화 완료 후, **코드 작성 시** 이 순서대로 진행합니다.  
> Plan mode에서는 `.py` / `.mdc` / `pyproject.toml` 수정이 불가하여 본 문서에 보류 항목을 기록합니다.

---

## Completed (Documentation)

- [x] [`docs/contracts.md`](contracts.md) — API Single Source of Truth
- [x] [`docs/test_plan.md`](test_plan.md) v1.1 — matrix 용어, ID mapping, ResultFormatter spy
- [x] [`docs/defect_list.md`](defect_list.md) — 결함 템플릿
- [x] [`docs/PRD_MagicSquare.md`](PRD_MagicSquare.md) §22 — AC-01 defensive inputs closed
- [x] [`README.md`](../README.md) — Track A / A-2 / B 분리, 상태·구조 갱신
- [x] [`Report/02_...md`](../Report/02_MagicSquare_DualTrack_UI_Logic_TDD_CleanArchitecture.md) — Superseded 배너

---

## Pending Step 1 — legacy/ 이동

```text
src/entity/user.py          → legacy/entity/user.py
tests/entity/test_user_entity.py → tests/legacy/test_user_entity.py
```

`tests/conftest.py`에 legacy path 추가:

```python
LEGACY_PATH = Path(__file__).resolve().parents[1] / "legacy"
if str(LEGACY_PATH) not in sys.path:
    sys.path.insert(0, str(LEGACY_PATH))
```

`src/entity/` 디렉터리 삭제.

---

## Pending Step 2 — Cursor rules (`.cursor/rules/`)

### `magicsquare-ecb-architecture.mdc`

- `entity` → `domain`
- `src/entity/` → `src/domain/`
- `legacy/entity/` · `tests/legacy/` 추가
- Reference: `docs/contracts.md`

### `magicsquare-tdd-testing.mdc`

- Coverage: Boundary **85%+**, Domain **95%+** (80% 제거)
- `matrix` terminology, business error `pytest.raises` 금지
- pytest-cov 명령 예시 추가

---

## Pending Step 3 — `pyproject.toml`

```toml
[project]
name = "magicsquare"
version = "0.1.0"
requires-python = ">=3.13"

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-cov>=5.0", "pydantic>=2.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "p0: release gate",
    "boundary: Track A boundary tests",
    "control: Track A-2 control tests",
]
```

---

## Pending Step 4 — src skeleton (NotImplemented only)

```text
src/boundary/models.py              # ErrorCode, ERROR_MESSAGES, ErrorResponse
src/boundary/boundary_validator.py  # validate() → NotImplementedError
src/boundary/result_formatter.py    # stub
src/control/solve_magic_square_use_case.py  # execute() + DI
src/domain/blank_finder.py
src/domain/missing_number_finder.py
src/domain/magic_square_validator.py
src/domain/solver.py
```

---

## Pending Step 5 — RED tests

```text
tests/conftest.py                   # BV-01~06 matrix fixtures
tests/boundary/test_boundary_validator_size.py   # P0 parametrize
tests/control/test_use_case_domain_isolation.py  # P1 mock injection
tests/boundary/test_error_contract.py            # P2 optional
```

**Verify RED:**

```bash
pip install -e ".[dev]"
pytest tests/boundary tests/control -v   # expect FAIL
```

---

## ID Quick Reference (README ↔ test_plan)

| README | test_plan | Input |
|---|---|---|
| TC-A-01 | TC-FR01-01 / BV-01 | `matrix=None` |
| TC-A2-01 | TC-FR01-01 | Domain 0-call |
| TC-A2-02 | — | ResultFormatter 0-call |

Full mapping: [`test_plan.md` §2.2](test_plan.md)
