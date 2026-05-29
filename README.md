# MagicSquare_cyoon

4×4 마방진(Magic Square)을 다루는 학습·연습 프로젝트입니다.  
현재는 **명세 완료 · RED 진행 중** — PRD v1.1, test_plan, contracts 고정 후 AC-01 Track A RED skeleton 작성 단계입니다.

---

## 프로젝트 개요

4×4 격자에 **1부터 16까지**의 정수를 각 칸에 한 번씩 놓았을 때, 정해진 **마법 선**(행·열·대각선)마다 합이 같고, 그 공통 합이 4×4 마방진의 **마법 상수(34)** 와 일치하는지를 **일관되게 판정**하는 것이 핵심입니다.

| 구분 | 내용 |
|------|------|
| **표면 문제 (피할 정의)** | “4×4 마방진을 완성하는 프로그램” |
| **진짜 문제** | 고정된 규칙으로 배치의 **유효성을 판정**하고, 조건·입출력·불변을 **먼저 명시**하는 연습 |
| **현재 단계** | PRD · test_plan · contracts 완료 → FR-01 AC-01 RED |
| **다음 단계** | RED 테스트 → GREEN 최소 구현 → Track B Domain |

---

## 왜 이 프로젝트인가

### 도메인 (4×4 마방진)

- 규모가 작아 **규칙 분해·검증·테스트** 연습에 적합합니다.
- “맞다/틀리다”가 명확하지만, **합 일치·숫자 집합·검사 범위**는 별도 조건입니다.

### 프로그램으로 다루는 이유

- **반복 가능성:** 같은 판정 절차를 임의의 배치에 반복 적용
- **검증 자동화:** 행·열·대각선·중복·범위를 누락 없이 검사
- **오류 방지:** 수기 계산에서 흔한 “한 줄만 확인” 실수 감소
- **규칙 기반 사고:** “마방진”을 검증 가능한 조건의 집합으로 다룸

### TDD를 전제로 하는 이유

- 여러 **독립 조건의 교집합**이므로, 테스트로 **판정 계약·불변·입출력**을 먼저 고정하지 않으면 요구가 구현 중에 바뀌기 쉽습니다.
- 통제의 중심은 UI가 아니라 **판정(검증) 코어**입니다.

---

## 핵심 불변 조건 (Invariant)

표준 정의: **4×4**, 값 **{1,…,16}** 각 1회, **행·열·주대각선·부대각선**을 마법 선으로 둠.

| ID | 불변 | 요약 |
|----|------|------|
| I1 | 격자 형태 | 4×4, 16칸 |
| I2 | 칸당 값 | 각 칸에 정확히 하나 |
| I3 | 숫자 집합 | 1~16 중복·누락 없음 |
| I5 | 마법 상수 | 각 마법 선의 합 = **34** |
| I7~I9 | 마법 선 | 4행 · 4열 · 2대각선 |
| I10~I13 | 판정 절차 | 동일 입력 → 동일 결과, 고정 검사 규칙, 정답/반례 예시 |

> **주의:** “모든 선의 합이 같다”만으로는 1~16 사용이 보장되지 않습니다. **숫자 집합(I3)** 과 **합 34(I5·I7~I9)** 는 별도로 다룹니다.

---

## 훈련하려는 사고 능력

1. **규칙 분해** — 마방진을 검증 가능한 조건 여러 개로 나눔  
2. **계약 사고** — 입력·성공/실패·(선택) 진단을 먼저 합의  
3. **불변 인식** — 변하지 않아야 할 것과 표현을 구분  
4. **경계·반례 설계** — 한 조건만 깨는 예시를 의도적으로 만듦  
5. **검증 우선** — “만들기”보다 “맞는지 판단하기”를 먼저 안정화  
6. **범위 통제** — 4×4 고정, 생성/UI는 판정 계약을 깨지 않는 한 후순위  
7. **명세 선행** — 구현 전에 조건·입출력·불변을 고정  

### 비목표 (이번 문제 정의 단계)

- 손으로 퍼즐을 빨리 푸는 속도
- 특정 구성 기법만 외우는 것
- 제품 수준의 UI·성능·배포 (별도 단계에서 다룰 수 있음)

---

## 문제 정의 워크숍 (STEP 1~5)

| STEP | 주제 | 핵심 |
|------|------|------|
| 1 | Observation | 16개 숫자 배치와 여러 선의 합 일치를 다루는 상황 |
| 2 | Why #1 | “완성” vs “검증”, 다중 규칙, 과정 vs 결과 |
| 3 | Why #2 | 프로그램 = 절차 복제·자동 판정·규칙 명시 |
| 4 | Why #3 | TDD로 판정 계약·불변·입출력 통제 |
| 5 | 진짜 문제 정의 | 표면/개선 정의, Invariant, 훈련 목표 |

상세 내용은 보고서를 참고하세요.

---

## 저장소 구조

```
MagicSquare_XX/
├── README.md
├── pyproject.toml              # pytest, pydantic, pytest-cov
├── docs/
│   ├── PRD_MagicSquare.md
│   ├── test_plan.md
│   ├── contracts.md            # API Single Source of Truth
│   └── defect_list.md
├── src/
│   ├── boundary/               # BoundaryValidator, ResultFormatter
│   ├── control/                # SolveMagicSquareUseCase
│   └── domain/                 # BlankFinder, Solver, ...
├── tests/
│   ├── boundary/
│   ├── control/
│   └── legacy/                 # User entity sample (out of RED scope)
├── legacy/
│   └── entity/user.py          # moved from src/entity (learning sample)
├── Report/
└── Prompt/
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) | FR/AC/BR, I/O 계약, Dual-Track TDD 전략 |
| [docs/test_plan.md](docs/test_plan.md) | FR-01 AC-01 테스트 계획 (BV, mock, pytest-cov) |
| [docs/contracts.md](docs/contracts.md) | API 시그니처 · Pydantic · error code Single Source |
| [docs/defect_list.md](docs/defect_list.md) | 결함 추적 템플릿 |
| [docs/red_implementation_checklist.md](docs/red_implementation_checklist.md) | 코드 Sprint 보류 항목 (legacy, skeleton, RED) |
| [Report/01_MagicSquare_ProblemDefinition_STEP1-5.md](Report/01_MagicSquare_ProblemDefinition_STEP1-5.md) | STEP 1~5 전체 산출물 |
| [Prompt/01_MagicSquare_ProblemDefinition_STEP1-5_prompt.md](Prompt/01_MagicSquare_ProblemDefinition_STEP1-5_prompt.md) | 문제 정의 워크숍 프롬프트 |

---

## 상태

- [x] STEP 1 — Observation  
- [x] STEP 2 — Why #1  
- [x] STEP 3 — Why #2  
- [x] STEP 4 — Why #3  
- [x] STEP 5 — 진짜 문제 정의  
- [x] PRD v1.1 — Functional Requirements · Error Policy  
- [x] test_plan v1.1 — FR-01 AC-01  
- [x] contracts.md — API / terminology 고정  
- [ ] FR-01 AC-01 RED 테스트  
- [ ] FR-01 GREEN (BoundaryValidator)  
- [ ] Track B Domain RED (FR-02~05a)  
- [ ] 실행 환경 · CI gate  
- [ ] (선택) 생성기 · UI  

---

## RED 단계 To-Do 리스트

> [`docs/test_plan.md`](docs/test_plan.md) · [`docs/PRD_MagicSquare.md`](docs/PRD_MagicSquare.md) · [`docs/contracts.md`](docs/contracts.md) 기반.  
> **Sprint 범위:** FR-01 AC-01 · AC-05 · AC-23 · TS-E-01 · 공개 파라미터명 **`matrix`**

### Track A — Boundary (FR-01)

- [ ] TC-A-01 (BV-01): `matrix=None` → `ErrorResponse`, 예외 throw 없음 (AC-01, §13)
- [ ] TC-A-02: `error.code == "INPUT_SIZE_INVALID"` (AC-01, §12.1)
- [ ] TC-A-03: `error.message == "Input matrix must be 4x4."` (§13)
- [ ] TC-A-05 (BV-02): `matrix=[]` → `INPUT_SIZE_INVALID` (AC-01)
- [ ] TC-A-06 (BV-03): `matrix=[[]]*4` → `INPUT_SIZE_INVALID` (AC-01)
- [ ] TC-A-07 (BV-04~06): 3×4 · 4×3 · 5×5 · TD-03 → `INPUT_SIZE_INVALID` (AC-01, TS-E-01)
- [ ] TC-A-08: §13 Pydantic `ErrorResponse` 스키마 준수
- [ ] TC-A-09: TD-01(4×4 정상) 테스트 **미포함** 확인

### Track A-2 — Control 격리 (FR-06, AC-05, AC-23)

- [ ] TC-A2-01 (TC-A-04): `matrix=None` 시 Domain chain 0회 — `BlankFinder` · `MissingNumberFinder` · `MagicSquareValidator` · `Solver` mock/spy
- [ ] TC-A2-02: `ResultFormatter.format()` 0회 호출 (FR-01 fail path)
- [ ] TC-A2-03: Domain/Formatter mock `call_count > 0` → 테스트 실패
- [ ] TC-A2-04: AC-02~04(TS-E-02~04) **본 Sprint RED 미포함** 확인

### Track B — Domain Logic (FR-02~05a)

> **본 Sprint OUT OF SCOPE** — skeleton stub만 존재. RED는 FR-02~05a Sprint에서 진행.

### 커버리지 목표 (Sprint AC-01)

- [ ] Boundary (`src/boundary`): **85%+** — `pytest --cov=src/boundary --cov-fail-under=85`
- [ ] Control (`src/control`): **85%+** — early-return 분기
- [ ] Domain: **호출 0회** (stub OK) — FR-02~05a Sprint에서 **95%+**
- [ ] `pip install pytest-cov` → `pytest --cov=src --cov-report=term-missing`

### 결함 목록 연결

- [ ] [`docs/defect_list.md`](docs/defect_list.md) 발견 결함 기록
- [ ] 결함 수정 후 회귀 테스트 통과

---

## 라이선스

미정 (추가 예정)
