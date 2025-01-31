import unittest
from textnode import TextNode, TextType
from delimiter import split_node_delimiter, extract_markdown_images, extract_markdown_links


class TestDelimiter(unittest.TestCase):
    def test_delim_basic_delimiter(self):
        node = TextNode("hello `code` world", TextType.NORMAL)
        result = split_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "hello ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " world")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_delim_multiple_delimiters(self):
        node = TextNode("hello `code` and `more code`", TextType.NORMAL)
        result = split_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 5)

    def test_delim_no_delimiter(self):
        node = TextNode("just plain text", TextType.NORMAL)
        result = split_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "just plain text")

    def test_delim_unclosed_delimiter(self):
        node = TextNode("unclosed `delimiter", TextType.NORMAL)
        with self.assertRaises(Exception):
            split_node_delimiter([node], "`", TextType.CODE)
    
    def test_delim_bold(self):
        node = TextNode("this is **bold** text", TextType.NORMAL)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result),3)
        self.assertEqual(result[0].text, "this is ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
    
    def test_delim_not_normal(self):
        node = TextNode("this is text", TextType.ITALIC)
        result = split_node_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0].text, "this is text")
        self.assertEqual(result[0].text_type, TextType.ITALIC)

    def test_delim_list_nodes(self):
        nodes = [
                TextNode("hello `code` world", TextType.NORMAL),
                TextNode("hello `code` world", TextType.NORMAL)
                ]
        result = split_node_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 6)

    def test_delim_no_text_between_case(self):
        node = TextNode("hello `` world", TextType.NORMAL)
        result = split_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "")

if __name__ == "__main__":
    unittest.main()

