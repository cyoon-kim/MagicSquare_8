# MagicSquare 진행 보고서 — PyQt6 Screen Migration

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare 4x4 TDD Practice |
| **문서 ID** | RPT-MSQ-PYQT6-SCREEN-012 |
| **날짜** | 2026-05-29 |
| **브랜치** | `stabilize/green` |
| **TDD 단계** | **GREEN 유지** — Boundary Screen 레이어만 교체 (Domain/Control 미변경) |
| **Production 코드** | `src/boundary/screen/`, `pyproject.toml` `[gui]`, `README.md` GUI 절 |
| **대응 Transcript** | `Prompt/12_MagicSquare_PyQt6_Screen_Migration_transcript.md` |
| **Git** | `a2082e7` — `feat(screen): replace Tkinter UI with PyQt6` |

---

## 1. 작업 개요

참고 예제 [`src/4.MagicSquare_1004_完`](../../src/4.MagicSquare_1004_完) 의 **PyQt6 GUI 패턴**에 맞춰, 기존 Tkinter Screen을 제거하고 **QSpinBox 4×4 + 「풀기」** UI로 교체했다. 풀이·검증 코어는 **`SolveMagicSquareUseCase` 그대로** 유지한다.

| # | 단계 | 산출 | 상태 |
|---|------|------|------|
| 1 | 예제 GUI 패턴 분석 | `main_window.py`, `app.py` (PyQt6) | 완료 |
| 2 | Tkinter 제거 | `magic_square_window.py`, `matrix_input.py` 삭제 | 완료 |
| 3 | 의존성 | `pyproject.toml` optional `[gui]` → PyQt6 | 완료 |
| 4 | 문서 | README GUI 실행 절 | 완료 |
| 5 | 검증 | pytest 43 + `--verify` CLI | 완료 |
| 6 | Git | `a2082e7` | 완료 |

**원칙**

- Screen → **Control only** (`SolveMagicSquareUseCase.execute`)
- 예제의 `UIBoundary` / `NotImplementedError` 우회 패턴은 **미적용**
- PRD G1 (`samples.G1_TD01_SAMPLE`) 기본 격자 유지
- 기존 pytest 43건 **변경 없음** (screen 레이어는 원래 미테스트)

---

## 2. SSOT 참조

| 문서 | 역할 |
|------|------|
| `docs/PRD_MagicSquare.md` | FR-06 오케스트레이션, I/O 계약 |
| `docs/contracts.md` | 성공 `int[6]`, `ErrorResponse` |
| `src/boundary/screen/samples.py` | PRD TD-01 G1 기본 격자 |
| `Report/11_MagicSquare_Full_GREEN_Sprint_Screen_Report.md` | 이전 Tkinter Screen 추가 보고 |
| 참고 예제 | `c:\DEV\src\4.MagicSquare_1004_完\src\boundary\screen\` |

---

## 3. 변경 내용

### 3.1 추가·수정

| 파일 | 변경 |
|------|------|
| `src/boundary/screen/main_window.py` | **신규** — `MagicSquareMainWindow` (PyQt6 `QSpinBox` 4×4, 「풀기」, 결과/오류 `QLabel`) |
| `src/boundary/screen/app.py` | `QApplication`, `MagicSquareMainWindow`, `--verify` CLI, `main() -> int` |
| `src/boundary/screen/__init__.py` | PyQt6 screen 모듈 설명만 유지 (`main` re-export 제거 — import 경고 방지) |
| `pyproject.toml` | `[project.optional-dependencies] gui = ["PyQt6>=6.6"]` |
| `README.md` | GUI 실행 절, 저장소 구조 `screen/` 주석 |

### 3.2 삭제

| 파일 | 사유 |
|------|------|
| `src/boundary/screen/magic_square_window.py` | Tkinter `MagicSquareWindow` |
| `src/boundary/screen/matrix_input.py` | Tk `Entry` 파싱 헬퍼 |

### 3.3 미변경

| 경로 | 비고 |
|------|------|
| `src/control/solve_magic_square_use_case.py` | 오케스트레이션 동일 |
| `src/boundary/boundary_validator.py` | FR-01 동일 |
| `src/entity/*` | Domain 동일 |
| `src/boundary/screen/samples.py` | G0/G1/G2 샘플 유지 (UI 로드 버튼은 미포함 — 예제 최소 UI) |
| `tests/boundary/`, `tests/control/`, `tests/entity/` | 테스트 코드 무변경 |

---

## 4. UI 동작 (예제 패턴)

| 요소 | 구현 |
|------|------|
| 입력 | 4×4 `QSpinBox`, 범위 0~16 |
| 기본값 | `G1_TD01_SAMPLE` (PRD TD-01) |
| 버튼 | 「풀기」 |
| 성공 | `결과 (r1, c1, n1, r2, c2, n2): …` |
| 실패 | `오류: {ErrorResponse.error.message}` |
| 진입 | `python -m boundary.screen.app` 또는 `magicsquare-screen` |
| CLI | `python -m boundary.screen.app --verify` → `matrix=None` 경계 검증 출력 |

---

## 5. 검증 결과

```powershell
pip install -e ".[gui,dev]"
python -m pytest tests/boundary tests/control tests/entity -q
python -m boundary.screen.app --verify
```

| 항목 | 결과 |
|------|------|
| Magic Square pytest | **43 passed** |
| `--verify` | `code=INPUT_SIZE_INVALID`, `message=Input matrix must be 4x4.` |
| 수동 GUI | G1 기본 → 풀기 → `1, 2, 3, 1, 4, 13` (예상) |

---

## 6. 생성 파일 목록

| 경로 | 설명 |
|------|------|
| `Report/12_MagicSquare_PyQt6_Screen_Migration_Report.md` | 본 보고서 |
| `Prompt/12_MagicSquare_PyQt6_Screen_Migration_transcript.md` | 대화 Transcript (코드 작업 Turn만) |
| `src/boundary/screen/main_window.py` | PyQt6 메인 윈도우 |
| `src/boundary/screen/app.py` | 앱 진입점 (수정) |

---

## 7. 다음 권장 작업

1. `git push` 후 `develop` 대상 PR 머지
2. (선택) G1/G2/G0 샘플 로드 `QPushButton` — Report/11 Tk에 있던 데모 UX
3. (선택) screen 레이어 smoke test 또는 Golden Master (예제 `1004_完` 참고)

---

*본 문서는 PyQt6 Screen Migration 코드 작업 세션 산출 보고서이다.*
