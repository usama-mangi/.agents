#!/usr/bin/env python3
"""Knowledge graph store: CRUD over <dir>/memory-graph.json.

Native memory management for the memory-skill. Mirrors the mechanism used by
dev-workflow's memory.py: a single JSON document on disk, atomic writes,
schema versioning, and keyword-scoped reads (never dumps the whole store).

Usage:
  python3 graph.py [--dir DIR] <command> [args]

Commands:
  init                         create an empty store
  get --keyword K              print every full entity matching K
                               (entity name, entityType, observation text,
                               or relation type) plus that entity's relations
  get --entity E               print one full entity by exact name, plus all
                               of its relations (outgoing and incoming)
  add --entity E --type T --text N
                               create an entity with one observation
                               [--source S] [--confidence C]
                               [--valid-from F] [--valid-until U]
  update --entity E --text N [--append]
                               append N as a new observation (with enrichment)
                               (without --append replace all observations)
  relate --from F --to T --type R
                               add a relation F -(R)-> T
  remove --entity E            delete an entity and all its relations
  remove-relation --from F --to T --type R
                               delete one relation
  traverse --entity E [--depth N]
                               follow relations N hops from E
  check --entity E             surface contradictions involving E
  suggest --entity E           recommend links to existing entities
  synthesize --entity E        produce a narrative summary of E's neighborhood
  stale [--days N]             surface observations older than N days
  list [--type T]               one-line summaries (entity + count)

The store defaults to memory-graph.json in the skill directory. Each entity is
{"entityType", "observations": [{text, source, confidence, valid_from, valid_until, updated}], updated}.
Relations are [{"from", "to", "type", updated}]. Substring match on --keyword
is case-insensitive. get always prints the complete objects, never truncated.
"""

import argparse
import json
import os
import re
import sys
from collections import deque
from datetime import datetime, timezone

STORE = "memory-graph.json"
SCHEMA_VERSION = 1
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VALID_CONFIDENCE = {"high", "medium", "low"}
CONTRADICTION_MARKERS = {
    "myth", "debunk", "false", "contradict", "wrong", "incorrect",
    "fake", "untrue", "disproven", "lie", "lies", "fabricated",
    "misleading", "bunk", "hogwash", "nonsense",
}
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "this", "that",
    "these", "those", "it", "its", "not", "no", "nor", "so", "if", "then",
    "than", "too", "very", "just", "about", "up", "out", "all", "any",
    "each", "every", "both", "few", "more", "most", "other", "some",
    "such", "only", "own", "same", "also", "into", "over", "after",
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    data = {"version": SCHEMA_VERSION, "entities": {}, "relations": [], "log": {}}
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"graph.py: cannot read {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    if (not isinstance(data, dict)
            or not isinstance(data.get("entities"), dict)
            or not isinstance(data.get("relations"), list)):
        print(f"graph.py: {path} is not a graph store (missing entities/relations).",
              file=sys.stderr)
        sys.exit(2)
    data.setdefault("version", SCHEMA_VERSION)
    data.setdefault("entities", {})
    data.setdefault("relations", [])
    data.setdefault("log", {"last_updated": now_iso(), "recent_changes": []})
    return data


def save(path, data):
    data.setdefault("log", {"last_updated": now_iso(), "recent_changes": []})
    data["log"]["last_updated"] = now_iso()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def store_path(args):
    return os.path.join(args.dir, STORE)


def log_change(data, entry):
    data["log"].setdefault("recent_changes", []).insert(0, entry)
    data["log"]["recent_changes"] = data["log"]["recent_changes"][:8]


def require_entity(args, parser):
    if not args.entity:
        parser.error("--entity is required")
    return args.entity


def require_text(args, parser):
    if not args.text:
        parser.error("--text is required")
    return args.text


def require_confidence(args, parser):
    if args.confidence and args.confidence not in VALID_CONFIDENCE:
        parser.error(f"--confidence must be one of {sorted(VALID_CONFIDENCE)}")


def print_obj(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def rel_key(rel):
    return (rel.get("from"), rel.get("type"), rel.get("to"))


def tokens(text):
    return set(re.findall(r"[a-zA-Z]{3,}", text.lower()))


def make_observation(text, args):
    obs = {"text": text, "updated": now_iso()}
    if getattr(args, "source", None):
        obs["source"] = args.source
    if getattr(args, "confidence", None):
        obs["confidence"] = args.confidence
    if getattr(args, "valid_from", None):
        obs["valid_from"] = args.valid_from
    if getattr(args, "valid_until", None):
        obs["valid_until"] = args.valid_until
    return obs


def relations_for(data, name):
    out = []
    for r in data["relations"]:
        if r.get("from") == name or r.get("to") == name:
            out.append(r)
    return out


def get_keyword(args, parser):
    if not args.keyword:
        parser.error("--keyword is required")
    data = load(store_path(args))
    needle = args.keyword.lower()
    hits = []
    for name, entity in data["entities"].items():
        text = entity.get("entityType", "")
        for obs in entity.get("observations", []):
            text = f"{text} {obs.get('text', '')}"
        if (needle in name.lower()
                or needle in entity.get("entityType", "").lower()
                or needle in text.lower()):
            rels = relations_for(data, name)
            hits.append({"entity": name, **entity, "relations": rels})
    rel_hits = [r for r in data["relations"]
                if needle in r.get("type", "").lower()]
    print(json.dumps({"entities": hits, "relations": rel_hits},
                     indent=2, ensure_ascii=False) if hits or rel_hits else "[]")


def get_entity(args, parser):
    name = require_entity(args, parser)
    data = load(store_path(args))
    entity = data["entities"].get(name)
    if entity is None:
        print(f"graph.py: no entity '{name}'.", file=sys.stderr)
        sys.exit(1)
    rels = relations_for(data, name)
    print_obj({"entity": name, **entity, "relations": rels})


def add_entity(args, parser):
    name = require_entity(args, parser)
    if not args.type:
        parser.error("--type is required")
    require_text(args, parser)
    require_confidence(args, parser)
    path = store_path(args)
    data = load(path)
    if name in data["entities"]:
        print(f"graph.py: entity '{name}' already exists; use update.",
              file=sys.stderr)
        sys.exit(1)
    data["entities"][name] = {
        "entityType": args.type,
        "observations": [make_observation(args.text, args)],
        "updated": now_iso(),
    }
    log_change(data, {"action": "add", "entity": name, "type": args.type, "at": now_iso()})
    save(path, data)
    print(f"graph.py: added entity '{name}'.")


def update_observation(args, parser):
    name = require_entity(args, parser)
    require_text(args, parser)
    require_confidence(args, parser)
    path = store_path(args)
    data = load(path)
    entity = data["entities"].get(name)
    if entity is None:
        print(f"graph.py: no entity '{name}'; use add.", file=sys.stderr)
        sys.exit(1)
    obs = make_observation(args.text, args)
    if args.append:
        entity["observations"].append(obs)
    else:
        entity["observations"] = [obs]
    entity["updated"] = now_iso()
    log_change(data, {"action": "update", "entity": name, "append": args.append, "at": now_iso()})
    save(path, data)
    print(f"graph.py: updated '{name}'.")


def relate(args, parser):
    if args.from_entity == args.to_entity:
        parser.error("--from and --to must differ")
    if not args.from_entity or not args.to_entity:
        parser.error("--from and --to are required")
    if not args.type:
        parser.error("--type is required")
    path = store_path(args)
    data = load(path)
    for r in data["relations"]:
        if rel_key(r) == (args.from_entity, args.type, args.to_entity):
            print(f"graph.py: relation '{args.from_entity}' -{args.type}-> '{args.to_entity}' already exists.",
                  file=sys.stderr)
            sys.exit(1)
    data["relations"].append({
        "from": args.from_entity,
        "to": args.to_entity,
        "type": args.type,
        "updated": now_iso(),
    })
    log_change(data, {"action": "relate", "from": args.from_entity,
                      "to": args.to_entity, "type": args.type, "at": now_iso()})
    save(path, data)
    print(f"graph.py: related '{args.from_entity}' -{args.type}-> '{args.to_entity}'.")


def remove_entity(args, parser):
    name = require_entity(args, parser)
    path = store_path(args)
    data = load(path)
    if name not in data["entities"]:
        print(f"graph.py: no entity '{name}'.", file=sys.stderr)
        sys.exit(1)
    del data["entities"][name]
    data["relations"] = [r for r in data["relations"]
                         if r.get("from") != name and r.get("to") != name]
    log_change(data, {"action": "remove", "entity": name, "at": now_iso()})
    save(path, data)
    print(f"graph.py: removed entity '{name}' and its relations.")


def remove_relation(args, parser):
    if args.from_entity == args.to_entity:
        parser.error("--from and --to must differ")
    if not args.from_entity or not args.to_entity:
        parser.error("--from and --to are required")
    if not args.type:
        parser.error("--type is required")
    path = store_path(args)
    data = load(path)
    target = (args.from_entity, args.type, args.to_entity)
    before = len(data["relations"])
    data["relations"] = [r for r in data["relations"] if rel_key(r) != target]
    if len(data["relations"]) == before:
        print(f"graph.py: no relation '{args.from_entity}' -{args.type}-> '{args.to_entity}'.",
              file=sys.stderr)
        sys.exit(1)
    log_change(data, {"action": "remove-relation", "from": args.from_entity,
                      "to": args.to_entity, "type": args.type, "at": now_iso()})
    save(path, data)
    print(f"graph.py: removed relation '{args.from_entity}' -{args.type}-> '{args.to_entity}'.")


def list_entries(args, parser):
    data = load(store_path(args))
    if not data["entities"]:
        return
    total_rels = {}
    for r in data["relations"]:
        total_rels[r.get("from")] = total_rels.get(r.get("from"), 0) + 1
        total_rels[r.get("to")] = total_rels.get(r.get("to"), 0) + 1
    for name, entity in sorted(data["entities"].items()):
        e_type = entity.get("entityType", "")
        if args.type and args.type.lower() not in e_type.lower():
            continue
        n_obs = len(entity.get("observations", []))
        n_rel = total_rels.get(name, 0)
        print(f"{name} [{e_type}] :: {n_obs} obs, {n_rel} rels")


def traverse(args, parser):
    name = require_entity(args, parser)
    depth = args.depth if args.depth is not None else 1
    data = load(store_path(args))
    if name not in data["entities"]:
        print(f"graph.py: no entity '{name}'.", file=sys.stderr)
        sys.exit(1)
    if depth < 0:
        parser.error("--depth must be >= 0")
    visited = {name}
    neighborhood = [{"entity": name, "via": None, "from": None, "depth": 0}]
    queue = deque([(name, 0)])
    while queue:
        current, d = queue.popleft()
        if d >= depth:
            continue
        for r in data["relations"]:
            neighbor = None
            if r.get("from") == current and r.get("to") not in visited:
                neighbor = r.get("to")
            elif r.get("to") == current and r.get("from") not in visited:
                neighbor = r.get("from")
            if neighbor:
                visited.add(neighbor)
                neighborhood.append({
                    "entity": neighbor,
                    "via": r.get("type"),
                    "from": current,
                    "depth": d + 1,
                })
                queue.append((neighbor, d + 1))
    print_obj({"entity": name, "depth": depth, "neighborhood": neighborhood})


def find_contradictions(data, entity_name):
    entity = data["entities"].get(entity_name)
    if not entity:
        return []
    e_type = entity.get("entityType", "").lower()
    e_obs = entity.get("observations", [])
    contradictions = []
    for other_name, other_entity in data["entities"].items():
        if other_name == entity_name:
            continue
        if other_entity.get("entityType", "").lower() != e_type:
            continue
        for o_obs in other_entity.get("observations", []):
            for e_o in e_obs:
                e_tok = tokens(e_o["text"])
                o_tok = tokens(o_obs["text"])
                shared = e_tok & o_tok
                if shared and any(m in o_obs["text"].lower() for m in CONTRADICTION_MARKERS):
                    contradictions.append({
                        "entity": entity_name,
                        "observation": e_o["text"],
                        "contradicts": other_name,
                        "contradicting_observation": o_obs["text"],
                    })
    return contradictions


def check(args, parser):
    name = require_entity(args, parser)
    data = load(store_path(args))
    if name not in data["entities"]:
        print(f"graph.py: no entity '{name}'.", file=sys.stderr)
        sys.exit(1)
    contradictions = find_contradictions(data, name)
    print_obj({"entity": name, "contradictions": contradictions})


def suggest(args, parser):
    name = require_entity(args, parser)
    data = load(store_path(args))
    if name not in data["entities"]:
        print(f"graph.py: no entity '{name}'.", file=sys.stderr)
        sys.exit(1)
    entity = data["entities"][name]
    existing_targets = set()
    for r in data["relations"]:
        if r.get("from") == name:
            existing_targets.add(r.get("to"))
        elif r.get("to") == name:
            existing_targets.add(r.get("from"))
    suggestions = []
    e_type = entity.get("entityType", "").lower()
    e_tokens = tokens(entity.get("entityType", "") + " " + " ".join(
        o["text"] for o in entity.get("observations", [])))
    for other_name, other_entity in data["entities"].items():
        if other_name == name or other_name in existing_targets:
            continue
        o_type = other_entity.get("entityType", "").lower()
        o_tokens = tokens(other_entity.get("entityType", "") + " " + " ".join(
            o["text"] for o in other_entity.get("observations", [])))
        shared = e_tokens & o_tokens
        if e_type == o_type or len(shared) >= 2:
            reason_parts = []
            if e_type == o_type:
                reason_parts.append(f"same type: {e_type}")
            if shared:
                reason_parts.append(f"shared keywords: {', '.join(sorted(shared)[:3])}")
            suggestions.append({"to": other_name, "reason": " & ".join(reason_parts)})
    print_obj({"entity": name, "suggestions": suggestions})


def synthesize(args, parser):
    name = require_entity(args, parser)
    data = load(store_path(args))
    if name not in data["entities"]:
        print(f"graph.py: no entity '{name}'.", file=sys.stderr)
        sys.exit(1)
    entity = data["entities"][name]
    rels = relations_for(data, name)
    parts = []
    parts.append(f"{name} ({entity['entityType']}).")
    for obs in entity.get("observations", []):
        parts.append(obs["text"])
    for r in rels:
        other = r.get("to") if r.get("from") == name else r.get("from")
        if other and other in data["entities"]:
            other_obs = data["entities"][other].get("observations", [])
            if other_obs:
                parts.append(f"{name} {r['type']} {other}: {other_obs[0]['text']}")
    summary = " ".join(parts)
    print_obj({"entity": name, "summary": summary})


def stale(args, parser):
    days = args.days if args.days is not None else 90
    data = load(store_path(args))
    cutoff = datetime.now(timezone.utc).timestamp() - (days * 86400)
    stale_obs = []
    for entity_name, entity in data["entities"].items():
        for obs in entity.get("observations", []):
            updated = None
            try:
                updated = datetime.fromisoformat(obs["updated"]).timestamp()
            except (ValueError, TypeError):
                pass
            if updated and updated < cutoff:
                stale_obs.append({
                    "entity": entity_name,
                    "observation": obs["text"],
                    "days_old": days,
                    "updated": obs["updated"],
                })
    print_obj({"days": days, "stale": stale_obs})


def main(argv=None):
    parser = argparse.ArgumentParser(prog="graph.py", description=__doc__)
    parser.add_argument("--dir", default=SKILL_DIR,
                        help="directory of memory-graph.json (default: skill dir)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create an empty store")

    p_get = sub.add_parser("get", help="fetch entities (full objects, never truncated)")
    g = p_get.add_mutually_exclusive_group(required=True)
    g.add_argument("--keyword", help="substring match on entity name, type, or text")
    g.add_argument("--entity", help="exact entity name")

    p_add = sub.add_parser("add", help="create an entity with one observation")
    p_add.add_argument("--entity", required=True)
    p_add.add_argument("--type", required=True)
    p_add.add_argument("--text", required=True)
    p_add.add_argument("--source", default=None, help="provenance source URL or file")
    p_add.add_argument("--confidence", default=None, choices=sorted(VALID_CONFIDENCE),
                       help="high, medium, or low")
    p_add.add_argument("--valid-from", default=None, help="ISO date observation becomes valid")
    p_add.add_argument("--valid-until", default=None, help="ISO date observation expires")

    p_upd = sub.add_parser("update", help="update an entity's observations")
    p_upd.add_argument("--entity", required=True)
    p_upd.add_argument("--text", required=True)
    p_upd.add_argument("--append", action="store_true", help="append as a new observation")
    p_upd.add_argument("--source", default=None, help="provenance source URL or file")
    p_upd.add_argument("--confidence", default=None, choices=sorted(VALID_CONFIDENCE),
                       help="high, medium, or low")
    p_upd.add_argument("--valid-from", default=None, help="ISO date observation becomes valid")
    p_upd.add_argument("--valid-until", default=None, help="ISO date observation expires")

    p_rel = sub.add_parser("relate", help="add a relation between entities")
    p_rel.add_argument("--from", dest="from_entity", required=True)
    p_rel.add_argument("--to", dest="to_entity", required=True)
    p_rel.add_argument("--type", required=True)

    p_rm = sub.add_parser("remove", help="delete an entity and its relations")
    p_rm.add_argument("--entity", required=True)

    p_rmr = sub.add_parser("remove-relation", help="delete one relation")
    p_rmr.add_argument("--from", dest="from_entity", required=True)
    p_rmr.add_argument("--to", dest="to_entity", required=True)
    p_rmr.add_argument("--type", required=True)

    p_trv = sub.add_parser("traverse", help="follow relations N hops from an entity")
    p_trv.add_argument("--entity", required=True)
    p_trv.add_argument("--depth", type=int, default=1)

    p_chk = sub.add_parser("check", help="surface contradictions involving an entity")
    p_chk.add_argument("--entity", required=True)

    p_sug = sub.add_parser("suggest", help="recommend links to existing entities")
    p_sug.add_argument("--entity", required=True)

    p_syn = sub.add_parser("synthesize", help="produce a narrative summary of an entity's neighborhood")
    p_syn.add_argument("--entity", required=True)

    p_stl = sub.add_parser("stale", help="surface observations older than N days")
    p_stl.add_argument("--days", type=int, default=90)

    p_list = sub.add_parser("list", help="one-line entity summaries")
    p_list.add_argument("--type", default="")

    args = parser.parse_args(argv)
    if args.command == "init":
        path = store_path(args)
        save(path, {"version": SCHEMA_VERSION, "entities": {}, "relations": [],
                    "log": {"last_updated": now_iso(), "recent_changes": []}})
        print(f"graph.py: initialized {path}.")
    elif args.command == "get":
        if args.keyword is not None:
            get_keyword(args, parser)
        else:
            get_entity(args, parser)
    elif args.command == "add":
        add_entity(args, parser)
    elif args.command == "update":
        update_observation(args, parser)
    elif args.command == "relate":
        relate(args, parser)
    elif args.command == "remove":
        remove_entity(args, parser)
    elif args.command == "remove-relation":
        remove_relation(args, parser)
    elif args.command == "traverse":
        traverse(args, parser)
    elif args.command == "check":
        check(args, parser)
    elif args.command == "suggest":
        suggest(args, parser)
    elif args.command == "synthesize":
        synthesize(args, parser)
    elif args.command == "stale":
        stale(args, parser)
    elif args.command == "list":
        list_entries(args, parser)


if __name__ == "__main__":
    main()
