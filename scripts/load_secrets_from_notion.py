#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    secrets_path = Path(".secrets.cache.json")
    secrets_payload = {
        "source": "notion",
        "status": "stubbed",
    }
    secrets_path.write_text(json.dumps(secrets_payload, indent=2))
    print(f"Wrote stub secrets to {secrets_path}")


if __name__ == "__main__":
    main()
