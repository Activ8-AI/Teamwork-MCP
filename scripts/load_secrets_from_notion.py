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
