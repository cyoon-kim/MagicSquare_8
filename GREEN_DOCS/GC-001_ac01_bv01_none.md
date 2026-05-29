# GC-001 — AC-01 BV-01 matrix=None

| 필드 | 값 |
|------|-----|
| **GC-ID** | GC-001 |
| **날짜** | 2026-05-29 |
| **Git commit** | (소급 — 세션 구현) |
| **브랜치** | `stabilize/green` |
| **Track** | A |
| **Test ID** | BV-01, TC-FR01-01 |
| **Phase** | `feat(green)` |

## node id

```text
tests/boundary/test_fr01_ac01_boundary_validator.py::TestFr01Ac01BoundaryValidator::test_matrix_none_returns_input_size_invalid_code
```

## RED before

- `ModuleNotFoundError: No module named 'boundary'`

## GREEN after

- PASS — `ErrorResponse`, `INPUT_SIZE_INVALID`
- 부수 PASS: `test_matrix_none_message_*`, `test_matrix_none_returns_error_without_exception`, `test_matrix_none_error_matches_prd_section_13_schema`

## pytest

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/boundary/test_fr01_ac01_boundary_validator.py::TestFr01Ac01BoundaryValidator::test_matrix_none_returns_input_size_invalid_code" -v
```

## 변경 파일

- `src/boundary/models.py`, `boundary_validator.py`, `__init__.py` 신규
