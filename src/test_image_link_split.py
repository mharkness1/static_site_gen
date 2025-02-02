import unittest
from delimiter import split_nodes_image, split_nodes_link
from textnode import TextType, TextNode

class TestImageLinkSplit(unittest.TestCase):
    def test_link_single_split(self):
        node = TextNode("This is [a link](www.google.co.uk)", TextType.NORMAL)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        assert nodes[0].text == "This is "
        assert nodes[1].text == "a link"
        assert nodes[1].url == "www.google.co.uk"
        assert nodes[1].text_type == TextType.LINK

    def test_link_no_links(self):
        node = TextNode("This is just plain text", TextType.NORMAL)
        nodes = split_nodes_link([node])
        assert len(nodes) == 1
        assert nodes[0].text == "This is just plain text"
    
    def test_link_multiple_links(self):
        node = TextNode("Here are two links: [one](url1) and [two](url2)", TextType.NORMAL)
        nodes = split_nodes_link([node])
        assert len(nodes) == 4
        assert nodes[0].text == "Here are two links: "
        assert nodes[1].url == "url1"
        assert nodes[3].text == "two"
        assert nodes[3].text_type == TextType.LINK
        assert nodes[2].text_type == TextType.NORMAL
    
    def test_link_with_image(self):
        node = TextNode("This is an image ![image](url)", TextType.NORMAL)
        nodes = split_nodes_link([node])
        assert len(nodes) == 1
        assert nodes[0].text == "This is an image ![image](url)"
        assert nodes[0].text_type == TextType.NORMAL
    
    def test_link_no_text_between(self):
        node = TextNode("[one](url1)[two](url2)", TextType.NORMAL)
        nodes = split_nodes_link([node])
        assert len(nodes) == 2
        assert nodes[0].text == "one"
        assert nodes[1].text == "two"

    def test_linke_multiple_mixed_nodes(self):
        nodes = [
            TextNode("[link](url)", TextType.NORMAL),
            TextNode("plain text", TextType.NORMAL),
            TextNode("![image](url)", TextType.IMAGE),
            TextNode("[link2](url2)", TextType.NORMAL)
        ]
        result = split_nodes_link(nodes)
        assert len(result) == 4

if __name__ == "__main__":
    unittest.main()