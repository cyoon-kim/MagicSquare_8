# tests/entity — Track B (Domain / ECB Entity Layer)

실습 §6 및 PRD FR-02~05a Domain Logic RED/GREEN 테스트를 이 폴더에 둡니다.

| 포함 | 제외 |
|---|---|
| `BlankFinder`, `MissingNumberFinder`, `MagicSquareValidator`, `Solver` | User 샘플 → `tests/legacy/` |

커버리지:

```bash
python -m pytest tests/entity/ --cov=src/entity --cov-report=term-missing
```
