# MagicSquare 진행 보고서 — PRD 사전 작성 및 검토

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare 4x4 TDD Practice |
| **범위** | 참고 문서 분석 · PRD 초안 · PRD 검토 · PRD v1.1 개정 |
| **작성 목적** | 구현 전 기준 문서(PRD) 확정 및 추적성 확보 |
| **구현·테스트 코드** | 본 보고서 범위에 포함하지 않음 |

---

## 1. 작업 개요

구현 착수 전에 Dual-Track UI + Logic TDD, Clean Architecture, ECB, Concept-to-Code Traceability를 반영한 PRD를 작성했다.  
작업은 다음 4단계로 진행했다.

1. **참고 문서 분석 및 PRD 섹션 매핑** (본문 작성 없음)
2. **PRD v1.0 초안 작성** (23개 섹션 구조)
3. **PRD 검토** (7개 기준, 수정 없이 이슈 보고)
4. **PRD v1.1 개정** (검토 반영, TD-01/TD-02 행렬 검증 포함)

---

## 2. 참고 문서 및 우선순위

| 역할 | 저장소 문서 (실제 경로) | PRD 반영 영역 |
|------|-------------------------|---------------|
| 문제 정의·동기 | `Report/01_MagicSquare_ProblemDefinition_STEP1-5.md` | Background, Problem, Why Chain |
| 기능 계약·아키텍처 | `Report/02_MagicSquare_DualTrack_UI_Logic_TDD_CleanArchitecture.md` | I/O Contract, Invariant, Layer |
| 품질·개발 방식 | `Report/03_...`, `.cursorrules`, `.cursor/rules/*.mdc` | NFR, TDD, ECB, Constraints |
| 요구·검증 1차 | `Report/05_Level5_Scenario_Verification_and_Summary.md` | Journey, Story, Scenario 갭 |
| 규칙 운영 | `Report/04_MagicSquare_CursorRules_Modularization_Report.md` | Appendix 규칙 구조 |

**매핑 결론:** PRD 작성 가능(조건부). UserJourney 전용 원문(`Report/4.UserJourney...`)은 저장소에 동일 파일명이 없어 `Report/05`와 `Report/02`를 병용했다.

---

## 3. PRD v1.0 → v1.1 개정 요약

### 3.1 검토에서 확인된 주요 이슈 (v1.0)

| # | 기준 | 결과 |
|---|------|------|
| 1 | FR별 테스트 가능 AC | FR-05 실패/포맷 AC 부족 |
| 2 | AC ↔ Traceability | AC-05 Matrix 누락, AC-10~13 과묶음 |
| 3 | Boundary/Domain 분리 | FR-05 Layer 혼합 |
| 4 | 오류 정책 | OUTPUT_FORMAT, Domain 내부 오류 §13 미완 |
| 5 | TD-01/TD-02 구분 | ID만 있고 행렬 값 없음 |
| 6 | 1-index / row-major | 내부 0-index 정책 미명시 |
| 7 | 코드 미포함 | 통과 |

### 3.2 v1.1 반영 내용

| 항목 | 조치 |
|------|------|
| FR 분리 | `FR-05a` Solver(Domain), `FR-05b` ResultFormatter(Boundary), `FR-06` Control |
| AC 보강 | AC-05, AC-18~24, 행/열/대각선 AC-11~13 분리 |
| 오류 정책 | §13 전 항목 확정, dual-fail = `DOMAIN_NO_MAGIC_ASSIGNMENT` |
| 좌표 정책 | Domain 0-index, 외부 출력 1-index (BR-14) |
| 테스트 데이터 | TD-01(small-first), TD-02(reverse) 행렬·기대값 검증 후 기입 |
| Traceability | AC ID 열 포함 Matrix 재작성 |

### 3.3 검증된 대표 테스트 데이터

| ID | Attempt 1 | Attempt 2 | Expected `int[6]` (1-index) |
|----|-----------|-----------|----------------------------|
| TD-01 | 성공 | (미시도) | `[1, 2, 3, 1, 4, 13]` |
| TD-02 | 실패 | 성공 | `[1, 1, 16, 1, 2, 3]` |

행렬 정의는 `docs/PRD_MagicSquare.md` §16.4 참조.

**TD-07 (dual fail):** `[[14,1,5,9],[8,7,16,12],[6,10,2,11],[0,13,4,0]]` — 두 조합 모두 non-magic, 기대 에러 `DOMAIN_NO_MAGIC_ASSIGNMENT`.

---

## 4. PRD 산출물

| 파일 | 설명 | 버전 |
|------|------|------|
| `docs/PRD_MagicSquare.md` | 구현 전 기준 PRD 본문 | v1.1 |
| `Report/06_MagicSquare_PRD_PreImplementation_Report.md` | 본 보고서 | 1.0 |
| `Prompt/06_MagicSquare_PRD_transcript.md` | 세션 Transcript Export | 1.0 |

---

## 5. PRD 핵심 고정 사항 (구현 시 준수)

1. **입력:** 4x4, `0` 정확히 2개, 값 `0` 또는 `1~16`, non-zero unique  
2. **출력:** `int[6]`, 1-index, `[r1,c1,n1,r2,c2,n2]`  
3. **Solver:** small-first → reverse, dual-fail 시 표준 에러  
4. **Magic Constant:** `34` (`MAGIC_CONSTANT_4X4`)  
5. **Dual-Track:** Track A(Boundary), Track B(Domain) RED 분리  
6. **Coverage:** Domain ≥95%, Boundary ≥85%  
7. **입력 실패 시 Domain 미호출** (AC-05, AC-23)

---

## 6. Report/05 대비 PRD 보강 상태

| Report/05 권고 | PRD v1.1 반영 |
|----------------|---------------|
| 4x4 shape 시나리오 | TS-E-01, TD-03, RED-BND-VAL-004 |
| small-first 성공 | TS-N-01, TD-01, RED-DOM-SOL-002 |
| BlankFinder SC | FR-02, RED-DOM-BLK-001 |
| MissingFinder SC | FR-03, RED-DOM-MIS-001/002 |
| Validator 단독 SC | FR-04, RED-DOM-VAL-001~003 |

---

## 7. 생성/수정 파일

- `docs/PRD_MagicSquare.md` (생성)
- `Report/06_MagicSquare_PRD_PreImplementation_Report.md` (생성)
- `Prompt/06_MagicSquare_PRD_transcript.md` (생성)

---

## 8. 다음 권장 작업

1. PRD v1.1 기준으로 Track A/B RED 테스트 스켈레톤 작성 (pytest, AAA)  
2. `BoundaryValidator` → `SolveMagicSquareUseCase` → Domain 컴포넌트 순 Dual-Track 구현  
3. TD-01~TD-07을 회귀 테스트 fixture로 고정  
4. Traceability Matrix의 RED ID와 실제 테스트 파일명 1:1 매핑

---

*본 문서는 PRD 사전 작성·검토·개정 세션의 산출 보고서이며, 구현 코드 및 테스트 코드는 포함하지 않는다.*
