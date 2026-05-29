# Defect List — Magic Square 4×4

| 항목 | 내용 |
|---|---|
| Document ID | DEF-MSQ-001 |
| Status | Active |
| Version | 1.1 |
| Date | 2026-05-29 |
| Reference | `docs/test_plan.md`, `docs/PRD_MagicSquare.md`, `docs/contracts.md` |
| Sprint | FR-01 AC-01 RED (Track A / A-2) |

---

## Open Defects

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-01 | 1. `cd MagicSquare_XX` 2. `.venv` 활성화 3. `python -m pytest tests/boundary/test_fr01_ac01_boundary_validator.py -v` 4. `matrix=None` 테스트 수집 시도 | `BoundaryValidator` import 성공 → `validate(None)` → `ErrorResponse` code=`INPUT_SIZE_INVALID`, message=`Input matrix must be 4x4.` | `ModuleNotFoundError: No module named 'boundary'` (collection ERROR) | `src/boundary/` production 패키지 미구현 (`boundary_validator.py`, `models.py` 없음) | `src/boundary/` 생성: `BoundaryValidator.validate()`, `ErrorResponse`, `INPUT_SIZE_INVALID` 반환 (GREEN) |
| DEF-002 | Critical | AC-01 | 1. `python -m pytest tests/boundary/test_fr01_ac01_error_contract.py -v` | §13 Pydantic `ErrorResponse` 스키마 검증 통과 | `ModuleNotFoundError: No module named 'boundary'` | DEF-001과 동일 — `boundary.models` 미존재 | DEF-001 수정과 동일 (`models.py` + `ErrorResponse`) |
| DEF-003 | Critical | AC-05, AC-23 | 1. `python -m pytest tests/control/test_fr01_ac05_ac23_use_case_isolation.py -v` 2. `matrix=None` 격리 테스트 수집 시도 | `SolveMagicSquareUseCase.execute(None)` → Domain/Formatter **0-call**, `INPUT_SIZE_INVALID` 반환 | `ModuleNotFoundError: No module named 'boundary'` (첫 import에서 중단) | `src/control/`, `src/entity/`, `src/boundary/result_formatter.py` 미구현 | `SolveMagicSquareUseCase` + DI stub, FR-01 실패 시 조기 return 및 Domain/Formatter 미호출 |
| DEF-004 | High | AC-01 | 1. DEF-001~003 해결 후 2. `python -m pytest tests/boundary/ -k matrix_none -v` | business error 시 **예외 throw 없음**, `ErrorResponse` 객체만 반환 (FR-01, §13) | (GREEN 전 검증 필요) `NotImplementedError` 또는 미처리 예외 가능성 | Boundary에서 `None`/invalid matrix 예외 미처리 설계 | `validate()`가 `ErrorResponse` 반환; `raise` 금지 (test `test_matrix_none_returns_error_without_exception`) |
| DEF-005 | Medium | — | 1. `python -m pytest tests/legacy/ --cov=legacy --cov-fail-under=80` | 전역 gate **80%+** (실습 §6) | `Coverage failure: total of 79% is less than fail-under=80` (테스트 5 passed) | `legacy/entity/user.py` 일부 분기 미커버 (lines 38, 50, 82-84, 104) | `activate()` 등 미호출 경로 테스트 추가 또는 legacy 범위에서 gate 제외 |
| DEF-006 | Low | — | 1. `python -m pytest tests/entity/ -v` | Track B Domain RED 테스트 존재 | `collected 0 items` (README만 존재) | FR-02~05a RED 미착수 | `tests/entity/`에 Track B 테스트 추가 (별도 Sprint) |

---

## RED 단계 참고 (의도적 실패)

| ID | RED 상태 | 설명 |
|---|---|---|
| DEF-001~003 | **의도적 RED** | production 미구현 → `ModuleNotFoundError`가 정상. GREEN Sprint에서 Close 예정 |
| DEF-005 | 범위 외 | Magic Square FR-01과 무관한 `legacy/` User 샘플 커버리지 |
| DEF-006 | 계획됨 | `tests/entity/`는 Track B Sprint에서 채움 |

---

## Test Run Snapshot (2026-05-29)

```text
pytest tests/
  tests/legacy/     5 passed
  tests/boundary/   3 ERROR  (ModuleNotFoundError: boundary)
  tests/control/    (included in boundary ERROR set)
  tests/entity/     0 collected
```

---

## Closed Defects

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — |

---

## Regression Checklist

- [ ] DEF-001~003 Close (GREEN: `src/boundary`, `src/control`, `src/entity` 구현)
- [ ] `python -m pytest tests/boundary/ tests/control/ -m p0` — ERROR 없이 실행 (FAIL/PASS 단계)
- [ ] AC-01: `matrix=None` → `INPUT_SIZE_INVALID` (예외 throw 없음)
- [ ] AC-05, AC-23: Domain + `ResultFormatter` mock `assert_not_called()`
- [ ] DEF-005 처리 또는 legacy gate 예외 문서화
- [ ] Closed 항목을 상단 Open → Closed 테이블로 이동

---

## Revision History

| Version | Date | Summary |
|---|---|---|
| 1.0 | 2026-05-29 | Initial template |
| 1.1 | 2026-05-29 | FR-01 RED 결함 DEF-001~006 등록 (PRD AC-01/05/23) |
