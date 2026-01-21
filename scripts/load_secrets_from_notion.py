#!/usr/bin/env python3
from __future__ import annotations

"""Local placeholder secrets loader.

This repository intentionally does not ship secrets. This script reads a local
JSON cache (ignored by git) if you have one.
"""

import json
from pathlib import Path
from typing import Any, Dict

SECRETS_CACHE = Path("configs/notion_secrets.json")

def load_secrets_from_notion() -> Dict[str, Any]:
    """Placeholder secrets loader that reads from a local cache if it exists."""
    if not SECRETS_CACHE.exists():
        return {}
    return json.loads(SECRETS_CACHE.read_text(encoding="utf-8"))


def main() -> None:
    print(json.dumps(load_secrets_from_notion(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
