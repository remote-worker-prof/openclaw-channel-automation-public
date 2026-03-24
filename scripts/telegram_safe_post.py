#!/usr/bin/env python3
"""
Safe Telegram publisher via Maton gateway.

Default behavior is DRY RUN to prevent accidental posting.
Only create-new-message flow (sendMessage) is supported.

Routing modes:
1) Preferred: explicit TELEGRAM_BOT_TOKEN (gateway path: /telegram/bot<TOKEN>/<method>)
2) Fallback: legacy connection substitution (/telegram/:token/<method>)

Formatting policy:
- Markdown/MarkdownV2 are intentionally disabled in this script to avoid escaping artifacts.
- Use HTML mode by default for readable rich formatting.
- Keep plain mode as fallback.
- Markdown/MarkdownV2 remain disabled.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def fail(msg: str, code: int = 1):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(code)


def load_secret_from_bashrc(var_name: str) -> str | None:
    bashrc = Path.home() / ".bashrc"
    if not bashrc.exists():
        return None
    text = bashrc.read_text(encoding="utf-8", errors="ignore")
    m = re.search(rf"^\s*export\s+{re.escape(var_name)}\s*=\s*['\"]([^'\"]+)['\"]\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


def get_secret(var_name: str) -> str | None:
    return os.environ.get(var_name) or load_secret_from_bashrc(var_name)


def build_url(method: str, bot_token: str | None) -> str:
    if bot_token:
        enc = urllib.parse.quote(bot_token, safe="")
        return f"https://gateway.maton.ai/telegram/bot{enc}/{method}"
    return f"https://gateway.maton.ai/telegram/:token/{method}"


def call_send_message(
    api_key: str,
    chat_id: str,
    text: str,
    format_mode: str,
    connection_id: str | None,
    bot_token: str | None,
):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": False,
    }

    # Explicitly avoid Markdown modes (artifact-prone in bot pipelines)
    if format_mode == "html":
        payload["parse_mode"] = "HTML"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(build_url("sendMessage", bot_token), data=data, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    if connection_id:
        req.add_header("Maton-Connection", connection_id)

    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def main():
    p = argparse.ArgumentParser(description="Safe Telegram post publisher (default dry-run)")
    p.add_argument("--chat", default="@algorithmic_planetoid", help="Target chat id or @username")
    p.add_argument("--text", help="Post text")
    p.add_argument("--text-file", help="Path to text file with post content")
    p.add_argument(
        "--format",
        default="html",
        choices=["plain", "html"],
        help="Formatting mode: html (default) or plain",
    )
    p.add_argument("--connection-id", help="Optional Maton connection id")
    p.add_argument("--bot-token", help="Optional Telegram bot token (preferred routing)")
    p.add_argument("--publish", action="store_true", help="Actually publish. Without this flag: dry-run only")

    args = p.parse_args()

    api_key = get_secret("MATON_API_KEY")
    if not api_key:
        fail("MATON_API_KEY is not set")

    bot_token = args.bot_token or get_secret("TELEGRAM_BOT_TOKEN")

    if bool(args.text) == bool(args.text_file):
        fail("Provide exactly one of --text or --text-file")

    text = args.text
    if args.text_file:
        try:
            with open(args.text_file, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            fail(f"Cannot read --text-file: {e}")

    text = (text or "").strip()
    if not text:
        fail("Post text is empty")

    if len(text) > 4096:
        fail(f"Post too long: {len(text)} chars (Telegram limit 4096)")

    preview = {
        "mode": "dry-run" if not args.publish else "publish",
        "chat": args.chat,
        "format": args.format,
        "parse_mode": "HTML" if args.format == "html" else None,
        "length": len(text),
        "route": "bot-token" if bot_token else "connection-substitution",
        "text": text,
    }
    print(json.dumps({"ok": True, "preview": preview}, ensure_ascii=False, indent=2))

    if not args.publish:
        return

    try:
        result = call_send_message(
            api_key=api_key,
            chat_id=args.chat,
            text=text,
            format_mode=args.format,
            connection_id=args.connection_id,
            bot_token=bot_token,
        )
    except Exception as e:
        fail(f"Publish failed: {e}")

    print(json.dumps({"ok": True, "result": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
