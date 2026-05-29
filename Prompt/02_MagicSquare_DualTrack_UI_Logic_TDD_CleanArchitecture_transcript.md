# Magic Square (4x4) — Dual-Track UI + Logic TDD 대화형 Transcript
_Exported: 2026-05-28 (KST)_

---

## User
당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.  
프로젝트: Magic Square (4x4) — TDD 연습용  
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련  
제약:  
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)  
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의  
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만  
- 입력/출력은 명확히 고정  

입력 계약:  
- 4x4 int[][] (0은 빈칸)  
- 빈칸은 정확히 2개  
- 값 범위: 0 또는 1~16  
- 0 제외 중복 금지  

출력 계약:  
- int[6]  
- 좌표는 1-index  
- 반환 형식: [r1,c1,n1,r2,c2,n2]  
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로  

출력 형식(필수):  
1) Logic Layer 설계  
2) Screen Layer 설계  
3) Data Layer 설계  
4) Integration & Verification  
그리고 다음 추가 조건:  
- 모호한 표현 금지  
- 모든 규칙은 검증 가능해야 함  
- 구현 코드 작성 금지  
- 표/체크리스트 적극 사용  

---

## Assistant
요청 형식에 맞춰 **구현 코드 없이** 다음을 제공함:

1. **Logic Layer (Domain)**
   - Entity/VO/Domain Service 책임(SRP)
   - Invariants(I1~I8): 크기, 빈칸 수, 범위, 중복, 누락 수, 합=34, 출력 포맷, 순서 규칙
   - Use Case(빈칸 탐색/누락 수 계산/마방진 판정/두 조합 시도)
   - Domain API 계약(시그니처 수준 + 실패 코드)
   - RED 우선 테스트 케이스(정상/비정상/엣지 + 보호 invariant)

2. **Screen Layer (Boundary)**
   - 입력→검증→도메인 호출→출력 정규화 시나리오
   - Input/Output/Error schema 고정
   - Domain Mock 전제 UI 계약 테스트(크기/빈칸/범위/중복/포맷)
   - 에러 메시지 표준(code/message 규칙, 고정 문구)

3. **Data Layer**
   - 저장/로드 경계 목적 정의(학습용)
   - Repository 인터페이스 계약(save/load input/result)
   - InMemory vs File(JSON/CSV) 옵션 비교 및 기본 추천안(InMemory)
   - 저장/로드 정합성/예외/4x4 불변 테스트

4. **Integration & Verification**
   - UI -> Application(선택) -> Domain -> Data 통합 경로와 의존성 방향
   - 정상 2+, 실패 3+ 통합 시나리오
   - 회귀 보호 규칙(계약/포맷 고정, 기존 테스트 삭제 금지)
   - 커버리지 목표(Domain 95%+, UI 85%+, Data 80%+)
   - Traceability Matrix(Concept -> Rule -> Use Case -> Contract -> Test -> Component)

---

## User
@MagicSquare_XX/ 기준으로 다음의 순서로 실행해줘  
1. Report 폴더에 보고서 생성해줘  
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompting 폴더에 Export transcript 해줘

---

## Assistant
요청 반영 결과:
- `Report` 폴더에 설계 보고서 생성
- `Prompting` 폴더에 대화형 transcript 생성

생성 파일:
- `Report/02_MagicSquare_DualTrack_UI_Logic_TDD_CleanArchitecture.md`
- `Prompting/02_MagicSquare_DualTrack_UI_Logic_TDD_CleanArchitecture_transcript.md`

