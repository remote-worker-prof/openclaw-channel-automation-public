#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from telegraph_common import (
    TelegraphError,
    build_edit_payload,
    get_access_token,
    markdown_to_nodes,
    nodes_payload_size,
    telegraph_call,
)


def main() -> int:
    p = argparse.ArgumentParser(description="Edit Telegra.ph page from markdown (safe by default)")
    p.add_argument("--path", required=True, help="Telegraph page path, e.g. My-Title-03-24")
    p.add_argument("--title", required=True, help="Updated page title")
    p.add_argument("--input", required=True, help="Path to markdown/text file")
    p.add_argument("--author-name", help="Author name (optional)")
    p.add_argument("--author-url", help="Author URL (optional)")
    p.add_argument("--access-token", help="Telegraph access token (optional if env set)")
    p.add_argument("--publish", action="store_true", help="Actually call Telegra.ph API. Without this flag = dry-run")
    p.add_argument("--return-content", action="store_true", help="Request content echo from API")
    args = p.parse_args()

    src = Path(args.input)
    if not src.exists():
        raise TelegraphError(f"Input file not found: {src}")

    markdown = src.read_text(encoding="utf-8")
    nodes = markdown_to_nodes(markdown)
    size = nodes_payload_size(nodes)

    preview = {
        "mode": "publish" if args.publish else "dry-run",
        "path": args.path,
        "title": args.title,
        "input": str(src),
        "nodes_count": len(nodes),
        "content_bytes": size,
        "content_limit_bytes": 64 * 1024,
        "within_limit": size <= 64 * 1024,
    }

    if size > 64 * 1024:
        raise TelegraphError(f"Content too large for Telegraph: {size} bytes > 65536 bytes")

    if not args.publish:
        print(json.dumps({"ok": True, "preview": preview}, ensure_ascii=False, indent=2))
        return 0

    token = get_access_token(args.access_token)
    payload = build_edit_payload(
        access_token=token,
        path=args.path,
        title=args.title,
        content_nodes=nodes,
        author_name=args.author_name,
        author_url=args.author_url,
        return_content=args.return_content,
    )
    result = telegraph_call("editPage", payload)

    print(json.dumps({"ok": True, "preview": preview, "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except TelegraphError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
