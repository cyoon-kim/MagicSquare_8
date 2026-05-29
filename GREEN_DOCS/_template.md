# GC-XXX — {title}

| 필드 | 값 |
|------|-----|
| **GC-ID** | GC-XXX |
| **날짜** | YYYY-MM-DD |
| **Git commit** | `{hash}` — `{message}` |
| **브랜치** | `stabilize/green` |
| **Track** | A / A-2 / B |
| **Test ID** | |
| **Phase** | `test(red)` / `feat(green)` / `docs` / `chore` |

## node id

```text
tests/...::TestClass::test_name
```

## RED before

- 

## GREEN after

- 

## pytest

```powershell
.\.venv\Scripts\python.exe -m pytest "<node id>" -v
```

## coverage (optional)

```powershell
.\.venv\Scripts\python.exe -m pytest ... --cov=src/... --cov-report=term-missing
```

## 변경 파일

- 
