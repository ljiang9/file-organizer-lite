"""分类规则与引擎。"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Rule:
    name: str; target: str
    exts: set = field(default_factory=set)
    patterns: list = field(default_factory=list)

DEFAULT_RULES = [
    Rule("图片", "Images", exts={".jpg",".jpeg",".png",".gif",".bmp",".webp",".svg",".heic"}),
    Rule("文档", "Documents", exts={".pdf",".doc",".docx",".txt",".md",".rtf",".odt"}),
    Rule("表格", "Spreadsheets", exts={".xls",".xlsx",".csv",".ods"}),
    Rule("演示", "Presentations", exts={".ppt",".pptx",".key"}),
    Rule("音频", "Audio", exts={".mp3",".wav",".flac",".aac",".ogg",".m4a"}),
    Rule("视频", "Videos", exts={".mp4",".mov",".mkv",".avi",".webm",".flv"}),
    Rule("压缩包", "Archives", exts={".zip",".rar",".7z",".tar",".gz",".bz2"}),
    Rule("代码", "Code", exts={".py",".js",".ts",".java",".c",".cpp",".go",".rs",".rb",".php",".html",".css",".json",".xml",".yml",".yaml"}),
    Rule("安装包", "Installers", exts={".dmg",".pkg",".exe",".msi",".deb",".rpm"}),
]

class RuleEngine:
    def __init__(self, rules=None): self.rules = rules or DEFAULT_RULES
    def classify(self, path):
        ext = path.suffix.lower()
        for r in self.rules:
            if ext and ext in r.exts: return r.target
        return None
