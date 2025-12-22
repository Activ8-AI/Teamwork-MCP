import json
from pathlib import Path

SECRETS_CACHE = Path("configs/notion_secrets.json")


def load_secrets_from_notion() -> dict:
    """Placeholder secrets loader that reads from a local cache if it exists."""
    if not SECRETS_CACHE.exists():
        return {}
    return json.loads(SECRETS_CACHE.read_text())


if __name__ == "__main__":
    print(json.dumps(load_secrets_from_notion(), indent=2))
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
