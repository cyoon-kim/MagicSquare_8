# Defect List — Magic Square 4×4

| 항목 | 내용 |
|---|---|
| Document ID | DEF-MSQ-001 |
| Status | Active |
| Reference | `docs/test_plan.md`, `docs/PRD_MagicSquare.md` |

---

## Open Defects

| ID | Severity | Sprint | Test ID | Summary | Status |
|---|---|---|---|---|---|
| — | — | — | — | (none) | — |

---

## Closed Defects

| ID | Severity | Sprint | Test ID | Summary | Resolution |
|---|---|---|---|---|---|
| — | — | — | — | (none) | — |

---

## Template (copy for new entries)

```markdown
| DEF-001 | High | AC-01 | TC-A-01 | Expected INPUT_SIZE_INVALID, got exception | Open |
```

**Fields:** ID · Severity (Critical/High/Medium/Low) · Sprint · Test ID · Summary · Status/Resolution

---

## Regression Checklist

- [ ] All open defects resolved or deferred with reason
- [ ] `pytest tests/boundary tests/control -m p0` passes after fix
- [ ] Domain mock `assert_not_called()` still holds on AC-01 inputs
- [ ] Entry recorded in this file before closing sprint
