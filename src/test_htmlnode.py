import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is random text", None, None)
        node2 = HTMLNode("p", "This is random text")
        self.assertEqual(node, node2)

    def test_repr(self):
        return repr(HTMLNode("h1", "Title")) == "HTMLNode(h1, Title)"

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        return node.props_to_html() == 'href="https://www.google.com" target="_blank"'

    def test_not_eq(self):
        node = HTMLNode("h1", "This is a title", None, None)
        node2 = HTMLNode("p", "This is a paragraph, not a heading", None, None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()