# RED Implementation Checklist — Status

> **2026-05-29:** Track A/B GREEN + REFACTOR Sprint (items 1–7) **완료**.  
> 본 문서는 초기 RED 스프린트 체크리스트의 **이력 보존** 및 현재 상태 요약입니다.

---

## Completed — Documentation

- [x] [`docs/contracts.md`](contracts.md) v1.1 — SSOT `src/contracts/errors.py`
- [x] [`docs/test_plan.md`](test_plan.md) — FR-01 baseline + Appendix B full scope
- [x] [`docs/defect_list.md`](defect_list.md) — DEF Close, QA-RISK 추적
- [x] [`docs/refactor-plan.md`](refactor-plan.md) — R1~R12 백로그
- [x] [`docs/coverage_guide.md`](coverage_guide.md) — boundary omit 정책 (QA-RISK-007)
- [x] [`README.md`](../README.md) — REFACTOR 7항목 체크리스트

---

## Completed — Implementation (GREEN Sprint)

- [x] `src/contracts/errors.py` — shared DTO + §13 codes (R1)
- [x] `src/boundary/` — BoundaryValidator, ResultFormatter (FR-05b), models re-export
- [x] `src/control/` — SolveMagicSquareUseCase, ports, factory (R2/R3)
- [x] `src/entity/` — BlankFinder, MissingNumberFinder, Validator, Solver (FR-02~05a)
- [x] `tests/boundary/` · `tests/control/` · `tests/entity/` — Track A/B P0
- [x] GM-1 Golden Master (GM-TC-01~05)
- [x] PyQt6 Screen (`src/boundary/screen/`)

---

## Completed — REFACTOR Sprint (R1~R12)

| Item | ID | Status |
|---|---|---|
| 숫자 상수 SSOT | R7 | ✅ |
| 선행 게이트 (AC-22 RED, NFR-04, cov 정책) | §14 | ✅ |
| ECB 구조 (contracts, ports, factory) | R1~R3 | ✅ |
| ResultFormatter FR-05b | R4 | ✅ |
| Solver 단일 API + UseCase slim | R5~R6 | ✅ |
| 테스트 위생 (fixture, docstring, logging) | R8~R11 | ✅ |
| 문서 SSOT | R12 | ✅ |

---

## Open / Out of Scope

| ID | 항목 | 비고 |
|---|---|---|
| DEF-005 | legacy 커버리지 79% | gate 제외 또는 테스트 추가 |
| QA-RISK-007 | screen/ cov smoke | omit 정책 적용 중 |
| QA-RISK-009 | stale docs | R12로 해소 |
| QA-RISK-010 | Solver type annotation | Low — 후속 |
| DOMAIN_MAGIC_UNCHECKABLE | AC-15 | 범위 외 (REFACTOR plan) |

---

## Historical — Original RED Steps (superseded)

<details>
<summary>Pending Step 1~5 (2026-05-29 초기 — 모두 완료됨)</summary>

- Step 1 legacy/ 이동 — 완료
- Step 2 Cursor rules — `magicsquare-*.mdc` 적용
- Step 3 pyproject.toml — dev/gui extras
- Step 4 src skeleton — GREEN Sprint에서 구현
- Step 5 RED tests — P0 55+ GM-1 6

</details>

---

## Verify GREEN + REFACTOR

```bash
pip install -e ".[dev]"
python -m pytest tests/boundary/ tests/control/ tests/entity/ tests/contracts/ -m p0 -v
python -m pytest tests/test_gm_01_magic_square_golden_master.py -v
```
