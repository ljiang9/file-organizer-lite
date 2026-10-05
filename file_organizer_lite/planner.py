"""规划与执行：build_plan 只读；apply_plan 才真正移动。"""
from __future__ import annotations
import shutil
from dataclasses import dataclass
from pathlib import Path
from .rules import RuleEngine


@dataclass
class PlanEntry:
    src: str; dst: str; category: str


def build_plan(root, engine=None, default_bucket="Others"):
    engine = engine or RuleEngine()
    root = Path(root).resolve()
    plan = []
    for p in root.iterdir():
        if not p.is_file() or p.name.startswith("."): continue
        cat = engine.classify(p) or default_bucket
        plan.append(PlanEntry(src=str(p), dst=str(root / cat / p.name), category=cat))
    return plan


def apply_plan(plan, dry_run=False):
    moved, skipped, errors = [], [], []
    for e in plan:
        src, dst = Path(e.src), Path(e.dst)
        if not src.exists(): skipped.append((e.src, "源不存在")); continue
        if dst.exists(): skipped.append((e.src, f"目标已存在: {dst.name}")); continue
        if dry_run: moved.append((e.src, e.dst)); continue
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst)); moved.append((e.src, e.dst))
        except OSError as ex: errors.append((e.src, str(ex)))
    return {"moved": moved, "skipped": skipped, "errors": errors}
