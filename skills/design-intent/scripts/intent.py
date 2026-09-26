#!/usr/bin/env python3
"""design-intent skill — mechanical support.

Subcommands:
  scan    Detect slop tells in source files + report design.yaml intent coverage.
  gates   Evaluate the four intent gates from design.yaml (exit 1 on fail).
  merge   Deep-merge an intent payload (JSON file) into design.yaml's `intent:` block.

No third-party dependencies. Only the `intent:` block is rewritten by `merge`;
the rest of design.yaml is preserved byte-for-byte.
"""
from __future__ import annotations

import utils.transport
import utils.session
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- slop rules

SLOP_RULES = [
    ("font-inter-lone", re.compile(r"font-family[^;\n}]*['\"]?Inter['\"]?[,;\n}]?", re.I),
     "Inter as the lone/leading family"),
    ("font-slop-family", re.compile(r"['\"](Geist|Space Grotesk|Instrument Serif)['\"]"),
     "Geist / Space Grotesk / Instrument Serif"),
    ("tailwind-slop-color", re.compile(r"\b(indigo|violet|purple)-(400|500|600|700)\b"),
     "Tailwind indigo/violet/purple accent"),
    ("gradient-hero", re.compile(r"linear-gradient\([^)]*\b(indigo|violet|purple|blue)\b", re.I),
     "purple/blue gradient"),
    ("glassmorphism", re.compile(r"backdrop-filter:\s*blur|backdrop-blur"),
     "glassmorphism (backdrop blur)"),
    ("bounce-default", re.compile(r"animate-bounce|animation[^;\n}]*\bbounce\b"),
     "bounce default animation"),
    ("fade-carpet", re.compile(r"initial=\{\{\s*opacity:\s*0\s*\}\}|initial:\s*\{\s*opacity:\s*0\s*\}"),
     "opacity-0 reveal default (fade carpet)"),
    ("lorem", re.compile(r"\blorem ipsum\b", re.I), "placeholder text"),
    ("buzzword", re.compile(r"\b(empower|unlock|seamless|cutting-edge|game-?changer|revolutionize|leverage)\b", re.I),
     "AI buzzword"),
    ("dev-cta", re.compile(r">\s*Learn [Mm]ore\s*<|['\"]Learn [Mm]ore['\"]|['\"]Get [Ss]tarted['\"]"),
     "generic dev-CTA fallback"),
    ("emoji-icon", re.compile(r"[\U0001F300-\U0001FAFF\u2700-\u27BF]"),
     "emoji as icon"),
]

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".venv", ".next", "out", ".obsidian", ".agents"}
SCAN_EXTS = {".html", ".css", ".scss", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".md"}


def find_files(root: Path, explicit: list[str] | None) -> list[Path]:
    if explicit:
        return [Path(p) for p in explicit if Path(p).is_file()]
    files: list[Path] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in SCAN_EXTS:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        files.append(p)
    return files[:400]


def scan_slop(files: list[Path], max_findings: int = 200) -> list[dict]:
    findings: list[dict] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if len(findings) >= max_findings:
                return findings
            for rule, rx, label in SLOP_RULES:
                m = rx.search(line)
                if m:
                    findings.append({"file": str(f), "line": lineno, "rule": rule,
                                     "label": label, "match": m.group(0)[:80]})
    return findings


# ---------------------------------------------------------------- yaml (minimal)

TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")


def load_yaml_blocks(text: str) -> dict[str, list[tuple[int, str, str]]]:
    """Return top-level key -> [(indent, key, raw_value)] lines of its block."""
    blocks: dict[str, list[tuple[int, str, str]]] = {}
    current: str | None = None
    for raw in text.splitlines():
        m = TOP_KEY.match(raw)
        if m and not raw.startswith((" ", "\t", "-", "#")):
            current = m.group(1)
            blocks.setdefault(current, [])
            continue
        if current and raw.strip() and not raw.lstrip().startswith("#"):
            indent = len(raw) - len(raw.lstrip(" "))
            kv = re.match(r"^([\w.-]+):\s*(.*)$", raw.strip())
            key, val = (kv.group(1), kv.group(2)) if kv else ("", raw.strip())
            blocks[current].append((indent, key, val))
    return blocks


def block_get(blocks, block, key):
    for indent, k, v in blocks.get(block, []):
        if k == key and indent <= 2:
            return v.strip()
    return None


def extract_intent_block(text: str) -> str | None:
    lines = text.splitlines(keepends=True)
    start = end = None
    for i, line in enumerate(lines):
        if line.strip() == "intent:":
            start = i
            for j in range(i + 1, len(lines)):
                if TOP_KEY.match(lines[j]) and not lines[j].startswith((" ", "\t", "-")):
                    end = j
                    break
            break
    if start is None:
        return None
    return "".join(lines[start + 1:(end or len(lines))])


def parse_intent(text: str) -> dict:
    """Recursively parse the intent: block (dicts, scalars, flow lists)."""
    block = extract_intent_block(text)
    return _parse_nested(block) if block else {}


def parse_design_yaml(text: str) -> dict:
    b = load_yaml_blocks(text)
    intent = parse_intent(text)
    style = intent.get("style", {}) if isinstance(intent.get("style"), dict) else {}
    motion = intent.get("motion", {}) if isinstance(intent.get("motion"), dict) else {}
    delivery = intent.get("delivery", {}) if isinstance(intent.get("delivery"), dict) else {}
    out = {
        "has_intent": "intent" in b,
        "has_tokens": "tokens" in b,
        "has_brand": "brand" in b,
        "audience": block_get(b, "project", "audience"),
        "intent_audience": intent.get("audience") if isinstance(intent.get("audience"), dict) else {},
        "style_direction": style.get("direction"),
        "style_rubric": style.get("rubric"),
        "motion_personality": motion.get("personality"),
        "motion_signature": motion.get("signature"),
        "delivery_results": delivery.get("results"),
        "a11y_aa_pass": block_get(b, "tokens", "a11y_aa_pass") or block_get(b, "status", "a11y_aa_pass"),
        "slop_scan_pass": block_get(b, "tokens", "slop_scan_pass") or block_get(b, "status", "slop_scan_pass"),
    }
    return out


# ---------------------------------------------------------------- merge

def emit(value, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            return pad + "{}\n"
        out = []
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                out.append(f"{pad}{k}:\n{emit(v, indent + 1)}")
            else:
                out.append(f"{pad}{k}: {emit_scalar(v)}\n")
        return "".join(out)
    if isinstance(value, list):
        if not value:
            return pad + "[]\n"
        return "".join(f"{pad}- {inline(v)}\n" for v in value)
    return pad + emit_scalar(value) + "\n"


def inline(v) -> str:
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return emit_scalar(v)


def emit_scalar(v) -> str:
    if v is None:
        return "~"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if re.search(r"[:{}\[\],&*?|>'\"%@`#]|^\s|\s$|^$|^(true|false|null|~|-?\d+(\.\d+)?)$", s):
        return json.dumps(s, ensure_ascii=False)
    return s


def merge_intent(design_path: Path, payload: dict) -> None:
    text = design_path.read_text(encoding="utf-8")
    existing: dict = {}
    lines = text.splitlines(keepends=True)
    start = end = None
    for i, line in enumerate(lines):
        if line.strip() == "intent:":
            start = i
            for j in range(i + 1, len(lines)):
                if TOP_KEY.match(lines[j]) and not lines[j].startswith((" ", "\t", "-")):
                    end = j
                    break
            break
    if start is not None:
        block_text = "".join(lines[start + 1:(end or len(lines))])
        existing = _parse_nested(block_text) or {}
    merged = _deep_merge(existing, payload.get("intent", payload))
    new_block = "intent:\n" + emit(merged, 1)
    if start is not None:
        lines[start:end or len(lines)] = [new_block]
    else:
        if lines and not text.endswith("\n"):
            lines.append("\n")
        lines.append(new_block)
    design_path.write_text("".join(lines), encoding="utf-8")


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _parse_nested(block: str) -> dict | None:
    """Tiny YAML subset parser for the intent block: nested dicts, scalars, block lists.

    An empty value ("key:") may resolve to a dict, a list, or null depending on the
    following line, so containers are created lazily via `pending`.
    """
    root: dict = {}
    stack: list[tuple[int, dict | list]] = [(-2, root)]
    pending: tuple[int, str, dict] | None = None  # (indent, key, parent)

    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        # Resolve a lazily-pending "key:" from the previous line.
        if pending is not None:
            pindent, pkey, pparent = pending
            pending = None
            if indent > pindent:
                if stripped.startswith("- "):
                    cont: dict | list = []
                else:
                    cont = {}
                pparent[pkey] = cont
                stack.append((pindent, cont))
            else:
                pparent[pkey] = None
                # fall through: current line is processed at its own level

        if stripped.startswith("- "):
            cont = stack[-1][1]
            if not isinstance(cont, list):
                return None
            cont.append(_scalar(stripped[2:].strip()))
            continue

        kv = re.match(r"^([\w.-]+):\s*(.*)$", stripped)
        if not kv:
            return None
        key, val = kv.group(1), kv.group(2).strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            return None
        parent = stack[-1][1]
        if not isinstance(parent, dict):
            return None
        if val == "":
            pending = (indent, key, parent)
        else:
            parent[key] = _scalar(val)

    if pending is not None:
        pindent, pkey, pparent = pending
        pparent[pkey] = None
    return root


def _scalar(s: str):
    if s.startswith(("[", "{")):
        try:
            return json.loads(s.replace("'", '"'))
        except json.JSONDecodeError:
            if s.startswith("{"):
                pairs = re.findall(r"([\w.-]+)\s*:\s*([^,{}]+)", s)
                if pairs:
                    return {k: _scalar(v.strip()) for k, v in pairs}
            return s
    if s in ("true", "false"):
        return s == "true"
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


# ---------------------------------------------------------------- commands

def cmd_scan(args) -> int:
    root = Path(args.root)
    files = find_files(root, args.files)
    findings = scan_slop(files)
    by_rule: dict[str, int] = {}
    for f in findings:
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1

    dy = root / (args.design_yaml or "design.yaml")
    intent = parse_design_yaml(dy.read_text(encoding="utf-8")) if dy.is_file() else {"has_intent": False}

    report = {
        "files_scanned": len(files),
        "slop_findings": len(findings),
        "slop_by_rule": dict(sorted(by_rule.items(), key=lambda kv: -kv[1])),
        "details": findings if args.verbose else findings[:40],
        "design_yaml": str(dy),
        "intent": intent,
        "verdict": (
            "CLEAN" if not by_rule else
            "MILD (2-3 rule families)" if len(by_rule) <= 3 else
            "HEAVY (4+ rule families)"
        ),
        "next": "run `gates` if intent present, else run CREATE Phase A (audience -> style -> motion)"
                if intent.get("has_intent") else
                "no intent block: run CREATE Phase A or REMEDIATE R1 (diagnose) first",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def cmd_gates(args) -> int:
    dy = Path(args.design_yaml)
    if not dy.is_file():
        print(f"FAIL: {dy} not found — intent gates cannot run without design.yaml", file=sys.stderr)
        return 1
    d = parse_design_yaml(dy.read_text(encoding="utf-8"))

    aud = d["intent_audience"]
    audience_ok = (
        d["has_intent"] and bool(aud.get("identity"))
        and bool(aud.get("say") or aud.get("never_say"))
        and bool(d["audience"])
    )

    direction = d["style_direction"] or ""
    style_ok = (
        bool(direction)
        and bool(d["style_rubric"])
        and not re.search(r"\b(clean|modern|minimal)\b", direction, re.I)
    )

    personality = str(d["motion_personality"] or "").strip().lower()
    motion_ok = personality in {"playful", "productive", "editorial", "technical"} and bool(d["motion_signature"])

    results = d["delivery_results"]
    if isinstance(results, str):
        delivery_ok = bool(results) and "fail" not in results.lower() and "pass" in results.lower()
    elif isinstance(results, dict):
        delivery_ok = bool(results) and all(str(v).lower() == "pass" for v in results.values())
    else:
        delivery_ok = False

    gates = {
        "audience": "pass" if audience_ok else "fail (write persona block: identity + say/never-say + project.audience; SKILL.md A1)",
        "style": "pass" if style_ok else f"fail ({'no direction or rubric recorded' if not direction else 'direction reads as default: ' + direction}; SKILL.md A2)",
        "motion": "pass" if motion_ok else f"fail ({'no motion personality' if not personality else 'personality set but no L3+ signature motion recorded'}; SKILL.md A3)",
        "delivery": "pass" if delivery_ok else "fail (intent.delivery.results not recorded as all-pass; SKILL.md A4)",
    }
    ok = all(v == "pass" for v in gates.values())
    print(json.dumps({"design_yaml": str(dy), "gates": gates, "overall": "PASS" if ok else "BLOCKED"},
                     indent=2, ensure_ascii=False))
    return 0 if ok else 1


def cmd_merge(args) -> int:
    payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
    dy = Path(args.design_yaml)
    if not dy.is_file():
        print(json.dumps({"error": f"{dy} not found", "hint": "run ui-ux-workflow initialize-design-system first"}))
        return 1
    merge_intent(dy, payload)
    print(json.dumps({"merged": str(dy), "intent_keys": sorted(payload.get("intent", payload).keys())}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="intent.py")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan")
    s.add_argument("--root", default=".")
    s.add_argument("--files", nargs="*", default=None)
    s.add_argument("--design-yaml", default=None)
    s.add_argument("--verbose", action="store_true")
    s.set_defaults(func=cmd_scan)

    g = sub.add_parser("gates")
    g.add_argument("--design-yaml", default="design.yaml")
    g.set_defaults(func=cmd_gates)

    m = sub.add_parser("merge")
    m.add_argument("--design-yaml", default="design.yaml")
    m.add_argument("--payload", required=True)
    m.set_defaults(func=cmd_merge)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
