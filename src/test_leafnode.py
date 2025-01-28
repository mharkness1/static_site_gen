import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq_2(self):
        leaf = LeafNode("p","This is a paragraph")
        leaf2 = "<p>This is a paragraph</p>"
        self.assertEqual(leaf.to_html(), leaf2)

    def test_eq_3(self):
        leaf = LeafNode("a","This is a link", {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        leaf2 = '<a href="https://www.google.com" target="_blank">This is a link</a>'
        self.assertEqual(str(leaf.to_html()), leaf2)