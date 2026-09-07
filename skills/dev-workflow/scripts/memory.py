#!/usr/bin/env python3
"""Project memory bank: CRUD over <dir>/memory.json.

Usage:
  python3 memory.py [--dir DIR] <command> [args]

Commands:
  init                       create an empty store
  get --keyword K            print every full entry matching K (key, cat, or text)
  get --key K                print one full entry by key
  add --key K --text T [--cat C]
  update --key K --text T [--cat C] [--append]
  remove --key K
  list [--cat C]

The store defaults to memory.json in the current directory. Each entry is
{"key", "text", "cat", "updated"}. Substring match on --keyword is
case-insensitive. get always prints the complete entry objects, never a
truncated form.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

STORE = "memory.json"
SCHEMA_VERSION = 1


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    data = {"version": SCHEMA_VERSION, "entries": {}}
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"memory.py: cannot read {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict) or not isinstance(data.get("entries"), dict):
        print(f"memory.py: {path} is not a memory store (missing entries).", file=sys.stderr)
        sys.exit(2)
    data.setdefault("version", SCHEMA_VERSION)
    return data


def save(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def store_path(args):
    return os.path.join(args.dir, STORE)


def require_key(args, parser):
    if not args.key:
        parser.error("--key is required")
    return args.key


def require_text(args, parser):
    if not args.text:
        parser.error("--text is required")
    return args.text


def print_store(path, data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def get_keyword(args, parser):
    if not args.keyword:
        parser.error("--keyword is required")
    data = load(store_path(args))
    needle = args.keyword.lower()
    hits = []
    for key, entry in data["entries"].items():
        text = entry.get("text", "")
        cat = entry.get("cat", "")
        if needle in key.lower() or needle in cat.lower() or needle in text.lower():
            hits.append({"key": key, **entry})
    print(json.dumps(hits, indent=2, ensure_ascii=False) if hits else "[]")


def get_key(args, parser):
    key = require_key(args, parser)
    data = load(store_path(args))
    entry = data["entries"].get(key)
    if entry is None:
        print(f"memory.py: no entry with key '{key}'.", file=sys.stderr)
        sys.exit(1)
    print(json.dumps({"key": key, **entry}, indent=2, ensure_ascii=False))


def add(args, parser):
    key = require_key(args, parser)
    require_text(args, parser)
    path = store_path(args)
    data = load(path)
    if key in data["entries"]:
        print(f"memory.py: key '{key}' already exists; use update.", file=sys.stderr)
        sys.exit(1)
    data["entries"][key] = {
        "text": args.text,
        "cat": args.cat or "",
        "updated": now_iso(),
    }
    data["version"] = SCHEMA_VERSION
    save(path, data)
    print(f"memory.py: added '{key}'.")


def update(args, parser):
    key = require_key(args, parser)
    require_text(args, parser)
    path = store_path(args)
    data = load(path)
    entry = data["entries"].get(key)
    if entry is None:
        print(f"memory.py: no entry with key '{key}'; use add.", file=sys.stderr)
        sys.exit(1)
    if args.append:
        entry["text"] = f"{entry.get('text', '')}\n{args.text}".strip()
    else:
        entry["text"] = args.text
    if args.cat is not None:
        entry["cat"] = args.cat
    entry["updated"] = now_iso()
    data["entries"][key] = entry
    save(path, data)
    print(f"memory.py: updated '{key}'.")


def remove(args, parser):
    key = require_key(args, parser)
    path = store_path(args)
    data = load(path)
    if key not in data["entries"]:
        print(f"memory.py: no entry with key '{key}'.", file=sys.stderr)
        sys.exit(1)
    del data["entries"][key]
    save(path, data)
    print(f"memory.py: removed '{key}'.")


def list_entries(args, parser):
    data = load(store_path(args))
    if not data["entries"]:
        return
    for key, entry in sorted(data["entries"].items()):
        if args.cat and args.cat.lower() not in entry.get("cat", "").lower():
            continue
        first = entry.get("text", "").splitlines()[0] if entry.get("text") else ""
        print(f"{key} [{entry.get('cat', '')}] {entry.get('updated', '')} :: {first}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="memory.py", description=__doc__)
    parser.add_argument("--dir", default=os.getcwd(), help="directory of memory.json (default: cwd)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create an empty store")

    p_get = sub.add_parser("get", help="fetch entries (full objects, never truncated)")
    g = p_get.add_mutually_exclusive_group(required=True)
    g.add_argument("--keyword", help="substring match on key, cat, or text")
    g.add_argument("--key", help="exact entry key")

    p_add = sub.add_parser("add", help="create an entry")
    p_add.add_argument("--key", required=True)
    p_add.add_argument("--text", required=True)
    p_add.add_argument("--cat", default="")

    p_upd = sub.add_parser("update", help="update an existing entry")
    p_upd.add_argument("--key", required=True)
    p_upd.add_argument("--text", required=True)
    p_upd.add_argument("--cat")
    p_upd.add_argument("--append", action="store_true", help="append text instead of replacing")

    p_rm = sub.add_parser("remove", help="delete an entry")
    p_rm.add_argument("--key", required=True)

    p_list = sub.add_parser("list", help="one-line summaries of entries")
    p_list.add_argument("--cat", default="")

    args = parser.parse_args(argv)
    if args.command == "init":
        save(store_path(args), {"version": SCHEMA_VERSION, "entries": {}})
        print(f"memory.py: initialized {store_path(args)}.")
    elif args.command == "get":
        if args.keyword is not None:
            get_keyword(args, parser)
        else:
            get_key(args, parser)
    elif args.command == "add":
        add(args, parser)
    elif args.command == "update":
        update(args, parser)
    elif args.command == "remove":
        remove(args, parser)
    elif args.command == "list":
        list_entries(args, parser)


if __name__ == "__main__":
    main()