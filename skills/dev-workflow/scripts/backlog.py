#!/usr/bin/env python3
"""Project backlog: CRUD over <dir>/project-backlog.json.

Usage:
  python3 backlog.py [--dir DIR] <command> [args]

Commands:
  init --name N [--description D]   create an empty backlog
  get --active          project meta + every full active task + last closed task
  get --task TASK-XX    one full task
  list [--status S]     one-line summaries (id | title | status)
  add --id TASK-XX --title T [--status S] [--deps A,B] [--notes N]
  update --id TASK-XX [--status S] [--title T] [--deps A,B] [--notes N]
  remove --id TASK-XX

Backlog file defaults to project-backlog.json in the current directory.
Status values: to-do, active, testing, blocked, closed (in_progress is
normalized to active). get always prints the complete task objects, never a
truncated or partial form. Every write appends to log.recent_changes.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

BACKLOG = "project-backlog.json"
VALID_STATUS = {"to-do", "active", "testing", "blocked", "closed"}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    if not os.path.exists(path):
        print(f"backlog.py: {path} not found. Run initialize-project first.", file=sys.stderr)
        sys.exit(2)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"backlog.py: cannot read {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
        print(f"backlog.py: {path} is not a backlog (missing tasks).", file=sys.stderr)
        sys.exit(2)
    data.setdefault("project", {})
    data.setdefault("log", {"last_updated": "", "recent_changes": []})
    return data


def save(path, data):
    data["log"]["last_updated"] = now_iso()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def log_change(data, entry):
    data["log"].setdefault("recent_changes", []).insert(0, entry)
    data["log"]["recent_changes"] = data["log"]["recent_changes"][:8]


def backlog_path(args):
    return os.path.join(args.dir, BACKLOG)


def init_backlog(args, parser):
    path = backlog_path(args)
    if os.path.exists(path):
        print(f"backlog.py: {path} already exists.", file=sys.stderr)
        sys.exit(1)
    data = {
        "project": {"name": args.name, "description": args.description or ""},
        "tasks": [],
        "log": {"last_updated": now_iso(), "recent_changes": []},
    }
    save(path, data)
    print(f"backlog.py: initialized {path}.")


def find_task(data, task_id):
    for task in data["tasks"]:
        if task["id"] == task_id:
            return task
    return None


def normalize_status(raw, parser=None):
    status = "to-do" if raw is None else raw.strip().lower()
    if status == "in_progress":
        status = "active"
    if status not in VALID_STATUS:
        print(f"backlog.py: invalid status '{raw}'. Use one of "
              f"{', '.join(sorted(VALID_STATUS))}.", file=sys.stderr)
        if parser:
            parser.error("invalid status")
        sys.exit(1)
    return status


def print_obj(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def get_active(args, parser):
    data = load(backlog_path(args))
    active = [t for t in data["tasks"] if t["status"] == "active"]
    closed = [t for t in data["tasks"] if t["status"] == "closed"]
    last_closed = closed[-1] if closed else None
    recent = data["log"].get("recent_changes", [])[:2]
    print_obj({
        "project": data["project"],
        "active": active,
        "last_closed": last_closed,
        "log": {"last_updated": data["log"].get("last_updated", ""), "recent_changes": recent},
    })


def get_task(args, parser):
    task = find_task(load(backlog_path(args)), args.task_id)
    if task is None:
        print(f"backlog.py: no task with id '{args.task_id}'.", file=sys.stderr)
        sys.exit(1)
    print_obj(task)


def list_tasks(args, parser):
    data = load(backlog_path(args))
    for task in data["tasks"]:
        if args.status and task["status"] != args.status:
            continue
        deps = ",".join(task.get("dependencies", [])) or "-"
        print(f"{task['id']} | {task['title']} | {task['status']} | deps {deps}")


def add(args, parser):
    status = normalize_status(args.status, parser)
    path = backlog_path(args)
    data = load(path)
    if find_task(data, args.task_id):
        print(f"backlog.py: task '{args.task_id}' already exists; use update.", file=sys.stderr)
        sys.exit(1)
    task = {
        "id": args.task_id,
        "title": args.title,
        "status": status,
        "dependencies": [d.strip() for d in (args.deps or "").split(",") if d.strip()],
        "notes": args.notes or "",
    }
    data["tasks"].append(task)
    log_change(data, {"action": "add", "task": args.task_id, "status": status, "at": now_iso()})
    save(path, data)
    print(f"backlog.py: added {args.task_id} ({status}).")


def update(args, parser):
    path = backlog_path(args)
    data = load(path)
    task = find_task(data, args.task_id)
    if task is None:
        print(f"backlog.py: no task with id '{args.task_id}'; use add.", file=sys.stderr)
        sys.exit(1)
    old_status = task["status"]
    if args.status is not None:
        task["status"] = normalize_status(args.status, parser)
    if args.title is not None:
        task["title"] = args.title
    if args.notes is not None:
        task["notes"] = args.notes
    if args.deps is not None:
        task["dependencies"] = [d.strip() for d in args.deps.split(",") if d.strip()]
    log_change(data, {"action": "update", "task": args.task_id,
                      "old_status": old_status, "new_status": task["status"], "at": now_iso()})
    save(path, data)
    print(f"backlog.py: updated {args.task_id} ({old_status} -> {task['status']}).")


def remove(args, parser):
    path = backlog_path(args)
    data = load(path)
    task = find_task(data, args.task_id)
    if task is None:
        print(f"backlog.py: no task with id '{args.task_id}'.", file=sys.stderr)
        sys.exit(1)
    data["tasks"] = [t for t in data["tasks"] if t["id"] != args.task_id]
    log_change(data, {"action": "remove", "task": args.task_id, "at": now_iso()})
    save(path, data)
    print(f"backlog.py: removed {args.task_id}.")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="backlog.py", description=__doc__)
    parser.add_argument("--dir", default=os.getcwd(), help="directory of project-backlog.json (default: cwd)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_active = sub.add_parser("get", help="fetch state (full objects, never truncated)")
    a = p_active.add_mutually_exclusive_group(required=True)
    a.add_argument("--active", action="store_true", help="project meta + active tasks + last closed")
    a.add_argument("--task", dest="task_id", help="exact task id")

    p_add = sub.add_parser("init", help="create an empty backlog")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--description", default="")

    p_list = sub.add_parser("list", help="one-line task summaries")
    p_list.add_argument("--status", help="filter by status")

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("--id", dest="task_id", required=True)
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--status", default="to-do")
    p_add.add_argument("--deps", default="")
    p_add.add_argument("--notes", default="")

    p_upd = sub.add_parser("update", help="update a task")
    p_upd.add_argument("--id", dest="task_id", required=True)
    p_upd.add_argument("--status")
    p_upd.add_argument("--title")
    p_upd.add_argument("--deps")
    p_upd.add_argument("--notes")

    p_rm = sub.add_parser("remove", help="delete a task")
    p_rm.add_argument("--id", dest="task_id", required=True)

    args = parser.parse_args(argv)
    if args.command == "init":
        init_backlog(args, parser)
    elif args.command == "get":
        (get_active if args.active else get_task)(args, parser)
    elif args.command == "list":
        list_tasks(args, parser)
    elif args.command == "add":
        add(args, parser)
    elif args.command == "update":
        update(args, parser)
    elif args.command == "remove":
        remove(args, parser)


if __name__ == "__main__":
    main()