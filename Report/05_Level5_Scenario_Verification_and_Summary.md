# Level 5: Scenario Verification and Summary

## 1. Overall Judgment

- 적합성 점수: **7.4 / 10**
- 현재 상태: **일부 수정 필요**
- 요약 판단:  
  Epic→Journey→Story 연결은 전반적으로 잘 정렬되어 있고, Boundary/Domain 분리 및 불변식 중심 구조도 명확합니다. 다만 **Level 4 Technical Scenario가 Story의 Acceptance Criteria를 충분히 커버하지 못해**(특히 Story 2/3/4 및 Normal small-first 성공 케이스), 다음 단계 전 보강이 필요합니다.

---

## 2. Epic → Journey Consistency Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| Epic의 성공 기준이 Journey에 반영되었는가? | [~] | Journey Stage 2/4/5에서 계약, Dual-Track, 회귀 보호 반영 | 커버리지 95%, 계약 테스트 100% 같은 정량 지표는 Journey에 직접 연결 약함 → Stage별 측정 지표 추가 |
| Journey의 각 단계가 Epic 목표 달성에 기여하는가? | [x] | Stage 1~5가 불변식→계약→분리→TDD→회귀 순으로 구성 | - |
| Pain Point가 명확히 정의되었는가? | [x] | 각 Stage에 Pain Point 명시됨 | - |
| 불변식 기반 사고 훈련이 Journey에 드러나는가? | [x] | Stage 1/3/5에서 불변식 중심으로 명시 | - |
| Dual-Track TDD 흐름이 Journey에 반영되었는가? | [x] | Stage 4에 UI RED / Logic RED 분리 명시 | - |

---

## 3. Journey → User Story Consistency Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| Journey 각 Stage마다 최소 1개 이상의 User Story가 있는가? | [x] | S1~S5가 Stage 2~5 목표를 커버 | Stage 1(Problem Recognition) 전용 Story 1개 추가 시 더 명확 |
| User Story가 실제 기능 단위로 변환 가능한가? | [x] | 입력검증, 빈칸탐색, 누락탐색, 검증기, Solver로 분리 | - |
| Acceptance Criteria가 측정 가능한 문장인가? | [x] | 대부분 조건-판정형 문장으로 구성 | 오류 타입/코드 형태를 Story 1에서 더 구체화하면 자동화 용이 |
| Boundary Story와 Domain Story가 분리되어 있는가? | [x] | S1(Boundary), S2~S4(Domain), S5(Domain+Output) | - |
| 각 Story가 보호하는 Contract 또는 Invariant가 명시되어 있는가? | [x] | 각 Story 섹션에 Protected 항목 명시 | - |

---

## 4. Story → Technical Scenario Consistency Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| 모든 Acceptance Criteria가 Gherkin Scenario로 변환되었는가? | [ ] | SC-DOM-SOL-001, SC-BND-VAL-001~003만 존재 | S2/S3/S4 전용 시나리오 추가 필요 |
| Given-When-Then이 명확한가? | [x] | Level 4 시나리오 구조가 명확 | - |
| 각 Scenario가 자동화 테스트로 변환 가능한가? | [x] | 입력/실패/성공 조건이 명시됨 | - |
| 각 Scenario마다 대상 Layer가 명시되어 있는가? | [x] | Domain/Solver, Boundary 명시 | - |
| 각 Scenario가 Future RED Test ID로 분해 가능한가? | [x] | RED-DOM-SOL-001, RED-BND-VAL-001~003 | 누락 시나리오에도 RED ID 사전 정의 필요 |
| 각 Scenario가 Implementation Task로 분해 가능한가? | [x] | TASK-DOM-SOL-001, TASK-BND-VAL-001~003 | 누락 시나리오에도 TASK ID 추가 필요 |

---

## 5. MagicSquare Edge Case Coverage

### Normal Case

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| small-first 성공 시나리오가 존재하는가? | [ ] | 현존 시나리오는 small-first 실패 후 reverse 성공만 있음 | `SC-DOM-SOL-002` 추가 (small-first 즉시 성공) |
| small-first 실패 후 reverse 성공 시나리오가 존재하는가? | [x] | `SC-DOM-SOL-001` | - |
| 최종 결과가 int[6] 형식으로 검증되는가? | [x] | `SC-DOM-SOL-001` Then 절 | - |
| 최종 좌표가 1-index로 검증되는가? | [x] | `SC-DOM-SOL-001` Then 절 | - |

### Exception Case

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| 4x4가 아닌 입력 검증 시나리오가 있는가? | [ ] | 명시된 SC 없음 | `SC-BND-VAL-004` 추가 |
| 빈칸 개수가 2개가 아닌 경우가 검증되는가? | [x] | `SC-BND-VAL-001` | - |
| 0을 제외한 중복 숫자가 검증되는가? | [x] | `SC-BND-VAL-002` | - |
| 값이 0 또는 1~16 범위를 벗어나는 경우가 검증되는가? | [x] | `SC-BND-VAL-003` | - |
| 입력 검증 실패 시 Domain resolver가 호출되지 않는가? | [x] | SC-BND-VAL-001~003에 공통 명시 | - |

### Boundary Case

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| 최소값 1이 유효값으로 처리되는가? | [~] | S3/S5 AC에 암시, 전용 SC 없음 | `SC-BND-VAL-005` 또는 Domain 정상 케이스로 명시 검증 |
| 최대값 16이 유효값으로 처리되는가? | [~] | 예시 행렬에 16 포함, 독립 검증 아님 | 경계값 전용 시나리오 추가 |
| 0은 빈칸으로만 처리되는가? | [~] | S2/S3 AC에 존재, Technical SC 부재 | `SC-DOM-BLK-001` 추가 |
| 누락 숫자가 정확히 2개인지 검증되는가? | [ ] | Story 3에만 존재, SC 부재 | `SC-DOM-MIS-001` 추가 |
| 누락 숫자가 오름차순으로 반환되는가? | [ ] | Story 3에만 존재, SC 부재 | `SC-DOM-MIS-002` 추가 |

---

## 6. Invariant Coverage Check

| Invariant | Covered by Story | Covered by Scenario | Future RED Test ID | Status |
|---|---|---|---|---|
| 입력은 4x4여야 한다 | S1 | (미정) | (제안) `RED-BND-VAL-004` | [ ] |
| 빈칸은 정확히 2개여야 한다 | S1, S2 | `SC-BND-VAL-001` | `RED-BND-VAL-001` | [x] |
| 값은 0 또는 1~16이어야 한다 | S1 | `SC-BND-VAL-003` | `RED-BND-VAL-003` | [x] |
| 0을 제외한 중복 숫자는 금지된다 | S1 | `SC-BND-VAL-002` | `RED-BND-VAL-002` | [x] |
| 누락 숫자는 정확히 2개여야 한다 | S3 | (미정) | (제안) `RED-DOM-MIS-001` | [ ] |
| 누락 숫자는 오름차순이어야 한다 | S3 | (미정) | (제안) `RED-DOM-MIS-002` | [ ] |
| 모든 행의 합은 34여야 한다 | S4 | `SC-DOM-SOL-001`(성공 케이스) | `RED-DOM-SOL-001` | [x] |
| 모든 열의 합은 34여야 한다 | S4 | `SC-DOM-SOL-001`(성공 케이스) | `RED-DOM-SOL-001` | [x] |
| 두 대각선의 합은 각각 34여야 한다 | S4 | `SC-DOM-SOL-001`(성공 케이스) | `RED-DOM-SOL-001` | [x] |
| 결과는 int[6]이어야 한다 | S5 | `SC-DOM-SOL-001` | `RED-DOM-SOL-001` | [x] |
| 결과 좌표는 1-index여야 한다 | S5 | `SC-DOM-SOL-001` | `RED-DOM-SOL-001` | [x] |

---

## 7. Dual-Track TDD Readiness Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| UI/Boundary RED 테스트로 분리 가능한가? | [x] | SC-BND-VAL-001~003 존재 | 4x4 shape/경계값 SC 추가 시 완성도 상승 |
| Logic/Domain RED 테스트로 분리 가능한가? | [~] | Solver 시나리오 1개 존재 | BlankFinder/MissingFinder/Validator 시나리오 추가 필요 |
| GREEN 단계에서 최소 구현으로 처리 가능한가? | [x] | Story 분해가 모듈 책임 단위 | - |
| REFACTOR 단계에서 계약 변경 없이 구조 개선 가능한가? | [x] | 계약/불변식이 별도 명시됨 | - |
| 테스트 약화 없이 통과 가능한 구조인가? | [~] | 핵심 축은 존재 | 누락된 RED 시나리오 보강 필요 |

---

## 8. Implementation Possibility Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| BlankFinder로 분리 가능한가? | [x] | Story 2 정의됨 | 전용 SC/RED 추가 권장 |
| MissingNumberFinder로 분리 가능한가? | [x] | Story 3 정의됨 | 전용 SC/RED 추가 권장 |
| MagicSquareValidator로 분리 가능한가? | [x] | Story 4 정의됨 | Validator 단독 SC 추가 권장 |
| Solver로 분리 가능한가? | [x] | Story 5 + SC-DOM-SOL-001 | small-first 성공 SC 추가 |
| Boundary Validator로 분리 가능한가? | [x] | Story 1 + SC-BND 시리즈 | 4x4 shape SC 추가 |
| 하드코딩 없이 구현 가능한가? | [x] | Story 5에 하드코딩 금지 명시 | - |
| 매직 넘버가 명명된 상수로 대체 가능한가? | [x] | Epic/L1에서 상수 정책 명시 | Story/Scenario 레벨에 상수명 추적 링크 추가하면 더 좋음 |

---

## 9. Traceability Matrix

| Epic Goal | Journey Stage | User Story | Acceptance Criteria | Technical Scenario | Future RED Test ID | Future Implementation Task |
|---|---|---|---|---|---|---|
| 입력/출력 계약 명확화 | Stage 2 | S1 입력 검증 | 빈칸 2개 아님 시 실패 + Domain 미호출 | SC-BND-VAL-001 | RED-BND-VAL-001 | TASK-BND-VAL-001 |
| 입력/출력 계약 명확화 | Stage 2 | S1 입력 검증 | 0 제외 중복 존재 시 실패 + Domain 미호출 | SC-BND-VAL-002 | RED-BND-VAL-002 | TASK-BND-VAL-002 |
| 입력/출력 계약 명확화 | Stage 2 | S1 입력 검증 | 값 범위 위반 시 실패 + Domain 미호출 | SC-BND-VAL-003 | RED-BND-VAL-003 | TASK-BND-VAL-003 |
| 불변식 기반 Solver 흐름 | Stage 4 | S5 두 조합 시도 | small-first 실패 시 reverse 시도 후 성공 반환 | SC-DOM-SOL-001 | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| 도메인 책임 분리 | Stage 3 | S2 빈칸 좌표 탐색 | 0 탐지, row-major, 좌표 기준 명시 | (미정) | (제안) RED-DOM-BLK-001 | (제안) TASK-DOM-BLK-001 |
| 도메인 책임 분리 | Stage 3 | S3 누락 숫자 탐색 | 누락 2개, 오름차순 반환 | (미정) | (제안) RED-DOM-MIS-001/002 | (제안) TASK-DOM-MIS-001/002 |
| 마방진 불변식 검증 | Stage 4 | S4 마방진 검증 | 행/열/대각선 34 동시 만족만 true | (부분: SOL 시나리오에 내포) | (제안) RED-DOM-VAL-001 | (제안) TASK-DOM-VAL-001 |

---

## 10. Missing Items / Correction Needed

| Missing or Weak Item | Why It Matters | Suggested Fix |
|---|---|---|
| 4x4 shape 오류 시나리오 부재 | Story 1 AC 누락으로 Boundary 계약 불완전 | `SC-BND-VAL-004` + `RED-BND-VAL-004` 추가 |
| small-first 성공 시나리오 부재 | Solver 분기 검증이 한쪽(reverse 성공)으로 편향 | `SC-DOM-SOL-002` 추가 |
| Story 2(BlankFinder) 시나리오 부재 | 좌표 순서/인덱스 기준 회귀 위험 | `SC-DOM-BLK-001` 추가 |
| Story 3(MissingFinder) 시나리오 부재 | 누락 숫자 2개/오름차순 불변식 미검증 | `SC-DOM-MIS-001`, `SC-DOM-MIS-002` 추가 |
| Story 4(Validator) 단독 시나리오 부재 | 합34 판정 로직이 Solver에 종속되어 원인 분리 약함 | `SC-DOM-VAL-001~003`(행/열/대각선 실패 분리) 추가 |
| 경계값(1,16,0 의미) 독립 검증 약함 | Boundary Case 커버리지 부족 | 경계값 전용 Boundary/Domain 시나리오 추가 |

---

## 11. Final Summary

- 검증 결과: **구조는 강하지만 시나리오 커버리지가 불완전하여 일부 수정 필요**
- 가장 강한 부분: **Boundary 입력 오류 3종과 Solver reverse 시도 시나리오의 명확한 분해 가능성(RED/TASK 연결)**
- 가장 약한 부분: **Story 2/3/4에 대응하는 Technical Scenario 부재로 인한 추적성 공백**
- 반드시 수정해야 할 항목:  
  1) `4x4 shape` 검증 시나리오 추가  
  2) `small-first 성공` 시나리오 추가  
  3) BlankFinder/MissingFinder/Validator 전용 시나리오 및 RED ID 추가
- 다음 단계로 진행 가능 여부: **조건부 가능** (위 3개 보강 후 Level 6로 진행 권장)
