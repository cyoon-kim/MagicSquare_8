"""GM-1 pytest path alias — implementation lives in ``test_gm_01_magic_square_golden_master``."""

from __future__ import annotations

from test_gm_01_magic_square_golden_master import TestGoldenMasterMagicSquare as _Gm01Tests


class TestGoldenMasterMagicSquare(_Gm01Tests):
    """Alias for ``test_golden_master_magic_square.py`` pytest path."""

    __test__ = False
