#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    """Write a stub `.secrets.cache.json` file for local development."""
    secrets_path = Path(".secrets.cache.json")
    secrets_payload = {
        "source": "notion",
        "status": "stubbed",
    }
    secrets_path.write_text(json.dumps(secrets_payload, indent=2), encoding="utf-8")
    print(f"Wrote stub secrets to {secrets_path}")


if __name__ == "__main__":
    main()
