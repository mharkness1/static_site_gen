import unittest

from htmlnode import ParentNode
from htmlnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_eq(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_parent_nested_parent(self):
        node = ParentNode(
        "div",
        [   
            ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        ],
        )
        self.assertEqual(node.to_html(), '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>')
    
    def test_parent_nested_parent_child(self):
        node = ParentNode(
        "div",
        [   
            LeafNode("h1","Title"),
            ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        ],
        )
        self.assertEqual(node.to_html(), '<div><h1>Title</h1><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>')

    def test_parent_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "text")])
            node.to_html()

    def test_parent_empty_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])
            node.to_html()
    
    def test_parent_none_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()

    def test_parent_nested_2(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("b", "Bold")
            ]),
            LeafNode("i", "Italic")
        ])
        self.assertEqual(node.to_html(), '<div><p><b>Bold</b></p><i>Italic</i></div>')
    
    def test_parent_properties(self):
        node = ParentNode("div", [LeafNode("p", "text")], {"class": "container"})
        self.assertEqual(node.to_html(),'<div class="container"><p>text</p></div>')

    def test_parent_mixed_content(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, "Normal"),
            LeafNode("i", "Italic")
        ])
        self.assertEqual(node.to_html(),'<p><b>Bold</b>Normal<i>Italic</i></p>')