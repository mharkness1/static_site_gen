import re

from textnode import TextType, TextNode

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("invalid markdown syntax")

        for i in range(0, len(split_node)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
