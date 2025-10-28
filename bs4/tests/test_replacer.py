import unittest
from bs4 import BeautifulSoup
from bs4.soupreplacer import SoupReplacer

class TestSoupReplacer(unittest.TestCase):
    def test_tag_replacement(self):
        html = "<html><body><b>Bold</b></body></html>"
        replacer = SoupReplacer("b", "blockquote")
        soup = BeautifulSoup(html, "html.parser", replacer=replacer)
        self.assertIn("<blockquote>", str(soup))
        self.assertNotIn("<b>", str(soup))

    def test_no_replacement(self):
        html = "<html><body><i>Italic</i></body></html>"
        replacer = SoupReplacer("b", "blockquote")
        soup = BeautifulSoup(html, "html.parser", replacer=replacer)
        self.assertIn("<i>", str(soup))
        self.assertNotIn("<blockquote>", str(soup))

if __name__ == "__main__":
    unittest.main()
