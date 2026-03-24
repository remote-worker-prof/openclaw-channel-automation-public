#!/usr/bin/env python3
"""Check Telegram + Maton setup health (safe, non-destructive)."""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path


def load_secret_from_bashrc(var_name: str) -> str | None:
    """Fallback: parse `export VAR=...` from ~/.bashrc for non-interactive shells."""
    bashrc = Path.home() / ".bashrc"
    if not bashrc.exists():
        return None
    text = bashrc.read_text(encoding="utf-8", errors="ignore")
    m = re.search(rf"^\s*export\s+{re.escape(var_name)}\s*=\s*['\"]([^'\"]+)['\"]\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


def get_secret(var_name: str) -> str | None:
    return os.environ.get(var_name) or load_secret_from_bashrc(var_name)


def req_json(url: str, api_key: str, method: str = "GET", payload: dict | None = None, headers: dict | None = None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {api_key}")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    api_key = get_secret("MATON_API_KEY")
    if not api_key:
        print(json.dumps({"ok": False, "error": "MATON_API_KEY is not set (env or ~/.bashrc export)"}, ensure_ascii=False, indent=2))
        return

    bot_token = get_secret("TELEGRAM_BOT_TOKEN")

    out: dict = {"ok": True}

    # 1) Control-plane connection check
    connections = req_json("https://ctrl.maton.ai/connections?app=telegram&status=ACTIVE", api_key)
    out["connections"] = connections

    # 2) Preferred probe route: explicit bot token
    if bot_token:
        enc = urllib.parse.quote(bot_token, safe="")
        getme_url = f"https://gateway.maton.ai/telegram/bot{enc}/getMe"
        getchat_url = f"https://gateway.maton.ai/telegram/bot{enc}/getChat"
        out["route"] = "bot-token"
        out["getMe"] = req_json(getme_url, api_key)
        out["channel"] = req_json(getchat_url, api_key, method="POST", payload={"chat_id": "@algorithmic_planetoid"})
    else:
        # Legacy fallback (documented in skill, may fail depending on gateway behavior)
        out["route"] = "connection-substitution"
        try:
            out["getMe"] = req_json("https://gateway.maton.ai/telegram/:token/getMe", api_key)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            out["getMe_error"] = {"code": e.code, "body": body}

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
