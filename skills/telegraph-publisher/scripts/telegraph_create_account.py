#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from telegraph_common import TelegraphError, telegraph_call


def main() -> int:
    p = argparse.ArgumentParser(description="Create Telegra.ph account/access token")
    p.add_argument("--short-name", required=True, help="1-32 chars")
    p.add_argument("--author-name", default="Loptr")
    p.add_argument("--author-url", default="")
    args = p.parse_args()

    payload = {
        "short_name": args.short_name,
        "author_name": args.author_name,
        "author_url": args.author_url,
    }

    result = telegraph_call("createAccount", payload)
    print(json.dumps({"ok": True, "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except TelegraphError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
