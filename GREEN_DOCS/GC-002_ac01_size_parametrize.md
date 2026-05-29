# GC-002 — AC-01 size parametrize (BV-02~06, TD-03)

| 필드 | 값 |
|------|-----|
| **GC-ID** | GC-002 |
| **날짜** | 2026-05-29 |
| **브랜치** | `stabilize/green` |
| **Track** | A |
| **Test ID** | BV-02~06, TD-03 |
| **Phase** | `feat(green)` |

## node id

```text
tests/boundary/test_fr01_ac01_boundary_validator.py::TestFr01Ac01BoundaryValidator::test_invalid_size_matrices_return_input_size_invalid_code
```

## RED before

- `assert None is not None` (6 cases)

## GREEN after

- 6 passed — `MATRIX_ORDER_4X4` size check

## pytest

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/boundary/test_fr01_ac01_boundary_validator.py::TestFr01Ac01BoundaryValidator::test_invalid_size_matrices_return_input_size_invalid_code" -v
```

## 변경 파일

- `src/boundary/boundary_validator.py` — `_is_matrix_4x4`, non-4x4 → `INPUT_SIZE_INVALID`
