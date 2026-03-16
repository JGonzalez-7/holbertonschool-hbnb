"""Test configuration for Part 3."""

from __future__ import annotations

import sys
from pathlib import Path

PART3_DIR = Path(__file__).resolve().parents[1]

if str(PART3_DIR) not in sys.path:
    sys.path.insert(0, str(PART3_DIR))
