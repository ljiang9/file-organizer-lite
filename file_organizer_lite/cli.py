"""命令行：python -m file_organizer_lite <dir> [--apply]。默认 dry-run。"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from .planner import build_plan, apply_plan


def main(argv=None):
    ap = argparse.ArgumentParser(prog="file-organizer", description="文件归类 agent：默认只生成移动计划；加 --apply 才真正移动。")
    ap.add_argument("dir"); ap.add_argument("--apply", action="store_true"); ap.add_argument("--default", default="Others")
    args = ap.parse_args(argv)
    root = Path(args.dir)
    if not root.is_dir(): print(f"目录不存在: {root}", file=sys.stderr); return 2
    plan = build_plan(root, default_bucket=args.default)
    if not plan: print("（目录下没有需要整理的顶层文件）"); return 0
    print(f"=== 整理计划（共 {len(plan)} 个文件）===")
    by_cat = {}
    for e in plan: by_cat.setdefault(e.category, []).append(Path(e.src).name)
    for cat, names in sorted(by_cat.items()):
        print(f"\n[{cat}] -> {cat}/")
        for n in names: print(f"   {n}")
    if not args.apply:
        print("\n（dry-run：未移动任何文件。加 --apply 才真正执行。）"); return 0
    print("\n=== 执行移动 ===")
    result = apply_plan(plan, dry_run=False)
    print(f"已移动 {len(result['moved'])} 个；跳过 {len(result['skipped'])} 个；错误 {len(result['errors'])} 个。")
    return 0


if __name__ == "__main__": raise SystemExit(main())
