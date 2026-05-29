# MagicSquare 진행 보고서 — Dual-Track RED 설계 · Skeleton · pytest 검증

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare 4x4 TDD Practice |
| **문서 ID** | RPT-MSQ-DUAL-RED-009 |
| **날짜** | 2026-05-29 |
| **브랜치** | `feature/dual-track-tdd` (권장) |
| **TDD 단계** | **RED** — 설계표 + Skeleton (GREEN/REFACTOR 미착수) |
| **Production 코드** | `src/boundary`, `src/control`, `src/entity` **미구현** |
| **대응 Transcript** | `Prompt/09_MagicSquare_DualTrack_RED_Skeleton_transcript.md` |

---

## 1. 작업 개요

FR-01~FR-05 **Dual-Track UI + Logic TDD** 범위에 대해 다음을 순차 수행했다.

| # | 단계 | 산출 | 상태 |
|---|------|------|------|
| 1 | RED 설계표 (Track A/B) | Plan · 본 보고서 §4~5 | 완료 |
| 2 | RED Skeleton pytest | `tests/boundary/test_u_*.py`, `tests/entity/test_d_*.py` | 완료 |
| 3 | `.venv` pytest 전체 실행 | §6 결과 고정 | 완료 |
| 4 | Report/09 · Prompt/09 Export | 본 문서 · Transcript | 완료 |

**원칙:** Skeleton은 `pytest.fail("RED: …")`만 사용 — assert 기대값·skip·xfail·`src/` stub 없음.  
Report/07 Full RED (`test_fr01_ac01_*`, `test_fr01_ac05_*`)는 **수정하지 않음**.

---

## 2. SSOT 참조

| 문서 | 역할 |
|------|------|
| `docs/PRD_MagicSquare.md` v1.1 | FR-01~06, AC, TD-01~07, 에러 코드 |
| `docs/contracts.md` | `matrix`, `INPUT_*`, ECB API |
| `docs/test_plan.md` | FR-01 AC-01, BV, mock 전략 |
| `Report/02_MagicSquare_DualTrack_UI_Logic_TDD_CleanArchitecture.md` | Dual-Track · Invariant (일부 Superseded 배너) |
| `.cursorrules` | ECB, pytest AAA, RED-GREEN-REFACTOR |
| `.cursor/rules/magicsquare-tdd-testing.mdc` | importlib, 커버리지 gate |

**설계 별칭 E00x → PRD 런타임 코드**

| 설계 | PRD `error.code` |
|------|------------------|
| E003 (null) | `INPUT_SIZE_INVALID` (short-circuit 1순위) |
| E001 (size) | `INPUT_SIZE_INVALID` |
| E002 (blank count) | `INPUT_BLANK_COUNT_INVALID` |
| E004 (range) | `INPUT_VALUE_RANGE_INVALID` |
| E005 (duplicate) | `INPUT_DUPLICATE_NON_ZERO` |

---

## 3. 고정 격자 (G0~G3)

Report/02 부록 미정의 → 본 스프린트 placeholder (`tests/entity/conftest.py` 주석).

| ID | 용도 | 요약 |
|----|------|------|
| **G0** | D-VAL-01, U-IN-07 | 완전 4×4 마방진, `0` 없음, M=34 |
| **G1** | D-LOC/MIS/SOL, U-OUT | 빈칸 1-index (2,2),(3,3); 누락 {7,10}; 기대 `[2,2,7,3,3,10]` |
| **G2** | D-SOL-02 | PRD TD-02 (Step B) — Skeleton: `G2 TBD` |
| **G3** | D-SOL-03 | PRD TD-07 dual fail |

---

## 4. Track A — Boundary/UI RED 설계 · Skeleton

### 4.1 Full RED (Report/07, 중복 금지)

| Test ID | 파일 | 상태 |
|---------|------|------|
| U-IN-01~03 (AC-01 size/null) | `test_fr01_ac01_boundary_validator.py` | collection **ERROR** |
| AC-01 error schema | `test_fr01_ac01_error_contract.py` | collection **ERROR** |
| AC-05/23 isolation | `test_fr01_ac05_ac23_use_case_isolation.py` | collection **ERROR** |

### 4.2 Skeleton RED (본 스프린트 신규)

| Test ID | 테스트 함수 | 파일 |
|---------|-------------|------|
| U-IN-04 | `test_u_in_04_negative_value_returns_e004` | `test_u_in_04_08_input_validation.py` |
| U-IN-05 | `test_u_in_05_value_17_returns_e004` | 동일 |
| U-IN-06 | `test_u_in_06_duplicate_non_zero_returns_e005` | 동일 |
| U-IN-07 | `test_u_in_07_zero_blank_cells_returns_e002` | 동일 |
| U-IN-08 | `test_u_in_08_three_blanks_returns_e002` | 동일 |
| U-OUT-01 | `test_u_out_01_success_result_length_is_six` | `test_u_out_01_03_output_contract.py` |
| U-OUT-02 | `test_u_out_02_coordinates_are_one_indexed_in_range` | 동일 |
| U-OUT-03 | `test_u_out_03_g1_step_a_success_payload` | 동일 |
| U-FLOW-02 | `test_u_flow_02_*` (5 cases) | `test_u_flow_02_domain_isolation_extended.py` |

**Skeleton 규칙:** production import 주석 · AAA 주석 · `pytest.fail` 1줄. U-FLOW/U-OUT은 Control `Solver.solve` mock/spy **주석만**.

---

## 5. Track B — Domain/Logic RED 설계 · Skeleton

**Domain Mock 금지** (실 Grid + Entity API만 Full RED에서 사용).

| Test ID | 테스트 함수 | 파일 |
|---------|-------------|------|
| D-LOC-01 | `test_d_loc_01_g1_row_major_blank_coords` | `test_d_loc_01_blank_coords.py` |
| D-MIS-01 | `test_d_mis_01_g1_missing_numbers_sorted` | `test_d_mis_01_missing_numbers.py` |
| D-VAL-01~06 | `test_d_val_01` … `test_d_val_06` | `test_d_val_01_06_magic_square_validator.py` |
| D-SOL-01 | `test_d_sol_01_g1_step_a_success_int_six` | `test_d_sol_01_04_two_cell_solver.py` |
| D-SOL-02 | `test_d_sol_02_g2_step_b_reverse_success` | 동일 (`G2 TBD`) |
| D-SOL-03 | `test_d_sol_03_g3_dual_fail_unsolvable` | 동일 |
| D-SOL-04 | `test_d_sol_04_g1_result_length_six` | 동일 |

---

## 6. pytest 실행 결과 (`.venv`)

**명령**

```powershell
cd MagicSquare_XX
.venv\Scripts\python.exe -m pytest tests/ -v --tb=no --continue-on-collection-errors
```

**환경:** Python 3.13.9, pytest 9.0.3, pytest-cov 7.1.0

| 결과 | 건수 | 비고 |
|------|------|------|
| **PASSED** | 5 | `tests/legacy/test_user_entity.py` (범위 외) |
| **FAILED** | 25 | Skeleton — 의도적 `pytest.fail` |
| **ERROR** | 3 | Full RED — `ModuleNotFoundError: No module named 'boundary'` |
| **passed (Magic Square src)** | 0 | `src/` 미구현 |

### 6.1 ERROR 상세

| 파일 | 원인 |
|------|------|
| `test_fr01_ac01_boundary_validator.py` | `from boundary.boundary_validator import …` |
| `test_fr01_ac01_error_contract.py` | 동일 |
| `test_fr01_ac05_ac23_use_case_isolation.py` | `boundary` / `control` / `entity` 미존재 |

### 6.2 Skeleton만 실행 (참고)

```powershell
.venv\Scripts\python.exe -m pytest `
  tests/boundary/test_u_in_04_08_input_validation.py `
  tests/boundary/test_u_out_01_03_output_contract.py `
  tests/boundary/test_u_flow_02_domain_isolation_extended.py `
  tests/entity/test_d_loc_01_blank_coords.py `
  tests/entity/test_d_mis_01_missing_numbers.py `
  tests/entity/test_d_val_01_06_magic_square_validator.py `
  tests/entity/test_d_sol_01_04_two_cell_solver.py -v
```

→ **25 failed, 0 passed** (정상 RED Skeleton)

---

## 7. 생성 파일 목록

| 경로 | 설명 |
|------|------|
| `tests/boundary/test_u_in_04_08_input_validation.py` | U-IN-04~08 |
| `tests/boundary/test_u_out_01_03_output_contract.py` | U-OUT-01~03 |
| `tests/boundary/test_u_flow_02_domain_isolation_extended.py` | U-FLOW-02 확장 |
| `tests/entity/conftest.py` | G0~G3 주석 placeholder |
| `tests/entity/test_d_loc_01_blank_coords.py` | D-LOC-01 |
| `tests/entity/test_d_mis_01_missing_numbers.py` | D-MIS-01 |
| `tests/entity/test_d_val_01_06_magic_square_validator.py` | D-VAL-01~06 |
| `tests/entity/test_d_sol_01_04_two_cell_solver.py` | D-SOL-01~04 |
| `Report/09_MagicSquare_DualTrack_RED_Skeleton_Test_Report.md` | 본 보고서 |
| `Prompt/09_MagicSquare_DualTrack_RED_Skeleton_transcript.md` | 대화 Transcript |

**미변경:** `test_fr01_ac01_*`, `test_fr01_ac05_*`, `src/`, `tests/legacy/*`

---

## 8. RED 설계 검수 체크리스트

- [x] Boundary Failure envelope (`INPUT_*`, generic Exception 아님)
- [x] invalid → Domain solve 0회 (U-FLOW-02 설계·Skeleton)
- [x] U-IN / U-OUT / U-FLOW 분리
- [x] Logic Track Domain Mock 없음
- [x] I1~I11 · AC-FR(PRD AC) 추적 가능
- [x] Skeleton 단계: assert 기대값 없음, `pytest.fail` only

---

## 9. 다음 권장 작업

1. **Skeleton → Full RED:** 각 `pytest.fail`을 AAA + assert로 교체 (import 해제).
2. **GREEN Track A:** `src/boundary/` `BoundaryValidator` + `models.py` — U-IN-04~08, FR-01 AC-02~04.
3. **GREEN Track A-2:** `SolveMagicSquareUseCase` — U-FLOW-02, AC-05/23.
4. **GREEN Track B:** `src/entity/` FR-02~05a — D-LOC ~ D-SOL (G2 확정 후 D-SOL-02).
5. `docs/defect_list.md` DEF-001~006 갱신 · 커버리지 gate (`docs/coverage_guide.md`).

---

*본 문서는 Dual-Track RED 설계·Skeleton·pytest 검증 세션 산출 보고서이다.*
