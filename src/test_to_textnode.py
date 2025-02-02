import unittest
from delimiter import text_to_textnodes
from textnode import TextType

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        text = "Hello world"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "Hello world"
        assert nodes[0].text_type == TextType.NORMAL

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " text"

    def test_text_to_textnodes_mixed(self):
        text = "This is `code` and *italic*"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 4
        assert nodes[1].text == "code"
        assert nodes[1].text_type == TextType.CODE
        assert nodes[3].text == "italic"
        assert nodes[3].text_type == TextType.ITALIC

    def test_text_to_textnodes_link(self):
        text = "Click [here](https://boot.dev) now"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[1].text == "here"
        assert nodes[1].text_type == TextType.LINK
        assert nodes[1].url == "https://boot.dev"

if __name__ == "__main__":
    unittest.main()