import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_text_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_text_node_url(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)
    
    def test_text_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "www.goodle.com")
        self.assertNotEqual(node, node2)

class TestConvertFunction(unittest.TestCase):
    def test_convert_link_node(self):
        text_node = TextNode("click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "a"
        assert html_node.value == "click me"
        assert html_node.props == {"href": "https://example.com"}
    
    def test_convert_normal_node(self):
        text_node = TextNode("normal text", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "normal text"
        assert html_node.props == {}
    
    def test_convert_bold_node(self):
        text_node = TextNode("bold text", TextType.BOLD, "shouldn't be a prop")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "b"
        assert html_node.value == "bold text"
        assert html_node.props == {}

    def test_convert_italic_node(self):
        text_node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "i"
        assert html_node.value == "italic text"
        assert html_node.props == {}

    def test_convert_type_error_none(self):
        with self.assertRaises(ValueError):
            text_node = TextNode("value error", None)
            text_node_to_html_node(text_node)
    
    def test_convert_type_error_string(self):
        with self.assertRaises(ValueError):
            text_node = TextNode("value error", "None")
            text_node_to_html_node(text_node)

    def test_convert_img_node(self):
        text_node = TextNode("alt text", TextType.IMAGE, "image source")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "img"
        assert html_node.value == ""
        assert html_node.props == {"src":"image source", "alt":"alt text"}
    
    def test_convert_code_node(self):
        text_node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "code"
        assert html_node.value == "code text"


if __name__ == "__main__":
    unittest.main()