# GREEN_DOCS — TDD GREEN 스프린트 로그

| GC-ID | Track | Test ID | Phase | 상태 | 문서 |
|-------|-------|---------|-------|------|------|
| GC-001 | A | BV-01 | feat | GREEN | [GC-001](GC-001_ac01_bv01_none.md) |
| GC-002 | A | BV-02~06 | feat | GREEN | [GC-002](GC-002_ac01_size_parametrize.md) |
| GC-003 | A-2 | AC-05 None domain | feat | GREEN | — |
| GC-004 | A-2 | AC-23 formatter | feat | GREEN | — |
| GC-005 | A-2 | AC-05 size parametrize | feat | GREEN | — |
| GC-006 | A | U-IN-04 | test+feat | GREEN | — |
| GC-007 | A | U-IN-05 | test+feat | GREEN | — |
| GC-008 | A | U-IN-06 | test+feat | GREEN | — |
| GC-009 | A | U-IN-07 | test+feat | GREEN | — |
| GC-010 | A | U-IN-08 | test+feat | GREEN | — |
| GC-011~015 | A | U-FLOW-02 | test+feat | GREEN | — |
| GC-016 | B | G0~G3 fixtures | test | GREEN | — |
| GC-017~028 | B | D-LOC~D-SOL | test+feat | GREEN | — |
| GC-029~031 | A | U-OUT-01~03 | test+feat | GREEN | — |
| GC-032 | — | coverage gate | docs | GREEN | [GC-032](GC-032_coverage_gate.md) |

**브랜치:** `stabilize/green`  
**Magic Square suite:** 43 passed (boundary 23 + control 5 + entity 15)  
**Legacy:** 5 passed (범위 외)

## Coverage snapshot

| Layer | Gate | Actual |
|-------|------|--------|
| boundary | 85% | 98.63% |
| entity | 95% | 96.55% |
| src global | 80% | 95.77% |

템플릿: [`_template.md`](_template.md)

## G1 SSOT note

G1 grid aligned to **PRD TD-01** (blanks 0-index `(0,1)`, `(0,3)`; expected `[1,2,3,1,4,13]`). Report/09 placeholder `[2,2,7,3,3,10]` superseded by PRD.
