import json
from pathlib import Path
import tempfile
import unittest

from build_pack_index import build_index


class PackIndexTests(unittest.TestCase):
    def test_native_wrapped_natural_order_and_index_exclusion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pack = {"title": "Test pack", "questions": [{"id": "q1"}]}
            (root / "pack-2.json").write_text(json.dumps(pack), encoding="utf-8")
            (root / "pack-10.json").write_text(json.dumps({"pack": pack}), encoding="utf-8")
            (root / "index.json").write_text("not a pack", encoding="utf-8")
            result = build_index(root)
            self.assertEqual(["pack-10.json", "pack-2.json"], [p["file"] for p in result["packs"]])
            self.assertEqual(1, result["packs"][0]["questions"])
            self.assertNotIn("answers", json.dumps(result))

    def test_invalid_pack_is_not_silently_omitted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for bad in [[], {}, {"title": "No questions"}, {"title": "Empty", "questions": []}]:
                with self.subTest(pack=bad):
                    (root / "bad.json").write_text(json.dumps(bad), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "bad.json"):
                        build_index(root)

    def test_empty_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual({"version": 1, "packs": []}, build_index(Path(temp)))


if __name__ == "__main__":
    unittest.main()
