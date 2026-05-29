---
name: export-report-transcript
description: >-
  MagicSquare_XX 세션 종료 시 Report/ 보고서와 Prompt/ Transcript를 쌍으로 Export한다.
  Use when the user runs /export, says Report 폴더에 보고서 생성, Prompt Transcript Export,
  보고서 작성 및 백업, or at the end of a MagicSquare TDD sprint or documentation session.
---

# Report · Transcript Export (MagicSquare_XX)

세션 산출물을 **항상 Report + Prompt 쌍**으로 저장한다. 둘 중 하나만 만들지 않는다.

관련 에이전트: `.cursor/agents/backup-manager.md` (GitHub 백업 포함 시). 본 skill은 문서 Export에 집중한다.

## Trigger

**슬래시 명령 (권장):** 채팅 입력창에 `/export` → Enter

**문장:** `Report 폴더에 보고서 생성하고, Prompt 폴더에 Transcript도 Export 해줘`

동의어: `보고서 작성 및 백업`, `Report Export`, `Transcript Export`

## 실행 체크리스트

```
- [ ] 1. Report/ 번호 확인 → 다음 NN 결정
- [ ] 2. 세션 주제·범위·변경 파일·테스트 결과 수집
- [ ] 3. Report/NN_MagicSquare_<Topic>_Report.md 작성
- [ ] 4. Prompt/NN_MagicSquare_<Topic>_transcript.md 작성 (동일 NN)
- [ ] 5. Report ↔ Transcript 상호 링크 확인
- [ ] 6. 사용자에게 생성 경로·번호 보고
```

## 1. 번호 (NN) 결정

1. `Report/` 아래 `NN_` 접두 숫자 목록을 확인한다.
2. **최대 NN + 1**을 사용한다. (현재 최신: 09 → 다음 10)
3. Report와 Prompt는 **동일 NN**을 쓴다.
4. 08번은 Report/Prompt 모두 없음 — 건너뛰지 말고 **10**부터 이어간다 (09 다음).

## 2. 파일명 규칙

| 종류 | 경로 | 패턴 | 예시 |
|------|------|------|------|
| 보고서 | `Report/` | `NN_MagicSquare_<Topic>_Report.md` | `09_..._Test_Report.md` |
| Transcript | `Prompt/` | `NN_MagicSquare_<Topic>_transcript.md` | `09_..._transcript.md` |

- `<Topic>`: PascalCase 또는 snake_case, 작업 주제를 짧게 (예: `FR01_RED_TestPlan`, `DualTrack_RED_Skeleton`)
- 공백 금지, 단어는 `_`로 연결
- **접미사:** Report는 `_Report.md`, Prompt는 `_transcript.md` (backup-manager의 `_Prompt.md` 아님)

## 3. Report 작성

[`templates.md`](templates.md)의 Report 템플릿을 따른다.

**필수 포함:**

- 메타 표: 프로젝트, 문서 ID, 날짜, 브랜치, TDD 단계, 대응 Transcript 경로
- §1 작업 개요 (목표·단계·상태 표)
- SSOT 참조 (`docs/PRD_MagicSquare.md`, `docs/contracts.md`, `docs/test_plan.md`, 관련 Report)
- 변경·생성 파일 목록 (경로 + 설명)
- pytest/검증 결과 (실행했다면 명령 + PASS/FAIL/ERROR 수)
- 다음 권장 작업
- 마지막 줄: `*본 문서는 … 세션 산출 보고서이다.*`

**금지:** 추측으로 변경 사항 작성, 테스트 미실행인데 통과 주장

## 4. Transcript 작성

[`templates.md`](templates.md)의 Transcript 템플릿을 따른다.

**필수 포함:**

- 헤더: Date, Project, Target Repo, Scope, TDD Phase, 대응 보고서 경로
- **Turn 단위** (`## Turn NN — <제목>`): User / Assistant 구분
- 각 Turn: 사용자 요청 원문(또는 핵심 인용) + 에이전트 수행 요약·산출물·명령·결과
- 부록: 세션 중 적용된 규칙·SSOT·생성 파일 경로 표

**Transcript 깊이 (우선순위):**

1. **가능하면** Cursor agent transcript 원문 참조:  
   `C:\Users\usejen_id\.cursor\projects\c-DEV\agent-transcripts\*.jsonl`  
   (현재 대화 UUID 파일 — User/Assistant 전체 보존)
2. 원문 접근 불가 시: 현재 채팅 히스토리에서 Turn별 **요약 Export** (Report/07·09·06 스타일)
3. backup-manager 규칙과 충돌 시: **전체 원문 Export**가 가능하면 원문 우선; 불가하면 Turn 요약 + `*(요약 Export)*` 명시

**금지:** Turn 순서 뒤바꿈, 존재하지 않는 파일·테스트 결과 invent

## 5. 상호 참조

Report 메타 표:

```markdown
| **대응 Transcript** | `Prompt/NN_MagicSquare_<Topic>_transcript.md` |
```

Transcript 헤더:

```markdown
- **대응 보고서:** `Report/NN_MagicSquare_<Topic>_Report.md`
```

Report §생성 파일 목록에 Report·Prompt 경로 모두 기재.

## 6. 완료 보고 형식

```markdown
## Export 완료

| 항목 | 경로 |
|------|------|
| 번호 | NN |
| 보고서 | Report/NN_..._Report.md |
| Transcript | Prompt/NN_..._transcript.md |
```

Git commit/push는 사용자가 요청할 때만.

## 참고 — 기존 산출물

| NN | Report | Prompt |
|----|--------|--------|
| 09 | DualTrack RED Skeleton Test | DualTrack RED Skeleton transcript |
| 07 | FR01 RED TestPlan | FR01 RED transcript |
| 06 | PRD PreImplementation | PRD transcript |

새 세션은 위 패턴과 **동일한 품질·구조**를 유지한다.

## 추가 리소스

- 상세 템플릿: [templates.md](templates.md)
- GitHub 포함 백업: `.cursor/agents/backup-manager.md`
