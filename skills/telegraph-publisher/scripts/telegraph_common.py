#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request

API_BASE = "https://api.telegra.ph"


class TelegraphError(RuntimeError):
    pass


def get_access_token(cli_token: str | None = None) -> str:
    token = cli_token or os.environ.get("TELEGRAPH_ACCESS_TOKEN")
    if not token:
        raise TelegraphError("TELEGRAPH_ACCESS_TOKEN is not set (and --access-token not provided)")
    return token


def telegraph_call(method: str, payload: dict) -> dict:
    url = f"{API_BASE}/{method}"
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8")
    result = json.loads(raw)
    if not result.get("ok"):
        raise TelegraphError(result.get("error", "Unknown Telegraph API error"))
    return result["result"]


def _render_inline_segment(text: str) -> list:
    """
    Parse minimal inline markdown in a plain text segment.

    Supported in this parser:
    - **bold** / __bold__
    - *italic* / _italic_
    - ~~strikethrough~~
    - `inline code`
    """
    pattern = re.compile(
        r"(\*\*[^*]+\*\*|__[^_]+__|\*[^*]+\*|_[^_]+_|~~[^~]+~~|`[^`]+`)"
    )
    out: list = []
    i = 0

    for m in pattern.finditer(text):
        if m.start() > i:
            out.append(text[i:m.start()])

        token = m.group(0)
        if token.startswith("**") and token.endswith("**"):
            out.append({"tag": "strong", "children": [token[2:-2]]})
        elif token.startswith("__") and token.endswith("__"):
            out.append({"tag": "strong", "children": [token[2:-2]]})
        elif token.startswith("~~") and token.endswith("~~"):
            out.append({"tag": "s", "children": [token[2:-2]]})
        elif token.startswith("`") and token.endswith("`"):
            out.append({"tag": "code", "children": [token[1:-1]]})
        elif token.startswith("*") and token.endswith("*"):
            out.append({"tag": "em", "children": [token[1:-1]]})
        elif token.startswith("_") and token.endswith("_"):
            out.append({"tag": "em", "children": [token[1:-1]]})
        else:
            out.append(token)

        i = m.end()

    if i < len(text):
        out.append(text[i:])

    return out if out else [""]


def _inline_nodes(text: str) -> list:
    """Parse inline links and basic inline markdown."""
    out: list = []
    i = 0

    # [label](https://...) links
    link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")

    for m in link_pattern.finditer(text):
        if m.start() > i:
            out.extend(_render_inline_segment(text[i:m.start()]))

        label, href = m.group(1), m.group(2)
        out.append({"tag": "a", "attrs": {"href": href}, "children": _render_inline_segment(label)})
        i = m.end()

    if i < len(text):
        out.extend(_render_inline_segment(text[i:]))

    return out if out else [""]


def _heading_tag_from_level(level: int) -> str:
    """
    Telegra.ph supports only h3/h4.
    Map markdown heading levels to supported tags:
    - #, ## -> h3
    - ###, ####+ -> h4
    """
    return "h3" if level <= 2 else "h4"


def markdown_to_nodes(markdown: str) -> list:
    """
    Convert lightweight markdown into Telegraph Node format.

    Supported:
    - # / ## / ### / #### headings (mapped to h3/h4)
    - paragraphs
    - unordered lists (- item)
    - blockquotes (> quote)
    - fenced code blocks ```
    - inline links [text](url)
    - inline style tokens (**bold**, *italic*, `code`, ~~strike~~)
    """
    lines = markdown.splitlines()
    nodes: list = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code block
        if stripped.startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # consume closing ```
            code_text = "\n".join(code_lines)
            nodes.append({"tag": "pre", "children": [{"tag": "code", "children": [code_text]}]})
            continue

        # headings (# ... ####)
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            nodes.append({"tag": _heading_tag_from_level(level), "children": _inline_nodes(text)})
            i += 1
            continue

        # unordered list
        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                item_text = lines[i].strip()[2:].strip()
                items.append({"tag": "li", "children": _inline_nodes(item_text)})
                i += 1
            nodes.append({"tag": "ul", "children": items})
            continue

        # ordered list (e.g., 1. item)
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                item_text = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append({"tag": "li", "children": _inline_nodes(item_text)})
                i += 1
            nodes.append({"tag": "ol", "children": items})
            continue

        # blockquote
        if stripped.startswith(">"):
            quote_parts = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_parts.append(lines[i].strip().lstrip(">").strip())
                i += 1
            quote_text = " ".join([q for q in quote_parts if q])
            nodes.append({"tag": "blockquote", "children": _inline_nodes(quote_text)})
            continue

        # paragraph (merge until blank / block start)
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            look = lines[i].strip()
            if not look:
                break
            if look.startswith(("#", "- ", ">", "```")) or re.match(r"^\d+\.\s+", look):
                break
            para_lines.append(look)
            i += 1
        para = " ".join(para_lines)
        nodes.append({"tag": "p", "children": _inline_nodes(para)})

    return nodes


def nodes_payload_size(nodes: list) -> int:
    return len(json.dumps(nodes, ensure_ascii=False).encode("utf-8"))


def build_create_payload(
    access_token: str,
    title: str,
    content_nodes: list,
    author_name: str | None = None,
    author_url: str | None = None,
    return_content: bool = False,
) -> dict:
    payload = {
        "access_token": access_token,
        "title": title,
        "content": json.dumps(content_nodes, ensure_ascii=False),
        "return_content": "true" if return_content else "false",
    }
    if author_name:
        payload["author_name"] = author_name
    if author_url:
        payload["author_url"] = author_url
    return payload


def build_edit_payload(
    access_token: str,
    path: str,
    title: str,
    content_nodes: list,
    author_name: str | None = None,
    author_url: str | None = None,
    return_content: bool = False,
) -> dict:
    payload = {
        "access_token": access_token,
        "path": path,
        "title": title,
        "content": json.dumps(content_nodes, ensure_ascii=False),
        "return_content": "true" if return_content else "false",
    }
    if author_name:
        payload["author_name"] = author_name
    if author_url:
        payload["author_url"] = author_url
    return payload
