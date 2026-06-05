"""Pytest bootstrap for importing workspace packages from src layout."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
API_SRC = ROOT / "apps" / "api" / "src"
CONTRACTS_SRC = ROOT / "packages" / "contracts" / "src"

for path in (str(API_SRC), str(CONTRACTS_SRC)):
    if path not in sys.path:
        sys.path.insert(0, path)