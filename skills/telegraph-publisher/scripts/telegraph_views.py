#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from telegraph_common import TelegraphError, telegraph_call


def main() -> int:
    p = argparse.ArgumentParser(description="Get Telegra.ph views")
    p.add_argument("--path", required=True, help="Telegraph page path, e.g. My-Title-03-24")
    p.add_argument("--year", type=int)
    p.add_argument("--month", type=int)
    p.add_argument("--day", type=int)
    p.add_argument("--hour", type=int)
    args = p.parse_args()

    payload = {"path": args.path}
    if args.year is not None:
        payload["year"] = str(args.year)
    if args.month is not None:
        payload["month"] = str(args.month)
    if args.day is not None:
        payload["day"] = str(args.day)
    if args.hour is not None:
        payload["hour"] = str(args.hour)

    result = telegraph_call("getViews", payload)
    print(json.dumps({"ok": True, "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except TelegraphError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
