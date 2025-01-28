import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_html_eq(self):
        node = HTMLNode("p", "This is random text", None, None)
        node2 = HTMLNode("p", "This is random text")
        self.assertEqual(node, node2)

    def test_html_repr(self):
        self.assertEqual(repr(HTMLNode("h1", "Title")), "HTMLNode(h1, Title, no children, no props)")

    def test_html_props_to_html(self):
        node = HTMLNode("a", "This is a link", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_html_not_eq(self):
        node = HTMLNode("h1", "This is a title", None, None)
        node2 = HTMLNode("p", "This is a paragraph, not a heading", None, None)
        self.assertNotEqual(node, node2)
    
    def test_html_props_single(self):
        node = HTMLNode("a", "This is a link", None,{
            "href": "https://www.google.com",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_html_eq_2(self):
        node = HTMLNode("p", "paragraph", [])
        node2 = HTMLNode("p", "paragraph", None, {})
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()