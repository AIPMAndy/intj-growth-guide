import unittest, json, re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((R/"data/catalog.json").read_text(encoding="utf-8"))
    def test_count(self):
        self.assertEqual(len(self.data),41)
        self.assertEqual({x["kind"]:sum(i["kind"]==x["kind"] for i in self.data) for x in self.data},{"series":10,"film":12,"book":15,"doc":4})
    def test_unique_ids(self):
        ids=[v["id"] for v in self.data]
        self.assertEqual(len(ids),len(set(ids)))
    def test_fields(self):
        required=["id","kind","title","original","theme","reason","takeaway","action","pitfall"]
        for item in self.data:
            for field in required: self.assertTrue(str(item.get(field,"")).strip(), f'{item.get("id")}: {field}')
    def test_pages(self):
        for file in ["index.html","plan.html","article.html"]:
            self.assertTrue((R/file).exists(),file)
            self.assertIn("<html", (R/file).read_text(encoding="utf-8"))
    def test_links(self):
        s=(R/"index.html").read_text(encoding="utf-8")
        self.assertIn("metaver.vip",s)
        self.assertIn("AIPMAndy",s)
        self.assertIn('id="catalogData"',s)
        self.assertNotIn("/*__CATALOG__*/",s)
if __name__=="__main__":
    unittest.main()
