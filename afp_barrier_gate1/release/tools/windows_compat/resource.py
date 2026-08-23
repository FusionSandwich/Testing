"""Minimal test-only Windows compatibility shim for Unix ``resource``.

Use only by prepending this directory to ``PYTHONPATH`` for local regression
tests. It is not used to generate or certify committed scientific results.
"""

from __future__ import annotations

from collections import namedtuple


RUSAGE_SELF = 0
_Usage = namedtuple("struct_rusage", ["ru_maxrss"])


def getrusage(who: int) -> _Usage:
    if who != RUSAGE_SELF:
        raise ValueError("the test-only shim supports RUSAGE_SELF only")
    return _Usage(ru_maxrss=0)
