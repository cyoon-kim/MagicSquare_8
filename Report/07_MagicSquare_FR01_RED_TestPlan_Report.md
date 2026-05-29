# MagicSquare 진행 보고서 — FR-01 AC-01 RED · Test Plan · 결함 관리

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare 4x4 TDD Practice |
| **브랜치** | `feature/dual-track-tdd` |
| **범위** | Test Plan · 문서 동기화 · RED 테스트 · 결함 목록 · 커버리지 가이드 |
| **작성 목적** | FR-01 AC-01 RED 단계 산출물 추적 및 GREEN 착수 전 기준 고정 |
| **Production 코드** | `src/boundary`, `src/control`, `src/entity` **미구현** (의도적 RED) |

---

## 1. 작업 개요

PRD v1.1 확정 이후, **Track A(FR-01)** 선행 RED를 위해 테스트 계획·계약 문서·pytest RED 스위트·결함 목록을 정비했다.  
구현(GREEN)은 범위에서 제외했으며, pytest 수집 단계 `ModuleNotFoundError: No module named 'boundary'` 를 **정상 RED**로 확인했다.

### 1.1 작업 단계

| # | 단계 | 산출 |
|---|------|------|
| 1 | `feature/dual-track-tdd` 브랜치 생성 | Git branch |
| 2 | 샘플 예제 선정 (AC-01, `matrix=None`) | test_plan §2.1 |
| 3 | `docs/test_plan.md` v1.0 → v1.1 | Test Plan |
| 4 | README RED To-Do · 문서 허점 정리 | README, contracts, coverage_guide |
| 5 | `legacy/entity` 분리 · 문서 커밋 | `f495d3e` |
| 6 | PRD 정렬 RED 테스트 작성 | `tests/boundary/`, `tests/control/` |
| 7 | `docs/defect_list.md` DEF-001~006 | 결함 추적 |
| 8 | HTML 커버리지 가이드 (legacy GREEN) | `htmlcov/` |

---

## 2. 문서 산출물

| 파일 | 버전 | 설명 |
|------|------|------|
| `docs/test_plan.md` | 1.1 | FR-01 AC-01, BV-01~06, mock 전략, ID 매핑 |
| `docs/contracts.md` | 1.0 | API SSOT — `matrix`, `INPUT_SIZE_INVALID`, ECB `entity` |
| `docs/coverage_guide.md` | 1.0 | 실습 §6 명령 · 80/85/95 gate |
| `docs/defect_list.md` | 1.1 | DEF-001~006 |
| `docs/red_implementation_checklist.md` | 1.0 | GREEN 전 보류 항목 |
| `docs/PRD_MagicSquare.md` | 1.1+ | §22 AC-01 defensive inputs Closed |
| `pyproject.toml` | — | `pythonpath=src`, `--import-mode=importlib` |
| `README.md` | — | Track A / A-2 / B, 커버리지 명령, 결함 체크 |

---

## 3. RED 테스트 산출물

### 3.1 테스트 파일

| 파일 | PRD | 테스트 수 | 상태 |
|------|-----|-----------|------|
| `tests/boundary/test_fr01_ac01_boundary_validator.py` | AC-01 | 4 + parametrize 6 | collection ERROR |
| `tests/boundary/test_fr01_ac01_error_contract.py` | AC-01, §13 | 1 | collection ERROR |
| `tests/control/test_fr01_ac05_ac23_use_case_isolation.py` | AC-05, AC-23 | 3 + parametrize 3 | collection ERROR |
| `tests/constants.py` | §13 | — | 테스트 전용 상수 |
| `tests/legacy/test_user_entity.py` | — | 5 | **PASS** (범위 외) |

### 3.2 AC-01 커버 입력 (BV)

| ID | Input | 기대 code |
|----|-------|-----------|
| BV-01 | `matrix=None` | `INPUT_SIZE_INVALID` |
| BV-02 | `matrix=[]` | `INPUT_SIZE_INVALID` |
| BV-03 | `matrix=[[]]*4` | `INPUT_SIZE_INVALID` |
| BV-04~06 | 3×4, 4×3, 5×5 | `INPUT_SIZE_INVALID` |
| TD-03 | `[[1,2],[3,4]]` | `INPUT_SIZE_INVALID` |

### 3.3 RED 확인 명령

```bash
python -m pytest tests/boundary/ tests/control/ -v
# ModuleNotFoundError: No module named 'boundary'  ← 정상 RED
```

---

## 4. 아키텍처 · 폴더 정책

| 레이어 | 경로 | 상태 |
|--------|------|------|
| Boundary | `src/boundary/` | 미구현 |
| Control | `src/control/` | 미구현 |
| Entity (Domain) | `src/entity/` | 미구현 (Track B) |
| Legacy User 샘플 | `legacy/entity/` | 구현 있음, RED 범위 밖 |
| 테스트 | `tests/boundary/`, `tests/control/`, `tests/entity/` | RED 스위트 |

**주의:** `tests/boundary/` 폴더명은 test_plan·실습과 동일하게 유지. `sys.path`에 프로젝트 루트가 들어가면 `boundary` 패키지 shadowing 발생 → `pyproject.toml`의 `--import-mode=importlib` + `pythonpath=["src"]` 로 방지.

---

## 5. 결함 목록 요약 (`docs/defect_list.md`)

| ID | Severity | AC | 요약 |
|----|----------|-----|------|
| DEF-001 | Critical | AC-01 | `src/boundary/` 없음 |
| DEF-002 | Critical | AC-01 | `boundary.models` 없음 |
| DEF-003 | Critical | AC-05, AC-23 | Control/Entity/Formatter 없음 |
| DEF-004 | High | AC-01 | GREEN 후 throw 금지 검증 |
| DEF-005 | Medium | — | legacy 커버리지 79% < 80% gate |
| DEF-006 | Low | — | `tests/entity/` 미착수 |

---

## 6. 커버리지 · HTML 리포트

| 대상 | 명령 | 결과 |
|------|------|------|
| Boundary RED | `pytest tests/boundary/ --cov=src/boundary` | ERROR (import) |
| Legacy GREEN | `pytest tests/legacy/ --cov=legacy --cov-report=html` | 5 passed, HTML `htmlcov/index.html` |
| Entity (실습) | `pytest tests/entity/` | 0 collected (README만) |

HTML 열람: `htmlcov/index.html` (브라우저 또는 `Start-Process`).

---

## 7. Git 이력

| Commit | 요약 |
|--------|------|
| `f495d3e` | test_plan, contracts, README RED, legacy 이동 |
| (미커밋) | RED 테스트, defect_list, pyproject, coverage_guide |

---

## 8. Report/02 · 실습 문서와의 정렬

| 항목 | Report/02 (구) | 본 프로젝트 |
|------|----------------|-------------|
| Validation 위치 | Domain `validateInput` | **Boundary** `BoundaryValidator` (PRD FR-01) |
| Entity 폴더 | `src/entity/` | 동일 (Domain Logic) |
| 커버리지 | Domain 95%, UI 85% | Boundary 85%, Entity 95%, Global 80% |

`Report/02` 상단에 Superseded 배너 반영 완료.

---

## 9. 생성/수정 파일 목록

**생성**

- `docs/test_plan.md`, `docs/contracts.md`, `docs/coverage_guide.md`, `docs/defect_list.md`, `docs/red_implementation_checklist.md`
- `tests/boundary/test_fr01_ac01_*.py`, `tests/control/test_fr01_ac05_ac23_use_case_isolation.py`
- `tests/constants.py`, `tests/entity/README.md`, `pyproject.toml`
- `legacy/entity/user.py`, `tests/legacy/test_user_entity.py`

**수정**

- `README.md`, `docs/PRD_MagicSquare.md`, `Report/02_...md`, `tests/conftest.py`
- `.cursor/rules/magicsquare-tdd-testing.mdc`

**삭제**

- `src/entity/user.py` → `legacy/` 이동
- `tests/entity/test_user_entity.py` → `tests/legacy/`
- (일시) stub `src/boundary`, `src/control` — RED 정합을 위해 제거

---

## 10. 다음 권장 작업 (GREEN)

1. `src/boundary/boundary_validator.py`, `models.py` 최소 구현 → AC-01 PASS  
2. `src/control/solve_magic_square_use_case.py` + Entity/Formatter DI → AC-05, AC-23 PASS  
3. `pytest tests/boundary/ tests/control/ -m p0`  
4. DEF-001~003 Closed 처리 후 `defect_list.md` 갱신  
5. Track B: `tests/entity/` RED (FR-02~05a)

---

*본 문서는 FR-01 AC-01 RED 세션 산출 보고서이다. Production GREEN 구현은 다음 스프린트에서 수행한다.*
