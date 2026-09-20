from __future__ import annotations

import sys
from pathlib import Path

from api.content import CONTENT_DIR, ContentError, ContentStore


def check(content_dir: Path) -> int:
    try:
        store = ContentStore(content_dir)
    except ContentError as exc:
        print(f"content error: {exc}")
        return 1
    print(f"OK: {len(store)} topics")
    return 0


def main() -> int:
    return check(CONTENT_DIR)


if __name__ == "__main__":
    sys.exit(main())
