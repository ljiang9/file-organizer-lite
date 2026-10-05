import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from file_organizer_lite.rules import RuleEngine
from file_organizer_lite.planner import build_plan, apply_plan


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for f in ["photo.jpg","note.md","data.csv","song.mp3","archive.zip","script.py","unknown.xyz"]:
            (self.root / f).write_text("x")
        (self.root / ".hidden").write_text("x")
    def tearDown(self): self.tmp.cleanup()
    def test_classify_ext(self):
        eng = RuleEngine()
        self.assertEqual(eng.classify(self.root / "a.jpg"), "Images")
        self.assertEqual(eng.classify(self.root / "a.py"), "Code")
        self.assertIsNone(eng.classify(self.root / "a.xyz"))
    def test_plan_only_no_move(self):
        plan = build_plan(self.root)
        subdirs = [p for p in self.root.iterdir() if p.is_dir()]
        self.assertEqual(subdirs, [])
        self.assertIn("photo.jpg", [p.name for p in self.root.iterdir()])
        cats = {Path(e.dst).parent.name for e in plan}
        self.assertIn("Images", cats); self.assertIn("Code", cats); self.assertIn("Others", cats)
    def test_plan_skips_hidden(self):
        plan = build_plan(self.root)
        self.assertNotIn(".hidden", [Path(e.src).name for e in plan])
    def test_apply_moves_files(self):
        result = apply_plan(build_plan(self.root), dry_run=False)
        self.assertEqual(len(result["errors"]), 0)
        self.assertEqual(len(result["moved"]), 7)
        self.assertTrue((self.root / "Images" / "photo.jpg").exists())
        self.assertTrue((self.root / "Others" / "unknown.xyz").exists())
        self.assertFalse((self.root / "photo.jpg").exists())
    def test_apply_dry_run(self):
        apply_plan(build_plan(self.root), dry_run=True)
        self.assertTrue((self.root / "photo.jpg").exists())
    def test_apply_idempotent_skip(self):
        apply_plan(build_plan(self.root), dry_run=False)
        self.assertEqual(build_plan(self.root), [])


if __name__ == "__main__": unittest.main()
