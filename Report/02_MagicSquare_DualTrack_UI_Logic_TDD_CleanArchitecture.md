# Magic Square (4x4) — Dual-Track UI + Logic TDD / Clean Architecture 보고서

> **Superseded (partial):** Input validation location — authoritative source is [`docs/PRD_MagicSquare.md`](../docs/PRD_MagicSquare.md) **FR-01** (`BoundaryValidator` in Boundary layer). Report §1.4 `validateInput` as Domain API is deprecated. See [`docs/contracts.md`](../docs/contracts.md).

## 문서 목적
- 알고리즘 구현이 아니라 **레이어 분리**, **계약 기반 테스트**, **리팩토링 안전성** 훈련을 위한 설계 산출물 고정
- 고정 입력/출력 계약을 기준으로 Domain/UI/Data/Integration 검증 기준 정의

## 고정 계약
- **입력**
  - `4x4 int[][]` (0은 빈칸)
  - 빈칸(0)은 정확히 2개
  - 값 범위: 0 또는 1~16
  - 0 제외 중복 금지
- **출력**
  - `int[6]`
  - 좌표는 1-index
  - 반환 형식: `[r1,c1,n1,r2,c2,n2]`
  - 순서 규칙: `(small->firstBlank, large->secondBlank)` 조합이 마방진이면 유지, 아니면 reverse

---

## 1) Logic Layer (Domain Layer) 설계

### 1.1 도메인 개념
- **Entity**
  - `PuzzleGrid`: 4x4 행렬 상태 및 유효 접근 책임
- **Value Objects**
  - `CellPosition`: 1-index 좌표 유효성
  - `MissingNumbers`: 누락 숫자 2개(오름차순)
  - `CandidateAssignment`: 두 빈칸-두 숫자 조합 1건 표현
- **Domain Services**
  - `InputContractValidator`: 입력 계약 위반 판정
  - `BlankCellLocator`: 빈칸 2개 좌표 탐색
  - `MissingNumberFinder`: 누락 숫자 2개 산출
  - `MagicSquareJudge`: 행/열/대각선 합 판정
  - `DualCandidateResolver`: small-first 후 reverse fallback

### 1.2 도메인 불변조건(Invariants)
- `I1`: 행렬은 정확히 4x4
- `I2`: 0의 개수는 정확히 2
- `I3`: 각 값은 0 또는 1~16
- `I4`: 0 제외 중복 없음
- `I5`: 누락 숫자 개수는 정확히 2
- `I6`: 완성 판정의 Magic Constant는 34
- `I7`: 결과 길이 6, 좌표 1-index
- `I8`: 순서 규칙(small-first, 실패 시 reverse)

### 1.3 핵심 유스케이스(도메인 관점)
- `UC1` 빈칸 찾기: `PuzzleGrid -> CellPosition[2]`
- `UC2` 누락 숫자 찾기: `PuzzleGrid -> MissingNumbers`
- `UC3` 마방진 판정: `PuzzleGrid(no zero) -> boolean`
- `UC4` 두 조합 시도: `(blank2, missing2) -> int[6]`

### 1.4 Domain API(내부 계약)
- `validateInput(matrix) -> ValidationResult`
  - 실패: `INPUT_SIZE_INVALID`, `INPUT_BLANK_COUNT_INVALID`, `INPUT_VALUE_RANGE_INVALID`, `INPUT_DUPLICATE_NON_ZERO`
- `locateBlankCells(grid) -> CellPosition[2]`
  - 실패: `DOMAIN_BLANK_COUNT`
- `findMissingNumbers(grid) -> MissingNumbers`
  - 실패: `DOMAIN_MISSING_COUNT`
- `isMagic(grid) -> boolean`
  - 실패: `DOMAIN_MAGIC_UNCHECKABLE`
- `resolveTwoCandidates(grid) -> int[6]`
  - 실패: `DOMAIN_NO_MAGIC_ASSIGNMENT`

### 1.5 Domain 단위 테스트 설계(RED 우선)
- **정상**
  - `D-RED-01`: 계약 유효 입력 통과 (`I1~I4`)
  - `D-RED-06`: 누락 숫자 산출 (`I5`)
  - `D-RED-07`: 마방진 판정 true (`I6`)
  - `D-RED-08`: small-first 성공 (`I8`)
  - `D-RED-09`: reverse 성공 (`I8`)
- **비정상/엣지**
  - `D-RED-02`: 크기 오류 (`I1`)
  - `D-RED-03`: 빈칸 개수 오류 (`I2`)
  - `D-RED-04`: 범위 오류 (`I3`)
  - `D-RED-05`: 중복 오류 (`I4`)
  - `D-RED-10`: 두 조합 모두 실패 (`I6`,`I8`)

---

## 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

### 2.1 사용자/호출자 관점 시나리오
1. 호출자가 4x4 행렬 입력
2. UI Boundary가 계약 검증
3. 실패 시 Error schema 즉시 반환
4. 성공 시 Domain 호출
5. 결과를 Output schema로 정규화하여 반환

### 2.2 UI 계약(외부 계약)
- **Input schema**: `{ matrix: int[4][4] }`
- **Output schema**: `{ result: int[6] }`
- **Error schema**: `{ error: { code, message, details? } }`

### 2.3 UI 레벨 테스트(Contract-first, RED 우선)
- `UI-RED-01`: 잘못된 크기
- `UI-RED-02`: 빈칸 개수 오류
- `UI-RED-03`: 값 범위 오류
- `UI-RED-04`: 중복 오류
- `UI-RED-05`: 반환 포맷 검증
- `UI-RED-06`: 정상 응답 포워딩
- 조건: Domain은 Mock으로 고정

### 2.4 UX/출력 규칙
- 에러 메시지 규칙
  - `code`: UPPER_SNAKE_CASE 고정
  - `message`: 고정 영문 문장(마침표 포함)
  - 같은 code는 항상 같은 message
- 표준 코드 예
  - `INPUT_SIZE_INVALID`
  - `INPUT_BLANK_COUNT_INVALID`
  - `INPUT_VALUE_RANGE_INVALID`
  - `INPUT_DUPLICATE_NON_ZERO`
  - `OUTPUT_FORMAT_INVALID`
  - `DOMAIN_NO_MAGIC_ASSIGNMENT`

---

## 3) Data Layer 설계

### 3.1 목적 정의
- DB가 아닌 학습용 저장/로드 경계
- 입력 행렬 저장/로드 필수
- 실행 결과 저장/로드는 선택

### 3.2 인터페이스 계약
- `saveInput(sessionId, matrix)`
- `loadInput(sessionId)`
- `saveResult(sessionId, result)` (선택)
- `loadResult(sessionId)` (선택)
- 저장/로드 시 4x4, int[6] 형식 검증 수행

### 3.3 구현 옵션 비교
- **옵션 A: InMemory**
  - 장점: 테스트 속도 빠름, I/O 없음
  - 단점: 프로세스 종료 시 유실
- **옵션 B: File(JSON/CSV)**
  - 장점: 재현 가능 로그 보존
  - 단점: 파일 없음/파싱 오류/권한 처리 필요
- **추천안**: 옵션 A(InMemory) 기본 채택, File은 통합 검증 보조

### 3.4 Data 레이어 테스트
- `DATA-RED-01`: 저장/로드 정합성
- `DATA-RED-02`: 파일 없음 예외
- `DATA-RED-03`: 형식 오류 예외
- `DATA-RED-04`: 4x4 불변조건 위반 차단

---

## 4) Integration & Verification

### 4.1 통합 경로 정의
- `UI Boundary -> Application(선택) -> Domain -> Data`
- 의존성 방향 고정
  - UI는 Domain 계약 의존
  - Domain은 UI/Data 구현에 비의존
  - Data는 Domain 포트 구현

### 4.2 통합 테스트 시나리오
- **정상**
  - `INT-PASS-01`: small-first 조합 성공
  - `INT-PASS-02`: small-first 실패 후 reverse 성공
- **실패**
  - `INT-FAIL-01`: 입력 오류(UI 차단)
  - `INT-FAIL-02`: 도메인 조합 실패
  - `INT-FAIL-03`: 데이터 저장 실패
  - `INT-FAIL-04`: 데이터 로드 형식 오류

### 4.3 회귀 보호 규칙
- 기존 RED 테스트 삭제 금지
- 계약/출력 포맷 변경 시 버전 변경 필수
- `int[6]` 출력 포맷 고정
- 에러 코드 문자열 변경 금지

### 4.4 커버리지 목표
- Domain Logic: 95%+
- UI Boundary: 85%+
- Data: 80%+

### 4.5 Traceability Matrix
| Concept(Invariant) | Rule | Use Case | Contract | Test | Component |
|---|---|---|---|---|---|
| I2 빈칸=2 | 0은 정확히 2개 | UC1 | validateInput / Input schema | D-RED-03, UI-RED-02, INT-FAIL-01 | InputContractValidator, UI Boundary |
| I3 값 범위 | 0 또는 1~16 | UC2 | validateInput | D-RED-04, UI-RED-03 | InputContractValidator |
| I4 중복 금지 | 0 제외 unique | UC2 | validateInput | D-RED-05, UI-RED-04 | InputContractValidator |
| I6 합=34 | 행/열/대각선 | UC3 | isMagic | D-RED-07, D-RED-10, INT-FAIL-02 | MagicSquareJudge |
| I8 순서 결정 | small-first else reverse | UC4 | resolveTwoCandidates / Output schema | D-RED-08, D-RED-09, INT-PASS-02 | DualCandidateResolver, UI Boundary |
| Data 4x4 유지 | 저장/로드에도 동일 | Save/Load | Repository 계약 | DATA-RED-01, DATA-RED-04, INT-FAIL-04 | MatrixRepository |

---

## 부록
- 상세 시각화 버전: `c:\Users\usejen_id\.cursor\projects\c-DEV\canvases\magic-square-4x4-tdd-architecture.canvas.tsx`
