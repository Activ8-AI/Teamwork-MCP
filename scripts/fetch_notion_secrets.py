#!/usr/bin/env python3
"""
Charter-standard script to fetch secrets from Notion Secrets Registry.

Fetches secrets from Notion database and caches them locally for use in automation.
Never commits secrets to git (configs/notion_secrets.json is gitignored).

Usage:
    # With Notion token in environment
    export NOTION_TOKEN="secret_xxxx"
    ./scripts/fetch_notion_secrets.py

    # Or provide token as argument
    ./scripts/fetch_notion_secrets.py --notion-token secret_xxxx

    # Fetch and export GITHUB_TOKEN for immediate use
    export GITHUB_TOKEN=$(./scripts/fetch_notion_secrets.py --output-token GITHUB_TOKEN)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    print("ERROR: notion-client not installed. Run: pip3 install notion-client", file=sys.stderr)
    sys.exit(1)


# Notion Secrets Registry page ID
SECRETS_PAGE_ID = "90f3336e8fda4a8f8517ffd9559eae36"
SECRETS_CACHE = Path("configs/notion_secrets.json")


def fetch_secrets_from_notion(notion_token: str) -> dict[str, str]:
    """
    Fetch secrets from Notion Secrets Registry page.

    Args:
        notion_token: Notion API integration token

    Returns:
        Dictionary of secret key-value pairs
    """
    client = Client(auth=notion_token)

    try:
        # Retrieve the page content
        page = client.pages.retrieve(page_id=SECRETS_PAGE_ID)

        # Try to get database if it's a database
        try:
            database = client.databases.query(database_id=SECRETS_PAGE_ID)
            secrets = {}

            # Parse database rows for secrets
            for result in database.get("results", []):
                props = result.get("properties", {})

                # Look for Name/Key and Value columns
                name = None
                value = None

                for prop_name, prop_data in props.items():
                    prop_type = prop_data.get("type")

                    if prop_type == "title" and prop_data.get("title"):
                        name = prop_data["title"][0]["plain_text"]
                    elif prop_name.lower() in ["value", "secret", "token"] and prop_type == "rich_text":
                        if prop_data.get("rich_text"):
                            value = prop_data["rich_text"][0]["plain_text"]

                if name and value:
                    secrets[name] = value

            return secrets

        except Exception as db_err:
            # Not a database, try as page with properties
            props = page.get("properties", {})
            secrets = {}

            # Extract properties that look like secrets
            for prop_name, prop_data in props.items():
                prop_type = prop_data.get("type")

                if prop_type == "rich_text" and prop_data.get("rich_text"):
                    value = prop_data["rich_text"][0]["plain_text"]
                    secrets[prop_name] = value
                elif prop_type == "title" and prop_data.get("title"):
                    value = prop_data["title"][0]["plain_text"]
                    secrets[prop_name] = value

            return secrets

    except Exception as e:
        print(f"ERROR: Failed to fetch secrets from Notion: {e}", file=sys.stderr)
        print(f"Page ID: {SECRETS_PAGE_ID}", file=sys.stderr)
        raise


def cache_secrets(secrets: dict[str, str]) -> None:
    """
    Cache secrets to local file (gitignored).

    Args:
        secrets: Dictionary of secrets to cache
    """
    SECRETS_CACHE.parent.mkdir(parents=True, exist_ok=True)

    cache_data = {
        "source": "notion",
        "status": "active",
        "page_id": SECRETS_PAGE_ID,
        **secrets
    }

    SECRETS_CACHE.write_text(json.dumps(cache_data, indent=2))
    print(f"✓ Cached {len(secrets)} secrets to {SECRETS_CACHE}", file=sys.stderr)


def load_cached_secrets() -> dict[str, str]:
    """
    Load secrets from local cache.

    Returns:
        Dictionary of cached secrets, or empty dict if cache doesn't exist
    """
    if not SECRETS_CACHE.exists():
        return {}

    try:
        data = json.loads(SECRETS_CACHE.read_text())
        # Remove metadata keys
        return {k: v for k, v in data.items() if k not in ["source", "status", "page_id"]}
    except json.JSONDecodeError:
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch secrets from Notion Secrets Registry"
    )
    parser.add_argument(
        "--notion-token",
        help="Notion API token (or set NOTION_TOKEN env var)"
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="Use cached secrets if available (skip Notion fetch)"
    )
    parser.add_argument(
        "--output-token",
        metavar="KEY",
        help="Output only the specified token value (for export)"
    )

    args = parser.parse_args()

    # Get Notion token
    notion_token = args.notion_token or os.getenv("NOTION_TOKEN") or os.getenv("NOTION_API_KEY")

    # Try cache first if requested
    if args.use_cache:
        secrets = load_cached_secrets()
        if secrets:
            if args.output_token:
                print(secrets.get(args.output_token, ""))
                return 0
            print(json.dumps(secrets, indent=2))
            return 0

    # Fetch from Notion
    if not notion_token:
        print("ERROR: Notion token required. Set NOTION_TOKEN env var or use --notion-token", file=sys.stderr)
        print("\nTo get a Notion API token:", file=sys.stderr)
        print("1. Go to https://www.notion.so/my-integrations", file=sys.stderr)
        print("2. Create new integration or use existing", file=sys.stderr)
        print("3. Copy the Internal Integration Token", file=sys.stderr)
        print("4. Share the Secrets Registry page with the integration", file=sys.stderr)
        return 1

    try:
        secrets = fetch_secrets_from_notion(notion_token)

        if not secrets:
            print("WARNING: No secrets found in Notion page", file=sys.stderr)
            return 1

        # Cache for future use
        cache_secrets(secrets)

        # Output
        if args.output_token:
            print(secrets.get(args.output_token, ""))
        else:
            print(json.dumps(secrets, indent=2))

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
