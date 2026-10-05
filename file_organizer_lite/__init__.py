"""file_organizer_lite: 文件归类 agent。默认只生成移动计划，--apply 才执行。"""
from .rules import Rule, RuleEngine, DEFAULT_RULES
from .planner import build_plan, apply_plan

__all__ = ["Rule", "RuleEngine", "DEFAULT_RULES", "build_plan", "apply_plan"]
__version__ = "0.1.0"
