# GC-032 — Full coverage gate

| 필드 | 값 |
|------|-----|
| **GC-ID** | GC-032 |
| **날짜** | 2026-05-29 |
| **브랜치** | `stabilize/green` |
| **Phase** | `docs` |

## Gate results (`.venv`)

| Gate | 명령 | 결과 |
|------|------|------|
| Boundary ≥85% | `pytest tests/boundary/ --cov=src/boundary --cov-fail-under=85` | **98.63%** — 23 passed |
| Entity ≥95% | `pytest tests/entity/ --cov=src/entity --cov-fail-under=95` | **96.55%** — 15 passed |
| Global ≥80% | `pytest tests/boundary/ tests/control/ tests/entity/ --cov=src --cov-fail-under=80` | **95.77%** — 43 passed |

## Full suite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/boundary/ tests/control/ tests/entity/ -v
# 43 passed
```

Legacy (`tests/legacy/`) — 5 passed, gate 범위 외.

## HTML

```powershell
.\.venv\Scripts\python.exe -m pytest tests/boundary/ tests/control/ tests/entity/ --cov=src --cov-report=html
# htmlcov/index.html
```
