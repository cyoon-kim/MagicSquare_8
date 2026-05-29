# MagicSquare_cyoon

4×4 마방진(Magic Square) **두 칸 완성**을 다루는 TDD · ECB 아키텍처 학습 프로젝트입니다.

**현재 단계:** **REFACTOR 진행 중** (R7 완료)  
Track A/B 구현·골든 마스터·PyQt6 Screen까지 완료했으며, ECB 의존 정리와 PRD 계약 보완 리팩터링을 진행 중입니다.

---

## 프로젝트 개요

4×4 격자에 **0(빈칸)** 또는 **1~16**을 배치하고, 빈칸 **정확히 2개**·누락 숫자 **2개**를 채워 **마방진(마법 상수 34)** 을 만드는 Use Case입니다.  
Boundary에서 입력을 검증하고, Domain에서 조합을 시도한 뒤, 성공 시 **int[6]** `(r1,c1,n1,r2,c2,n2)` 1-index 좌표를 반환합니다.

| 구분 | 내용 |
|------|------|
| **도메인** | 4×4 마방진 두 칸 완성 (FR-02~05a) |
| **아키텍처** | ECB — `boundary → control → entity` |
| **현재 단계** | REFACTOR 진행 중 (item 6 위생 완료 · 7항목 중 6완료) |
| **다음 단계** | 문서 SSOT 동기화 (R12 + §13) |
| **브랜치** | `refactor/refactor` (리팩터 작업) |

---

## 빠른 시작

### 테스트 (P0 + Golden Master)

```powershell
cd MagicSquare_XX
pip install -e ".[dev]"

# P0 회귀
python -m pytest tests/boundary/ tests/control/ tests/entity/ -m p0 -v

# Golden Master
python -m pytest tests/test_gm_01_magic_square_golden_master.py -v
python -m pytest -m golden_master -v
```

### 커버리지 gate ([`docs/coverage_guide.md`](docs/coverage_guide.md))

```powershell
# Entity 95%+ (NFR-01) — PASS (Report/11: 96.55%)
python -m pytest tests/entity/ --cov=src/entity --cov-report=term-missing --cov-fail-under=95

# Boundary 85%+ (NFR-02) — screen/ 포함 시 FAIL (~38%); omit 또는 smoke 정책 필요
python -m pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing --cov-fail-under=85

# 전역 80%+
python -m pytest tests/boundary/ tests/control/ tests/entity/ --cov=src --cov-report=term-missing --cov-fail-under=80
```

### GUI (PyQt6)

```powershell
pip install -e ".[gui,dev]"
python -m boundary.screen.app
```

- 기본 격자: PRD TD-01 (G1). **풀기** → 성공 시 `결과 (r1, c1, n1, r2, c2, n2): …`, 실패 시 `오류: …`
- CLI: `python -m boundary.screen.app --verify` (`matrix=None` 경계 검증)

---

## ECB 레이어

```
boundary/          control/                    entity/
├── BoundaryValidator   SolveMagicSquareUseCase   ├── BlankFinder
├── ResultFormatter     (FR-06 orchestration)     ├── MissingNumberFinder
├── models (ErrorResponse)                        ├── MagicSquareValidator
└── screen/ (PyQt6)                               └── Solver
```

**의존 방향:** `boundary → control → entity` · `entity → (none)`

> **REFACTOR 알림:** 현재 entity→boundary, control→boundary, `app.py`→entity 위반이 기록되어 있습니다.  
> 상세: [`docs/refactor-plan.md`](docs/refactor-plan.md) · [`docs/defect_list.md`](docs/defect_list.md) (QA-RISK-001~011)

---

## Golden Master 회귀 테스트 (GM-1)

`SolveMagicSquareUseCase`의 **실제 출력**을 스냅샷으로 고정하는 Approval / Golden Master 회귀 레이어입니다.

| 항목 | 내용 |
|------|------|
| **Test ID** | GM-1 |
| **기준 파일** | `tests/golden_master_expected.txt` |
| **시나리오 SSOT** | `tests/golden_master_scenarios.py` |
| **설계 문서** | [docs/golden_master_design.md](docs/golden_master_design.md) |

| Section | Test ID | 의미 |
|---------|---------|------|
| `normal_success` | GM-TC-01 | small-first 조합 성공 (G1) |
| `reverse_success` | GM-TC-02 | reverse fallback 성공 (G2) |
| `invalid_blank_count` | GM-TC-03 | 빈칸 0개 → `INPUT_BLANK_COUNT_INVALID` |
| `duplicate_number` | GM-TC-04 | non-zero 중복 → `INPUT_DUPLICATE_NON_ZERO` |
| `no_valid_solution` | GM-TC-05 | dual-fail → `DOMAIN_NO_MAGIC_ASSIGNMENT` |

```powershell
# 회귀 검증
pytest tests/test_gm_01_magic_square_golden_master.py -v

# 의도적 출력 변경 후 기준 갱신
pytest tests/test_gm_01_magic_square_golden_master.py --approve-golden -v
python scripts/generate_golden_master.py
python scripts/generate_golden_master.py --check   # CI compare-only
```

---

## 저장소 구조

```
MagicSquare_XX/
├── README.md
├── pyproject.toml
├── docs/
│   ├── PRD_MagicSquare.md
│   ├── test_plan.md
│   ├── contracts.md
│   ├── refactor-plan.md        # REFACTOR 백로그 R1~R12 (REF-MSQ-001)
│   ├── defect_list.md          # 결함·QA-RISK 추적
│   ├── coverage_guide.md
│   ├── golden_master_design.md
│   └── red_implementation_checklist.md
├── src/
│   ├── contracts/              # 공유 DTO + §13 codes (R1)
│   ├── boundary/               # BoundaryValidator, ResultFormatter, screen/
│   ├── control/                # SolveMagicSquareUseCase, ports, factory
│   └── entity/                 # BlankFinder, Solver, …
├── tests/
│   ├── boundary/  control/  entity/
│   ├── golden_master_*.py / golden_master_expected.txt
│   ├── test_gm_01_magic_square_golden_master.py
│   └── legacy/                 # User 샘플 (실습 Domain 아님)
├── legacy/entity/user.py
├── Report/                     # 진행 보고서 (최신: 13)
├── Prompt/                     # Transcript (최신: 13)
└── scripts/generate_golden_master.py
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) | FR/AC/BR, I/O 계약, Dual-Track TDD |
| [docs/contracts.md](docs/contracts.md) | API · Pydantic · error code SSOT |
| [docs/test_plan.md](docs/test_plan.md) | AC별 테스트·시나리오·RED ID |
| [**docs/refactor-plan.md**](docs/refactor-plan.md) | **REFACTOR 백로그, 슬라이스, 회귀 gate** |
| [docs/defect_list.md](docs/defect_list.md) | DEF Close/Open, QA-RISK 레지스트리 |
| [docs/coverage_guide.md](docs/coverage_guide.md) | entity/boundary/global 커버리지 gate |
| [docs/golden_master_design.md](docs/golden_master_design.md) | GM-1 Approve 패턴 |
| [Report/13_MagicSquare_CodeReview_QA_RefactorPlan_Report.md](Report/13_MagicSquare_CodeReview_QA_RefactorPlan_Report.md) | code-reviewer·QA 검토 보고 |
| [Prompt/13_MagicSquare_CodeReview_QA_RefactorPlan_transcript.md](Prompt/13_MagicSquare_CodeReview_QA_RefactorPlan_transcript.md) | 대응 Transcript |

---

## 진행 상태

### 완료

- [x] STEP 1~5 문제 정의 · PRD v1.1 · contracts · test_plan
- [x] Track A Boundary (FR-01) — AC-01, AC-05, AC-23
- [x] Track B Entity (FR-02~05a) — blank, missing, validator, solver
- [x] Control (FR-06) — `SolveMagicSquareUseCase`
- [x] GM-1 Golden Master (GM-TC-01~05)
- [x] PyQt6 Screen ([Report/12](Report/12_MagicSquare_PyQt6_Screen_Migration_Report.md))
- [x] REFACTOR 계획 · QA 리스크 정리 ([Report/13](Report/13_MagicSquare_CodeReview_QA_RefactorPlan_Report.md))

### REFACTOR Sprint

리팩터 merge마다 [`docs/refactor-plan.md`](docs/refactor-plan.md) §10 회귀 gate 실행.

> **통합 기준:** 원본 백로그 R1~R12 + §14 선행 작업을 **7개 체크리스트**로 묶었습니다.  
> 상세 ID·수용 기준·QA 테스트는 [`docs/refactor-plan.md`](docs/refactor-plan.md) (REF-MSQ-001) 참조.

| # | 항목 | 포함 (원본 ID) | 상태 |
|---|------|----------------|------|
| 1 | **숫자 상수 SSOT** — `validation.py` 하드코딩 → `entity.constants` | R7 | ✅ |
| 2 | **선행 게이트** — defect_list Close, AC-22 RED, NFR-04/AC-24, Boundary cov 정책 | §14 · QA-RISK-007~009 | ✅ |
| 3 | **슬라이스 A — ECB 구조** — `src/contracts/`, control ports, composition factory; AV-01~03 | R1 → R2/R3 | ✅ |
| 4 | **슬라이스 B — Boundary 출력** — `ResultFormatter` FR-05b, int[6] 검증, +1 index 이동 | R4 (AC-22 GREEN) | ✅ |
| 5 | **슬라이스 C — Domain·UseCase** — Solver 단일 error API, §13 `DOMAIN_*`, dead orchestration 제거 | R5 + R6 | ✅ |
| 6 | **코드·테스트 위생** — conftest fixture, docstring, assertion 정리, `print`→logging | R8 + R9 + R10 + R11 | ✅ |
| 7 | **문서 SSOT 동기화** — `contracts.md`↔`models.py`, test_plan·checklist·coverage_guide | R12 + §13 | ⬜ |

**진행:** 6 / 7 완료

#### 체크리스트 (merge 시 `[x]` 갱신)

- [x] **1. R7** — `validation.py` `MIN/MAX_CELL_VALUE` SSOT (`refactor/boundary`, `d539045`)
- [x] **2. 선행 게이트**
  - [x] `docs/defect_list.md` — DEF-001~004 Close, QA-RISK 반영
  - [x] AC-22 RED — `RED-BND-OUT-001/002` (`red_bnd_out` marker, R4 전 FAIL)
  - [x] NFR-04 matrix 불변성 · AC-24 UseCase G3 격리 테스트
  - [x] Boundary cov 정책 — `screen/` omit (`docs/coverage_guide.md` §4)
- [x] **3. 슬라이스 A (R1→R2/R3)** — ECB 의존 정리
  - [x] R1 `src/contracts/errors.py` — 공유 DTO + §13 코드 (entity→boundary 차단)
  - [x] R2 `control/ports.py` — Protocol + use case boundary import 제거
  - [x] R3 `control/factory.py` — `app.py` entity 직접 wire 제거
- [x] **4. 슬라이스 B (R4)** — Boundary 출력 계약
  - [x] `ResultFormatter` int[6] 검증 · `OUTPUT_FORMAT_INVALID`
  - [x] Solver 0-index 내부 · Formatter +1 변환 (QA-RISK-004)
  - [x] GM-TC-01/02 출력 불변
- [x] **5. 슬라이스 C (R5+R6)** — Domain API · 오케스트레이션
  - [x] R5 Solver 실패 API 단일화 — error 객체만, `DOMAIN_BLANK/MISSING_COUNT`
  - [x] R6 UseCase dead `find()` 제거 · validator DI 정리
- [x] **6. 코드·테스트 위생 (R8~R11)**
  - [x] R8 `solve_use_case` conftest fixture
  - [x] R9 public API Google docstring
  - [x] R10 중복 assertion 정리 (cosmetic)
  - [x] R11 `app.py` `print()` → `logging`
- [ ] **7. 문서 SSOT (R12 + §13)**
  - [ ] `docs/contracts.md` ↔ `src/boundary/models.py` parity
  - [ ] `docs/test_plan.md` · `docs/red_implementation_checklist.md` 상태 갱신
  - [ ] `docs/coverage_guide.md` boundary cov note

### 알려진 이슈 (Open)

| ID | 요약 |
|----|------|
| QA-RISK-007~011 | Boundary cov, stale docs (R12) |
| DEF-005 | legacy 커버리지 79% (< 80% gate) |

전체 목록: [`docs/defect_list.md`](docs/defect_list.md)

---

## 핵심 불변 조건 (Invariant)

| ID | 불변 | 요약 |
|----|------|------|
| I1 | 격자 형태 | 4×4, 16칸 |
| I3 | 숫자 집합 | 1~16 (0=빈칸) 중복·누락 규칙 |
| I5 | 마법 상수 | 각 마법 선의 합 = **34** |
| I7~I9 | 마법 선 | 4행 · 4열 · 2대각선 |

---

## TDD · 프로젝트 규칙

- **프레임워크:** pytest, AAA 패턴
- **커버리지:** entity ≥95%, boundary ≥85%, global ≥80%
- **business error:** `ErrorResponse` 객체 반환 — `pytest.raises` 금지 (entity는 R5에서 정렬 예정)
- **금지:** production `src/`에 `print()`, bare `except:`, 의미 없는 매직 상수
- **Cursor rules:** `.cursor/rules/magicsquare-*.mdc`

---

## 라이선스

미정 (추가 예정)
