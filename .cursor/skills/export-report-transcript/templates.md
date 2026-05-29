# Report · Transcript Templates

## Report template

```markdown
# MagicSquare 진행 보고서 — <세션 제목>

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare 4x4 TDD Practice |
| **문서 ID** | RPT-MSQ-<SHORT-ID>-<NN> |
| **날짜** | YYYY-MM-DD |
| **브랜치** | `<branch-name>` |
| **TDD 단계** | **RED/GREEN/REFACTOR** — <한 줄 설명> |
| **Production 코드** | <구현 범위 또는 "미구현"> |
| **대응 Transcript** | `Prompt/NN_MagicSquare_<Topic>_transcript.md` |

---

## 1. 작업 개요

<이번 세션 목표 1~2문장>

| # | 단계 | 산출 | 상태 |
|---|------|------|------|
| 1 | ... | ... | 완료/진행/보류 |

**원칙:** <세션에서 지킨 TDD·ECB·금지 사항>

---

## 2. SSOT 참조

| 문서 | 역할 |
|------|------|
| `docs/PRD_MagicSquare.md` | ... |
| `docs/contracts.md` | ... |
| `docs/test_plan.md` | ... |
| `Report/XX_...md` | ... |

---

## 3. <도메인별 섹션 — 변경 내용·설계·테스트>

(세션 주제에 맞게 §3~§N 구성. 표·체크리스트 적극 사용)

---

## N. 생성 파일 목록

| 경로 | 설명 |
|------|------|
| `Report/NN_..._Report.md` | 본 보고서 |
| `Prompt/NN_..._transcript.md` | 대화 Transcript |
| ... | ... |

**미변경:** <의도적으로 건드리지 않은 파일>

---

## N+1. 다음 권장 작업

1. ...
2. ...

---

*본 문서는 <세션 주제> 세션 산출 보고서이다.*
```

---

## Transcript template

```markdown
# MagicSquare <세션 제목> — Prompt Transcript (Export)

- **Date:** YYYY-MM-DD
- **Project:** Magic Square 4x4 TDD Practice
- **Target Repo:** `MagicSquare_XX/`
- **Scope:** <한 줄 범위>
- **TDD Phase:** <RED/GREEN/REFACTOR + 부가 설명>
- **대응 보고서:** `Report/NN_MagicSquare_<Topic>_Report.md`

---

## Turn 01 — <첫 사용자 요청 요약>

**User**  
<사용자 메시지 원문 또는 핵심 인용>

**Assistant**  
- <수행한 분석·파일·결정>
- <생성/수정 파일 목록>
- <실행한 명령 및 결과>

---

## Turn 02 — <제목>

**User**  
...

**Assistant**  
...

---

## Turn NN — Report · Transcript Export

**User**  
Report 폴더에 보고서 생성, Prompt 폴더에 Transcript Export.

**Assistant**  
- `Report/NN_MagicSquare_<Topic>_Report.md` 생성
- `Prompt/NN_MagicSquare_<Topic>_transcript.md` 생성 (본 문서)

---

## 부록 — 주요 사용자 규칙 (세션)

| 규칙 | 내용 |
|------|------|
| ECB | boundary → control → entity |
| Dual-Track | Track A 계약 / Track B 로직 분리 |
| ... | ... |

---

## 산출물 경로

| 유형 | 경로 |
|------|------|
| 진행 보고서 | `Report/NN_..._Report.md` |
| Transcript | `Prompt/NN_..._transcript.md` |
```

---

## Topic naming examples

| 세션 유형 | Topic 예시 |
|-----------|------------|
| FR-01 RED | `FR01_RED_TestPlan` |
| Dual-Track skeleton | `DualTrack_RED_Skeleton` |
| PRD 작성 | `PRD_PreImplementation` |
| Cursor rules | `CursorRules_Modularization` |
| Entity GREEN | `Entity_FR02_GREEN` |
