from textnode import TextType

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        
        split_node = node.text.split(delimiter)
        
