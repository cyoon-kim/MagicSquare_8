# Test Coverage Guide — 실습 · PRD 정렬

| 항목 | 내용 |
|---|---|
| Document ID | COV-MSQ-001 |
| 실습 자료 | 커버리지 §6 (pytest-cov) |
| PRD | NFR-01 Domain 95%+, NFR-02 Boundary 85%+ |
| ECB 폴더 | **`src/entity/`** = Domain Logic (실습 용어 Entity) |

---

## 1. 실습 vs 프로젝트 용어 (싱크 표)

| 실습 안내 | 본 저장소 경로 | 비고 |
|---|---|---|
| `src/boundary/` | `src/boundary/` | FR-01, FR-05b |
| `src/entity/` | `src/entity/` | FR-02~05a Domain Logic (**`domain` 아님**) |
| `src/control/` | `src/control/` | FR-06 Orchestration |
| `tests/boundary/` | `tests/boundary/` | Track A |
| `tests/entity/` | `tests/entity/` | Track B Domain RED |
| `tests/control/` | `tests/control/` | Track A-2 격리 |
| — | `tests/legacy/` | User 샘플만 (실습 Domain **아님**) |
| — | `legacy/entity/` | 구 `src/entity/user.py` (RED 범위 밖) |

> 이전에 문서에만 `src/domain/` 으로 적혀 있던 부분은 **실습 ECB `entity` 레이어**와 동일합니다.

---

## 2. 사전 준비 (최초 1회)

```bash
pip install pytest pydantic pytest-cov
```

또는:

```bash
pip install -e ".[dev]"
```

---

## 3. 전체 커버리지 (기본)

```bash
python -m pytest --cov=src --cov-report=term-missing
```

---

## 4. Boundary 테스트 + Boundary 레이어 커버리지

```bash
python -m pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing
```

**목표:** Boundary **85%+** (PRD NFR-02)

### Boundary cov 정책 (QA-RISK-007 — REFACTOR item 2)

`src/boundary/screen/` (PyQt6) 는 현재 단위 테스트 없음 → 전체 boundary gate 시 **~38% FAIL**.

**결정 (2026-05-29):** REFACTOR Sprint gate에서는 **`screen/` omit** — core boundary 모듈만 85% gate 적용.  
Screen smoke/cov는 R3/R11 이후 별도 정책 검토.

**Gate (core boundary only — screen omit):**

```bash
python -m coverage run --source=src/boundary --omit="src/boundary/screen/*" -m pytest tests/boundary/ -q
python -m coverage report --fail-under=85
```

**Full boundary (참고 — 현재 FAIL 예상):**

```bash
python -m pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing --cov-fail-under=85
```

---

## 5. Domain(Entity) 테스트 + Domain 커버리지

```bash
python -m pytest tests/entity/ --cov=src/entity --cov-report=term-missing
```

**목표:** Domain Logic **95%+** (PRD NFR-01)

> `tests/legacy/` 는 User 튜토리얼용이며, 위 명령에 **포함하지 않습니다.**

---

## 6. 커버리지 하한선 강제 (gate)

```bash
# Boundary gate (85%)
python -m pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing --cov-fail-under=85

# Domain gate (95%) — control 포함 시 (실습 안내)
python -m pytest tests/entity/ --cov=src/entity --cov=src/control --cov-report=term-missing --cov-fail-under=95

# 전역 gate (80%) — 실습 기본 gate
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## 7. Sprint AC-01 (현재) 참고

| Sprint | Boundary | Entity (Domain) | Control |
|---|---|---|---|
| AC-01 RED | import ERROR (의도) | 미작성 | import ERROR (의도) |
| AC-01 GREEN 후 | ≥85% | **호출 0회** (격리만) | ≥85% early-return |
| FR-02~05a | — | ≥95% | — |

AC-01 단계에서 `tests/entity/` 가 비어 있으면 `pytest tests/entity/` 는 **0 tests collected** 가 정상입니다.

---

## 8. pytest 설정 (`pyproject.toml`)

- `pythonpath = ["src"]` — `src` 만 path에 추가 (`tests/boundary` 가 `boundary` 패키지로 가로채지 않도록)
- `addopts = "--import-mode=importlib"` — 위와 동일 목적

RED 확인: `ModuleNotFoundError: No module named 'boundary'` → production 미구현 **정상**.
