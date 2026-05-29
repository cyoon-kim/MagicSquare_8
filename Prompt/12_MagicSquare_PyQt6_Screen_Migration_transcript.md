# MagicSquare PyQt6 Screen Migration — Prompt Transcript (Export)

- **Date:** 2026-05-29
- **Project:** Magic Square 4x4 TDD Practice
- **Target Repo:** `MagicSquare_XX/`
- **Scope:** Tkinter Screen 제거 → 예제 기준 PyQt6 GUI · 커밋 · (본 Export는 **코드 작업 Turn만**)
- **TDD Phase:** GREEN 유지 (Screen presentation only)
- **대응 보고서:** `Report/12_MagicSquare_PyQt6_Screen_Migration_Report.md`
- **Git:** `a2082e7` on `stabilize/green`

*(Turn 요약 Export — 분석·PR 문구·문서-only 대화는 제외)*

---

## Turn 01 — PyQt6 GUI로 교체 요청

**User**  
예제를 기준으로 GUI 방식은 그거 따라줄래?

**Assistant**  
- 참고: `c:\DEV\src\4.MagicSquare_1004_完\src\boundary\screen\main_window.py`, `app.py`
- 계획: PyQt6 `QSpinBox` 4×4, 「풀기」, 한국어 결과/오류 라벨
- **유지:** `SolveMagicSquareUseCase`, `BoundaryValidator`, pytest 43건
- **미적용:** 예제 `UIBoundary` + `InputValidator` `NotImplementedError` 패턴
- 기본 격자: PRD `G1_TD01_SAMPLE` (예제 G1 아님)

---

## Turn 02 — 구현 실행

**User**  
해줘

**Assistant**  
**생성**

- `src/boundary/screen/main_window.py` — `MagicSquareMainWindow`
  - `QSpinBox` 0~16, `G1_TD01_SAMPLE` 초기값
  - 「풀기」 → `use_case.execute(grid)`
  - 성공: `결과 (r1, c1, n1, r2, c2, n2): …`
  - 실패: `오류: {message}`

**수정**

- `src/boundary/screen/app.py` — `QApplication`, `build_use_case()`, `--verify`, `raise SystemExit(main())`
- `src/boundary/screen/__init__.py` — docstring only (`main` re-export 제거)
- `pyproject.toml` — `gui = ["PyQt6>=6.6"]`
- `README.md` — GUI 실행 절, `screen/` 구조 주석

**삭제**

- `src/boundary/screen/magic_square_window.py`
- `src/boundary/screen/matrix_input.py`

**검증**

```powershell
pip install -e ".[gui,dev]"
python -m pytest tests/boundary tests/control tests/entity -q
# 43 passed

python -m boundary.screen.app --verify
# code=INPUT_SIZE_INVALID
# message=Input matrix must be 4x4.
```

---

## Turn 03 — Git 커밋

**User**  
커밋 만들어줘 커밋 메시지와 함께

**Assistant**  
- 커밋 `a2082e7` on `stabilize/green`
- 메시지:
  ```
  feat(screen): replace Tkinter UI with PyQt6

  Match reference GUI pattern (4x4 QSpinBox, 풀기, Korean result/error labels)
  while keeping SolveMagicSquareUseCase unchanged. Add optional [gui] extra with
  PyQt6, --verify CLI, and README run instructions.
  ```
- 7 files changed, +128 / −179

---

## Turn 04 — Report · Transcript Export (코드 작업만)

**User**  
코드 작업한 부분만 report 랑 prompt 정리해줘

**Assistant**  
- `Report/12_MagicSquare_PyQt6_Screen_Migration_Report.md` 생성
- `Prompt/12_MagicSquare_PyQt6_Screen_Migration_transcript.md` 생성 (본 문서)

---

## 부록 — 세션 규칙 (코드 작업)

| 규칙 | 내용 |
|------|------|
| ECB | Screen → Control only (`SolveMagicSquareUseCase`) |
| 예제 따름 | PyQt6 레이아웃·문구 패턴만 |
| 예제 미따름 | `UIBoundary`, solver 무시 조립, 예제 G1 격자 |
| 테스트 | Domain/Boundary/Control pytest 무변경 |
| 의존성 | PyQt6는 `[gui]` optional extra |

---

## 산출물 경로

| 유형 | 경로 |
|------|------|
| 진행 보고서 | `Report/12_MagicSquare_PyQt6_Screen_Migration_Report.md` |
| Transcript | `Prompt/12_MagicSquare_PyQt6_Screen_Migration_transcript.md` |
| 커밋 | `a2082e7` — `feat(screen): replace Tkinter UI with PyQt6` |
