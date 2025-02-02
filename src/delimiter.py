import re

from textnode import TextType, TextNode

def split_node_delimiter(old_nodes, delimiter, text_type):
    # takes a list of NORMAL nodes (by default), iterates over a provided delimiter and converts the node.
    # converts to list of new nodes where the TextType is altered for the text inside the delimiter. Returns as a list.
    new_nodes = []

    for node in old_nodes:
        # automatically add any nodes that have already been given the correct type from markdown.
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        # Handles conflict between unordered lists starting with * and italics that would raise syntax error.
        if node.text.lstrip().startswith("* "):
            new_nodes.append(node)
            continue

        split_node = node.text.split(delimiter)
        # any split will always result in an odd number of list elements (before markdown, after markdown, markdown).
        # Thus, if there is an even number of elements, there must have been a markdown error.
        if len(split_node) % 2 == 0:
            raise Exception("invalid markdown syntax")

        for i in range(0, len(split_node)):
            # iterate over the entire split node. For even elements, the text type is normal. [before][markdown][after][mardown]...
            # if a node begins with markdown an empty string begins the list. if not even, then its markdown and all appended.
            if i % 2 == 0 and split_node[i] != "":
                new_nodes.append(TextNode(split_node[i], TextType.NORMAL))
            elif split_node[i] != "":
                new_nodes.append(TextNode(split_node[i], text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # iterate through nodes (list items) in the input, it is a list of text 'lines'.
        if node.text_type != TextType.NORMAL:
            # append any node that has already had an updated text type.
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        # images takes the form of a [(a,b)(c,d)] list of tuples. Each looks like: (alt_text, url).
        if not images:
            new_nodes.append(node)
            continue

        current_text = node.text
        # iterate over the return tuples
        for alt_text, img_url in images:
            # Split around the relevant markdown syntax.
            parts = current_text.split(f"![{alt_text}]({img_url})", 1)
            # Add part before markdown if it isn't empty.
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            # Add the image markdown to a new node, formatted correctly.
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_url))

            # Update the current text to be what's left after the link, and run it again.
            current_text = parts[1] if len(parts) > 1 else ""

        # Add any text remaning to the new node once all images have been iterated over.
        new_nodes.append(TextNode(current_text, TextType.NORMAL))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # iterate through nodes (list items) in the input, it is a list of text 'lines'.
        if node.text_type != TextType.NORMAL:
            # automatically add any nodes that have already been given the correct type from markdown.
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        # checks to see if there are any links in the node, if not, it just immediately adds it.
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.text
        # iterate over the already returned tuples in the links.
        for link_text, link_url in links:
            # Split around the markdown link syntax.
            parts = current_text.split(f"[{link_text}]({link_url})", 1)
            
            # Add the text before the link.
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            
            # Add the link node.
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Update current_text to what remains.
            current_text = parts[1] if len(parts) > 1 else ""

        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    # returns a list of tuples of each of the groups above (), for images this is (alt_text, url)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    # returns a list of tuples of each of the groups (), for texts this is (text, url)
    return matches

def text_to_textnodes(text):
    converted_text = [TextNode(text, TextType.NORMAL)]
    converted_text = split_nodes_link(converted_text)
    converted_text = split_nodes_image(converted_text)
    converted_text = split_node_delimiter(converted_text, "**", TextType.BOLD)
    converted_text = split_node_delimiter(converted_text, "*", TextType.ITALIC)
    converted_text = split_node_delimiter(converted_text, "`", TextType.CODE)

    return converted_text