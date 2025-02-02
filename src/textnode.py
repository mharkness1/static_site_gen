from enum import Enum
from htmlnode import LeafNode, HTMLNode

# Enforces typing for textnodes (the core componenent of the conversion system)
class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

# Accurately tags a Leafnode with the relevant HTML info and props.    
def text_node_to_html_node(text_node):
    if isinstance(text_node, list):
        # If it's a list of text nodes, wrap them in a parent node
        return HTMLNode(None, None, [text_node_to_html_node(node) for node in text_node])
    
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    else:
        raise ValueError("invalid text type")