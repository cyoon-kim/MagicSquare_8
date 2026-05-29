# Defect List — Magic Square 4×4

| 항목 | 내용 |
|---|---|
| Document ID | DEF-MSQ-001 |
| Status | Active |
| Version | 1.2 |
| Date | 2026-05-29 |
| Reference | `docs/test_plan.md`, `docs/PRD_MagicSquare.md`, `docs/contracts.md`, `docs/refactor-plan.md` |
| Sprint | GREEN 완료 → REFACTOR 준비 |

---

## Open Defects

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-005 | Medium | — | 1. `python -m pytest tests/legacy/ --cov=legacy --cov-fail-under=80` | 전역 gate **80%+** (실습 §6) | `Coverage failure: total of 79% is less than fail-under=80` (테스트 5 passed) | `legacy/entity/user.py` 일부 분기 미커버 (lines 38, 50, 82-84, 104) | `activate()` 등 미호출 경로 테스트 추가 또는 legacy 범위에서 gate 제외 |
| QA-RISK-001 | Critical | NFR-06 | `grep "from boundary" src/entity/` | entity → (none) | `solver.py`가 `boundary.models` import | ECB 위반 — 오류 DTO가 boundary에 있음 | R1: `src/contracts/` 분리 (refactor-plan §6 R1) |
| QA-RISK-002 | Critical | NFR-06 | `grep "from entity" src/boundary/screen/app.py` | boundary → control → entity | `app.py`가 entity 직접 import | composition root가 entity wire | R3: factory 분리 (refactor-plan §6 R3) |
| QA-RISK-003 | High | AC-22 | `ResultFormatter.format()` 호출 | len≠6 → `OUTPUT_FORMAT_INVALID` | pass-through만 수행 | FR-05b 미구현 | R4 + RED-BND-OUT-001/002 |
| QA-RISK-004 | High | AC-19~21 | Solver 성공 payload 좌표 | Domain 0-index, Boundary +1 | `solver.py:68` 1-index 반환 | 레이어 책임 혼재 | R4: Formatter가 +1 담당 |
| QA-RISK-005 | High | FR-06 | UseCase `execute()` 호출 | blank/missing finder 결과 활용 | find() 결과 버림, validator 미사용 | dead orchestration | R6 |
| QA-RISK-006 | High | §13 | `Solver.solve()` vs `solve_or_error()` | 단일 error 객체 API | raise + ErrorResponse 이중 API | 설계 미정 | R5 |
| QA-RISK-007 | Medium | NFR-02 | `pytest tests/boundary/ --cov=src/boundary --cov-fail-under=85` | ≥85% | ~38% FAIL (full) | `screen/` 0% | **정책 결정:** core omit gate (coverage_guide §4); smoke는 R3/R11 후 |
| QA-RISK-008 | Medium | — | `grep "print(" src/` | print 없음 | `app.py:44-47` | dev CLI 잔존 | R11 |
| QA-RISK-011 | Low | §13 | `models.py` 오류 코드 목록 | PRD §13 전체 | 4개 코드 미등록 | GREEN Sprint 범위 밖 | R1/R4/R5 |

---

## Closed Defects

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-01 | `pytest tests/boundary/test_fr01_ac01_boundary_validator.py -v` | BoundaryValidator import + validate | (RED) ModuleNotFoundError | boundary 미구현 | GREEN Sprint: `src/boundary/` 구현 완료 |
| DEF-002 | Critical | AC-01 | `pytest tests/boundary/test_fr01_ac01_error_contract.py -v` | ErrorResponse 스키마 | (RED) ModuleNotFoundError | models 미구현 | GREEN Sprint: `models.py` 구현 완료 |
| DEF-003 | Critical | AC-05, AC-23 | `pytest tests/control/test_fr01_ac05_ac23_use_case_isolation.py -v` | UseCase 격리 | (RED) ModuleNotFoundError | control/entity 미구현 | GREEN Sprint: 전체 ECB 구현 완료 |
| DEF-004 | High | AC-01 | `pytest tests/boundary/ -k matrix_none -v` | 예외 throw 없이 ErrorResponse | (RED) 미검증 | boundary 미구현 | GREEN Sprint: business error 객체 반환 확인 |
| DEF-006 | Low | — | `pytest tests/entity/ -v` | Track B Domain 테스트 | (RED) 0 collected | FR-02~05a 미착수 | GREEN Sprint: entity 테스트 15건 추가 |

---

## Test Run Snapshot (2026-05-29, GREEN 기준)

```text
pytest tests/boundary/ tests/control/ tests/entity/ -m p0
  → 43 passed (Report/11)

pytest tests/test_gm_01_magic_square_golden_master.py
  → 6 passed (골든 마스터)

pytest tests/entity/ --cov=src/entity --cov-fail-under=95
  → 96.55% PASS

pytest tests/boundary/ --cov=src/boundary --cov-fail-under=85
  → ~38% FAIL (screen/ 미포함 테스트)
```

---

## Regression Checklist (REFACTOR Sprint)

- [x] DEF-001~004 Close (GREEN 완료)
- [x] DEF-006 Close (entity 테스트 존재)
- [ ] QA-RISK-001~011 — refactor-plan 슬라이스별 Close
- [x] AC-22 RED-BND-OUT-001/002 작성 (R4 선행) — `red_bnd_out` marker, R4 전 FAIL 예상
- [x] NFR-04 matrix 불변성 테스트 — `test_nfr_04_matrix_immutability.py`
- [x] AC-24 UseCase G3 → ErrorResponse — `test_ac_24_g3_failure_no_success_format.py`
- [x] Boundary cov 정책 결정 — `screen/` omit (coverage_guide §4)
- [ ] DEF-005 처리 또는 legacy gate 예외 문서화

---

## Revision History

| Version | Date | Summary |
|---|---|---|
| 1.0 | 2026-05-29 | Initial template |
| 1.1 | 2026-05-29 | FR-01 RED 결함 DEF-001~006 등록 |
| 1.2 | 2026-05-29 | GREEN Close (DEF-001~004, DEF-006); QA-RISK-001~011 Open 등록; refactor-plan 연계 |
