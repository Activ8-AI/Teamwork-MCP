#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SECRETS_CACHE = Path("configs/notion_secrets.json")


def load_secrets_from_cache(path: Path = SECRETS_CACHE) -> dict[str, Any]:
    """
    Charter-safe placeholder secrets loader.

    - Reads from a local cache file if it exists.
    - Never writes secrets to disk.
    """
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def main() -> None:
    print(json.dumps(load_secrets_from_cache(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
