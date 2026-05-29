# MagicSquare 진행 보고서 — Code Review · QA · Refactor Plan

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare 4x4 TDD Practice |
| **문서 ID** | RPT-MSQ-REFACTOR-PLAN-013 |
| **날짜** | 2026-05-29 |
| **브랜치** | `refactor/refactor` |
| **TDD 단계** | **REFACTOR 준비** — GREEN 유지, code-reviewer·QA 검토 후 계획서·결함 목록 정리 |
| **Production 코드** | **미변경** (문서만 생성·갱신) |
| **대응 Transcript** | `Prompt/13_MagicSquare_CodeReview_QA_RefactorPlan_transcript.md` |

---

## 1. 작업 개요

GREEN Sprint 완료 후 REFACTOR 착수를 위해 **code-reviewer**와 **qa-engineer** 서브에이전트로 전체 코드베이스를 검토하고, ECB·PRD·TDD 관점의 리팩터링 계획과 QA 리스크를 **한국어 문서**로 정리했다.

| # | 단계 | 산출 | 상태 |
|---|------|------|------|
| 1 | code-reviewer 코드 리뷰 | ECB 위반 3곳, R1~R12 백로그 | 완료 |
| 2 | qa-engineer 갭 분석 | PRD AC/NFR 공백, QA-RISK-001~011 | 완료 |
| 3 | `docs/refactor-plan.md` 작성 (한국어) | REF-MSQ-001 v1.0 | 완료 |
| 4 | `docs/defect_list.md` 갱신 | v1.2 — GREEN Close + QA-RISK Open | 완료 |
| 5 | Report · Transcript Export | 본 보고서 + Prompt/13 | 완료 |

**원칙**

- Production `src/` **미수정** — 계획·결함 추적 문서만 갱신
- ECB: `boundary → control → entity` (현재 3곳 위반 기록)
- TDD: business error는 `ErrorResponse` 객체; R4 전 AC-22 RED 선행
- REFACTOR Go/No-Go: **조건부 Go** (doc drift 정리 + AC-22 RED 후 슬라이스 A)

---

## 2. SSOT 참조

| 문서 | 역할 |
|------|------|
| `docs/PRD_MagicSquare.md` | FR-05b, FR-06, AC-22, AC-24, §13 오류 코드 |
| `docs/contracts.md` | 성공 int[6], ErrorResponse 스키마 |
| `docs/test_plan.md` | AC·시나리오·RED ID (일부 stale — REFACTOR 전 갱신 필요) |
| `docs/defect_list.md` | DEF Close/Open, QA-RISK 추적 |
| `docs/refactor-plan.md` | R1~R12 백로그, 슬라이스, 회귀 gate |
| `Report/11_MagicSquare_Full_GREEN_Sprint_Screen_Report.md` | GREEN 기준선 (43 passed, entity 96.55%) |
| `Report/12_MagicSquare_PyQt6_Screen_Migration_Report.md` | PyQt6 Screen (boundary cov 이슈 배경) |

---

## 3. code-reviewer 주요 발견

### 3.1 ECB 아키텍처 위반

| ID | 위반 | 위치 |
|----|------|------|
| AV-01 | entity → boundary | `src/entity/solver.py:7-12` — `boundary.models` import |
| AV-02 | control → boundary | `src/control/solve_magic_square_use_case.py:5-7` |
| AV-03 | boundary → entity | `src/boundary/screen/app.py:23-26` — composition root |

**준수:** `src/boundary/screen/main_window.py` → `SolveMagicSquareUseCase`만 사용.

### 3.2 코드·계약 리스크

| 항목 | 내용 |
|------|------|
| FR-05b | `ResultFormatter` pass-through — AC-22 미구현 |
| Solver API | `solve()` raise vs `solve_or_error()` ErrorResponse 이중 API |
| UseCase | `blank_finder`/`missing_finder` 결과 버림; `MagicSquareValidator` 미사용 |
| 금지 패턴 | `print()` in `app.py:44-47` |
| §13 | `DOMAIN_BLANK_COUNT`, `DOMAIN_MISSING_COUNT` 미구현 |

### 3.3 잘 되어 있는 부분

- 레이어 폴더·테스트 미러링, 골든 마스터, AC-05/AC-23 mock 격리
- `entity/constants.py` 명명 상수, bare `except` 없음
- Boundary 입력 검증 테스트 밀도

---

## 4. qa-engineer 보완 (refactor-plan에 반영)

### 4.1 PRD AC 커버리지 (~18/24)

| 미흡 AC | 공백 |
|---------|------|
| **AC-22** | RED-BND-OUT-001/002 없음 |
| **AC-24** | UseCase G3 → ErrorResponse + Formatter 격리 없음 |
| AC-05/AC-23 | Control BV-04~06 미파라미터화 |
| AC-01 P2 | ragged, non-list, 1D list |
| AC-02~04 | §13 message assertion 없음 |
| AC-15 | `DOMAIN_MAGIC_UNCHECKABLE` 미검증 |

### 4.2 NFR 자동화 공백

| NFR | 상태 |
|-----|------|
| NFR-01 (entity ≥95%) | Report/11: 96.55% PASS |
| NFR-02 (boundary ≥85%) | ~38% FAIL (`screen/` 0%) |
| NFR-03~05 | idempotency, 불변성, perf smoke **테스트 없음** |
| NFR-06 | ECB 위반 — R1~R3으로 해결 예정 |

### 4.3 QA 리스크 레지스트리 (defect_list Open)

QA-RISK-001~011 — `docs/defect_list.md` v1.2 Open 항목 참조.

---

## 5. 리팩터링 백로그 요약 (R1~R12)

### 높음

| ID | 작업 |
|----|------|
| R1 | 공유 contracts (`src/contracts/errors.py`) |
| R2 | Control ports (Protocol) |
| R3 | Composition factory — `app.py` entity import 제거 |
| R4 | FR-05b + AC-22 (RED 선행) |
| R5 | Solver 실패 API 단일화 |

### 중간 · 낮음

R6~R12: UseCase 오케스트레이션, 상수 SSOT, 테스트 factory, docstring, print 제거, contracts 동기화.

### 슬라이스 순서

```
R1 → R2/R3 → R4/R5 → R6 → R7~R12
```

---

## 6. pytest / 검증 결과

**본 세션:** production 코드 미변경 — pytest **미실행**.

**기준선 (Report/11, GREEN Sprint):**

| 명령 | 결과 |
|------|------|
| `pytest tests/boundary/ tests/control/ tests/entity/ -m p0` | 43 passed |
| `pytest tests/test_gm_01_magic_square_golden_master.py` | 6 passed |
| `pytest tests/entity/ --cov=src/entity --cov-fail-under=95` | 96.55% PASS |
| `pytest tests/boundary/ --cov=src/boundary --cov-fail-under=85` | ~38% FAIL (screen/) |

---

## 7. 생성·갱신 파일 목록

| 경로 | 설명 |
|------|------|
| `docs/refactor-plan.md` | **신규** — REF-MSQ-001 v1.0, R1~R12·QA·회귀 gate (한국어) |
| `docs/defect_list.md` | **갱신** v1.2 — DEF-001~004/006 Close, QA-RISK Open |
| `Report/13_MagicSquare_CodeReview_QA_RefactorPlan_Report.md` | 본 보고서 |
| `Prompt/13_MagicSquare_CodeReview_QA_RefactorPlan_transcript.md` | 대화 Transcript |

**미변경:** `src/**`, `tests/**`, `pyproject.toml`

---

## 8. 다음 권장 작업

1. **AC-22 RED** — `RED-BND-OUT-001/002` boundary 테스트 작성 (R4 TDD 선행)
2. **NFR-04** — success path matrix 불변성 테스트
3. **AC-24** — UseCase G3 → ErrorResponse, Formatter 격리
4. **Boundary cov 정책** — `screen/` omit vs smoke 결정
5. **슬라이스 A** — R1 contracts → R2/R3 ports/factory
6. **문서 drift** — `test_plan.md`, `contracts.md`, `red_implementation_checklist.md` 갱신

---

*본 문서는 Code Review · QA · Refactor Plan 세션 산출 보고서이다.*
