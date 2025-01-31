import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_conversion_no_props(self):
        leaf = LeafNode("p","This is a paragraph")
        leaf2 = "<p>This is a paragraph</p>"
        self.assertEqual(leaf.to_html(), leaf2)

    def test_leaf_html_conversion_with_props(self):
        leaf = LeafNode("a","This is a link", {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        leaf2 = '<a href="https://www.google.com" target="_blank">This is a link</a>'
        self.assertEqual(leaf.to_html(), leaf2)
    
    def test_leaf_value_error(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode("h2", None)
            leaf.to_html()
    
    def test_leaf_no_tag(self):
        leaf = LeafNode(None, "There is no tag")
        self.assertEqual(leaf.to_html(), "There is no tag")

    def test_leaf_empty_prop_dict(self):
        leaf = LeafNode("p","Paragraph",{})
        self.assertEqual(leaf.to_html(), "<p>Paragraph</p>")

if __name__ == "__main__":
    unittest.main()