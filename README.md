# file-organizer-lite

零依赖的文件归类 agent。按扩展名把目录顶层混杂文件规划到分类子目录。**默认只生成移动计划（dry-run），不会动你的任何文件；加 --apply 才真正执行。**

## 快速开始

```bash
python -m file_organizer_lite ~/Downloads
python -m file_organizer_lite ~/Downloads --apply
```

## 无 API Key 如何运行

纯本地规则引擎，不调用任何 LLM，不需要任何 API Key。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © ljiang9
