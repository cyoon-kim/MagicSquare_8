# MagicSquare Dual-Track RED Skeleton — Prompt Transcript (Export)

- **Date:** 2026-05-29
- **Project:** Magic Square 4x4 TDD Practice
- **Target Repo:** `MagicSquare_XX/`
- **Scope:** RED 설계표 · RED Skeleton pytest · `.venv` pytest 검증 · Report/09 Export
- **TDD Phase:** RED (설계 + Skeleton only; GREEN/REFACTOR 없음)
- **대응 보고서:** `Report/09_MagicSquare_DualTrack_RED_Skeleton_Test_Report.md`

---

## Turn 01 — Dual-Track RED 설계표 (Plan Mode)

**User**  
Dual-Track UI + Logic TDD 전문가로 **TDD phase: RED** 설계표만 작성.

- 금지: 구현/테스트 코드/스켈레톤, GREEN/REFACTOR, pytest 실행
- SSOT: docs, Report, `.cursorrules`
- Track A: U-IN-*, U-OUT-*, U-FLOW-02 (Boundary, E00x envelope)
- Track B: D-LOC/MIS/VAL/SOL, G0~G3, Domain Mock 금지
- 출력: `# UI RED Tests` / `# Logic RED Tests` 마크다운 표 + 검수 체크리스트

**Assistant**  
- `docs/contracts.md`, `docs/PRD_MagicSquare.md`, `Report/02`, `.cursorrules` 분석
- E00x 설계 별칭 ↔ PRD `INPUT_*` 매핑 정리
- G0~G3 placeholder (G0/G1 격자 수치, G2=TD-02, G3=TD-07)
- Track A 9행 + Track B 14행 설계표 작성 (Plan 문서 저장)
- 검수 체크리스트 6항목 통과 확인

---

## Turn 02 — RED Skeleton 작성 요청

**User**  
**TDD phase: RED (Skeleton)** — Report/09 설계표 기준 테스트 스켈레톤만.

- 금지: `src/` 구현, GREEN, skip/xfail, assert 기대값
- 범위: U-IN-04~08, U-OUT-01~03, U-FLOW-02; D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04
- U-IN-01~03 중복 금지 (Report/08 Full RED 유지)
- naming: `test_<test_id>_<scenario>`
- 본문: `pytest.fail("RED: …")` 한 줄만
- G2: `pytest.fail("RED: D-SOL-02 — G2 TBD")`

**Assistant**  
- Plan mode에서 파일 작성 차단 → Agent mode 전환
- 생성 8파일:
  - `tests/boundary/test_u_in_04_08_input_validation.py`
  - `tests/boundary/test_u_out_01_03_output_contract.py`
  - `tests/boundary/test_u_flow_02_domain_isolation_extended.py`
  - `tests/entity/conftest.py` (G0~G3 주석)
  - `tests/entity/test_d_loc_01_blank_coords.py`
  - `tests/entity/test_d_mis_01_missing_numbers.py`
  - `tests/entity/test_d_val_01_06_magic_square_validator.py`
  - `tests/entity/test_d_sol_01_04_two_cell_solver.py`
- `test_fr01_ac01_*`, `test_fr01_ac05_*` 미수정
- 산출: 파일 목록, Test ID 매핑표, 예상 RED (25 FAIL / import ERROR)

---

## Turn 03 — `.venv` pytest 실행 요약

**User**  
`MagicSquare_XX/` 하위 가상환경에서 테스트 실행 후 결과 요약.

**Assistant**  
```powershell
.venv\Scripts\python.exe -m pytest tests/ -v --tb=no --continue-on-collection-errors
```

**결과 요약**

| 항목 | 수 |
|------|-----|
| PASSED | 5 (`tests/legacy/`) |
| FAILED | 25 (Skeleton `pytest.fail`) |
| ERROR | 3 (Full RED `ModuleNotFoundError: boundary`) |
| Magic Square `src/` 통과 | 0 |

- ERROR: `test_fr01_ac01_boundary_validator.py`, `test_fr01_ac01_error_contract.py`, `test_fr01_ac05_ac23_use_case_isolation.py`
- Skeleton 25건 FAILED = 의도적 RED 정상

---

## Turn 04 — Report · Transcript Export

**User**  
Report 폴더에 보고서 생성, Prompt 폴더에 Transcript Export.

**Assistant**  
- `Report/09_MagicSquare_DualTrack_RED_Skeleton_Test_Report.md` 생성
- `Prompt/09_MagicSquare_DualTrack_RED_Skeleton_transcript.md` 생성 (본 문서)

---

## 부록 — 주요 사용자 규칙 (세션)

| 규칙 | 내용 |
|------|------|
| ECB | boundary → control → entity |
| Dual-Track | Track A 계약 / Track B 로직 분리 |
| RED Skeleton | `pytest.fail` only, no assert on expected values |
| PRD 에러 | Failure envelope, `pytest.raises` 금지 (business error) |
| 커버리지 gate | Global 80%, Boundary 85%, Entity 95% |
| import | `pyproject.toml` `--import-mode=importlib`, `pythonpath=["src"]` |

---

## 부록 — pytest 명령 모음

```powershell
# 전체 (legacy 포함)
.venv\Scripts\python.exe -m pytest tests/ -v --continue-on-collection-errors

# Skeleton만
.venv\Scripts\python.exe -m pytest tests/boundary/test_u_in_04_08_input_validation.py tests/boundary/test_u_out_01_03_output_contract.py tests/boundary/test_u_flow_02_domain_isolation_extended.py tests/entity/test_d_loc_01_blank_coords.py tests/entity/test_d_mis_01_missing_numbers.py tests/entity/test_d_val_01_06_magic_square_validator.py tests/entity/test_d_sol_01_04_two_cell_solver.py -v

# Full RED (src 구현 후)
.venv\Scripts\python.exe -m pytest tests/boundary/ tests/control/ -v
```

---

*Exported: 2026-05-29 — MagicSquare Dual-Track RED Skeleton session.*
