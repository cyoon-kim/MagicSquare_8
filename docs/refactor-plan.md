# MagicSquare 리팩터링 계획

| 항목 | 내용 |
|------|------|
| 문서 ID | REF-MSQ-001 |
| 상태 | 초안 (Draft) |
| 버전 | 1.0 |
| 작성일 | 2026-05-29 |
| 작성 | code-reviewer, QA engineer |
| 기준선 | GREEN stabilize/green (Report/11) |
| 참조 | `docs/PRD_MagicSquare.md`, `docs/contracts.md`, `docs/test_plan.md` |

---

## 0. 요약

구현은 **기능적으로 GREEN** 상태이며, 골든 마스터와 AC-05/AC-23 격리 테스트가 잘 갖춰져 있다. 주요 부채는 **ECB 의존 방향 위반**과 **PRD 계약 미완** (FR-05b, 도메인 invariant 오류 코드)이다.

REFACTOR 착수는 **조건부 Go**: 문서 drift 정리, AC-22 RED + NFR-04 기준선 테스트 추가 후 구조 슬라이스를 진행한다.

**첫 슬라이스 (ROI 높음):** R1 (공유 contracts) → R2/R3 (포트 + 팩토리) — GM-TC-01~05 및 P0 테스트 동작 유지.

---

## 1. 현재 상태 평가

### 잘 되어 있는 부분

- 레이어 폴더 및 테스트 미러링 (`src/boundary|control|entity`)
- Boundary 입력 검증 + AC-01 테스트
- 도메인 단위: BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver
- `main_window.py` → UseCase만 사용 (entity 직접 호출 없음)
- 골든 마스터 + 계약 헬퍼
- Entity 커버리지 **96.55%** (Report/11)

### 알려진 이슈

- ECB 위반 3곳 (§2 참조)
- `ResultFormatter` pass-through — AC-22 테스트 없음
- UseCase dead call (`blank_finder`/`missing_finder` 결과 버림; `MagicSquareValidator` 미사용)
- Solver 이중 API: `solve()`는 raise, `solve_or_error()`는 `ErrorResponse` 반환
- `src/boundary/screen/app.py:44-47`에 `print()` (금지 패턴)
- Boundary cov gate **FAIL ~38%** (`src/boundary/screen/` 미테스트 포함 시)

### REFACTOR 전 갱신할 문서 (stale)

| 문서 | 문제 |
|------|------|
| `docs/defect_list.md` | DEF-001~006 RED 시점 그대로 — production 이미 존재 |
| `docs/test_plan.md` | AC-01 스프린트만 기술; Track A/B 전체 구현됨 |
| `docs/red_implementation_checklist.md` | Pending 표기 — 대부분 완료 |
| `docs/contracts.md` | `ErrorCode`/`ERROR_MESSAGES` vs `models.py` flat 상수 불일치 |

---

## 2. 아키텍처 부채 (R1–R3)

| ID | 위반 | 위치 |
|----|------|------|
| AV-01 | entity → boundary | `src/entity/solver.py:7-12` |
| AV-02 | control → boundary | `src/control/solve_magic_square_use_case.py:5-7` |
| AV-03 | boundary → entity (조립) | `src/boundary/screen/app.py:23-26` |

**준수:** `src/boundary/screen/main_window.py` → `SolveMagicSquareUseCase`만 사용.

**수용 기준:** entity는 `boundary`/`control`을 import하지 않음 (grep/import-linter).

---

## 3. 계약 부채 (R4–R5)

| 공백 | PRD | 현재 |
|------|-----|------|
| AC-22 | `OUTPUT_FORMAT_INVALID` | 테스트 없음; formatter pass-through |
| AC-15 | `DOMAIN_MAGIC_UNCHECKABLE` | `False` 반환만 |
| §13 | `DOMAIN_BLANK_COUNT`, `DOMAIN_MISSING_COUNT` | generic `UnsolvableDomainError` |
| 인덱스 계약 | Domain 0-index, Boundary +1 | `solver.py:68`에서 1-index 반환 |

**R4 선행 조건:** `ResultFormatter` 변경 **전에** RED-BND-OUT-001/002 작성 (TDD).

**R5:** entity 비즈니스 오류 테스트에서 `pytest.raises` 제거 (`test_d_sol_01_04`).

---

## 4. 오케스트레이션 부채 (R6)

- `solve_magic_square_use_case.py:41-42` — `find()` 결과 버림; Solver 내부에서 동일 작업 재수행
- `magic_square_validator` 주입만 되고 `execute()`에서 미사용

**QA:** 호출 제거 전 call-count spy 테스트 추가.

---

## 5. 품질 / 위생 (R7–R12)

| ID | 항목 |
|----|------|
| R7 | `validation.py:19` 하드코딩 `16` → 공유 상수 |
| R8 | 테스트 `build_use_case()` ≥4곳 중복 → `conftest.py` fixture |
| R9 | public API Google docstring |
| R10 | 중복 assertion 정리 (cosmetic) |
| R11 | `app.py`의 `print()` 제거 |
| R12 | `docs/contracts.md` ↔ `models.py` 동기화 |

---

## 6. 리팩터링 백로그

### 높음 (High)

| ID | 작업 | 이유 | 접근 |
|----|------|------|------|
| R1 | 공유 contracts 모듈 | entity→boundary 차단 | `src/contracts/errors.py`: DTO + §13 코드 |
| R2 | Control ports | control→boundary 역전 | `control/ports.py` Protocol; boundary 구현 |
| R3 | Composition factory | UI에서 entity 직접 wire 제거 | `control/factory.py`; `app.py` 슬림화 |
| R4 | FR-05b 완성 | AC-19~22 | Formatter가 int[6] 검증; solver는 0-index 내부 |
| R5 | Solver 실패 API 단일화 | PRD §13 + TDD 규칙 | 단일 반환 타입; 도메인 오류 코드 |

### 중간 (Medium)

| ID | 작업 |
|----|------|
| R6 | UseCase 오케스트레이션 정리 |
| R7 | 숫자 상수 SSOT |
| R8 | 테스트 factory 중복 제거 |
| R9 | Google docstring |

### 낮음 (Low)

| ID | 작업 |
|----|------|
| R10 | 중복 assertion 정리 |
| R11 | dev `print` → logging |
| R12 | `docs/contracts.md` 동기화 |

---

## 7. 테스트 공백 (QA 담당 — 리팩터 전/동시에 보완)

### PRD AC 공백

| AC | 공백 |
|----|------|
| AC-01 P2 | ragged rows, non-list, 1D list (EX-04~06) |
| AC-02~04 | §13 **message** assertion 없음 |
| AC-05/AC-23 | Control: BV-04~06 미파라미터화 |
| AC-06~10 | Entity G2 (TD-02) blank/missing 변형 |
| AC-15 | `DOMAIN_MAGIC_UNCHECKABLE` 미검증 |
| AC-17 | U-OUT G2 전용 테스트 없음 |
| **AC-22** | **RED-BND-OUT-001/002 없음** |
| **AC-24** | UseCase G3 → ErrorResponse + Formatter 격리 없음 |

### NFR 공백

| NFR | 공백 |
|-----|------|
| NFR-03 | TD-01 idempotency 테스트 없음 |
| NFR-04 | matrix 불변성 테스트 없음 |
| NFR-05 | ≤50ms 성능 smoke 없음 |
| NFR-06 | ECB 위반 (R1–R3으로 해결) |
| NFR-02 | `screen/` 포함 시 Boundary gate FAIL |

### 추가 권장 테스트

- `tests/boundary/test_red_bnd_out_001_format_invalid_length.py`
- `tests/boundary/test_red_bnd_out_002_format_invalid_coords.py`
- `tests/contracts/test_error_schema.py` (R1)
- `tests/control/test_factory_builds_use_case.py` (R3)
- UseCase AC-24: G3 execute → `ErrorResponse`, formatter success 경로 미호출
- NFR-04: 성공 `execute()` 후 입력 matrix 변경 없음

---

## 8. QA 리스크 레지스트리

| ID | 심각도 | 제목 |
|----|--------|------|
| QA-RISK-001 | Critical | Entity가 boundary.models import |
| QA-RISK-002 | Critical | app.py가 entity 직접 wire |
| QA-RISK-003 | High | FR-05b 미구현 |
| QA-RISK-004 | High | 1-index가 잘못된 레이어에 있음 |
| QA-RISK-005 | High | UseCase dead orchestration |
| QA-RISK-006 | High | Solver 이중 실패 API |
| QA-RISK-007 | Medium | Boundary cov ~38% (screen/) |
| QA-RISK-008 | Medium | app.py print() |
| QA-RISK-009 | Medium | stale defect_list.md |
| QA-RISK-010 | Low | Solver.solve 타입 annotation 불일치 |
| QA-RISK-011 | Low | §13 코드 4개 models.py 미등록 |

---

## 9. 구현 슬라이스 및 수용 기준

### 의존 순서

```
R1 → R2/R3 (병렬) → R4/R5 → R6 → R7/R8/R9 → R10/R11/R12
```

**R4는 AC-22 RED 테스트 존재 후에만 시작.**

### 슬라이스 A — 구조 (R1, R2, R3)

| 수용 기준 | 내용 |
|-----------|------|
| Import | entity에 boundary/control import 0건 |
| Ports | mock protocol로 use case 테스트 |
| Factory | `app.py`에 entity import 없음 |
| 회귀 | GM-TC-01~05 + P0 green |

### 슬라이스 B — Boundary 계약 (R4)

| 수용 기준 | 내용 |
|-----------|------|
| AC-22 | RED-BND-OUT-001/002 green |
| AC-19~21 | GM-TC-01/02 출력 불변 |
| Index | Formatter가 +1 변환 담당 |

### 슬라이스 C — Domain API (R5, R6)

| 수용 기준 | 내용 |
|-----------|------|
| No raises | public Solver API는 error 객체만 반환 |
| §13 codes | BLANK_COUNT, MISSING_COUNT, NO_MAGIC_ASSIGNMENT |
| Orchestration | 중복 find() 없음 또는 단일 경로 문서화 |

---

## 10. 회귀 게이트 (슬라이스 merge마다 필수)

```bash
python -m pytest tests/boundary/ tests/control/ tests/entity/ -m p0 -v
python -m pytest tests/test_gm_01_magic_square_golden_master.py -v
python -m pytest tests/entity/ --cov=src/entity --cov-report=term-missing --cov-fail-under=95
python -m pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing --cov-fail-under=85
```

**참고:** Boundary 85% gate 적용 전 `screen/` omit vs smoke 정책 결정 필요.

---

## 11. R1–R12 항목별 QA 테스트 계획

| ID | 추가/변경할 테스트 |
|----|-------------------|
| R1 | `tests/contracts/test_error_schema.py`; import 방향 smoke |
| R2 | AC-05/AC-23 mock ports; control에 concrete boundary 없음 |
| R3 | `test_factory_builds_use_case.py` |
| R4 | RED-BND-OUT-001/002; formatter 0→1 index; UseCase malformed payload |
| R5 | entity `pytest.raises` 제거; DOMAIN_BLANK/MISSING_COUNT |
| R6 | blank_finder call-count spy; validator DI 정리 |
| R7 | TS-B-01/02 공유 상수 parametrize |
| R8 | conftest `solve_use_case` fixture SSOT |
| R9 | docstring 리뷰 gate |
| R10 | 신규 테스트 없음 |
| R11 | CLI verify caplog; src에 print 없음 |
| R12 | contracts.md ↔ models.py parity 리뷰 |

---

## 12. 범위 외 (Out of Scope)

- PyQt GUI 기능 (smoke/cov 정책 제외)
- N×N 일반화
- 메시지 i18n
- `entity/` → `domain/` rename (coverage_guide 경로와 충돌)

---

## 13. 문서 동기화 체크리스트 (merge 시)

- [ ] `docs/contracts.md` 갱신 (R1, R4, R12)
- [ ] `docs/defect_list.md` DEF-001~004 Close; QA-RISK 반영
- [ ] `docs/test_plan.md` 범위를 Track A/B 전체로 갱신
- [ ] `docs/red_implementation_checklist.md` 상태 갱신
- [ ] `docs/coverage_guide.md`에 boundary cov 정책(note) 추가

---

## 14. REFACTOR 착수 권장 순서

1. **`docs/refactor-plan.md` 확정** (본 문서)
2. **`docs/defect_list.md` 갱신** — DEF-001~004 Close, QA-RISK 등록
3. **AC-22 RED** (RED-BND-OUT-001/002) 작성
4. **NFR-04 불변성** + **AC-24** UseCase 테스트 추가
5. **Boundary cov 정책** 결정 (omit vs screen smoke)
6. **슬라이스 A:** R1 → R2/R3 → 회귀 gate
7. **슬라이스 B:** R4 (RED→GREEN) → **슬라이스 C:** R5/R6

---

## 15. 참조

- `docs/PRD_MagicSquare.md` §13, FR-05b, FR-06, AC-22, AC-24
- `Report/11_MagicSquare_Full_GREEN_Sprint_Screen_Report.md`
- `.cursor/rules/magicsquare-ecb-architecture.mdc`
- `.cursor/rules/magicsquare-tdd-testing.mdc`

---

## 개정 이력

| 버전 | 날짜 | 요약 |
|------|------|------|
| 1.0 | 2026-05-29 | code-reviewer + QA 검토 반영, 초안 작성 |
