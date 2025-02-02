from textnode import TextNode, TextType, text_node_to_html_node
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from delimiter import text_to_textnodes

# Splits markdown into blocks.
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    non_empty_blocks = []

    for block in blocks:
        block = block.strip()
        if block != "":
            non_empty_blocks.append(block)

    return non_empty_blocks

# Returns a string representing the block type.
def block_to_blocktype(block):
    if block.startswith("#"):        
        if re.match(r"^#{1,6} ", block):
            x = block.find(" ")
            if 1 <= x <= 6:
                return f"level-{x} heading"
        else:
            raise Exception("incorrect markdown syntax - heading")
    
    if block.startswith("```") and block.endswith("```") and len(block) > 6:
        return "code"
    
    if block.startswith(">"):
        lines = block.split("\n")
        if all(line.startswith(">") for line in lines):
            return "quote"
    
    if block.startswith("* ") or block.startswith("- "):
        lines = block.split("\n")
        if all(line.strip().startswith("* ") or line.strip().startswith("- ") for line in lines):
            return "unordered_list"
    
    if block.startswith("1. "):
        lines = block.split("\n")
        line_counter = 1
        for line in lines:
            if line.startswith(f"{line_counter}. "):
                line_counter += 1
                continue
            else:
                raise Exception("invalid markdown syntax - ordered list")
        return "ordered_list"
    
    return "paragraph"

################### NEED TO REDO BELOW ##################
# NEED OUTPUT OF HTMLNODES THEREFORE: NEED TAGS, VALUES, CHILDREN, PROPS.
# THEREFORE NEED TO CHECK STRINGS AND RETURN LISTS OF CHILDREN I.E., INLINE FORMATTING. TEXTNODE -> HTMLNODE FUNC: STRING TO CHILDREN NODES 
# EVERYTHING HAS TO BE WRAPPED IN A DIV AT THE END (FUNC: DIV WRAPPER)
# REMEMBER ALL INLINE FORMATTING IS A LEAFNODE.


# THIS SHOULD BE RETURNING HTMLNODE() NOT STRINGS ALAS. This returns the necessary tag.
def block_to_html_tag(block_type):
    if block_type == "paragraph":
        return f"p"
    elif block_type == "level-1 heading":
        return f"h1"
    elif block_type == "level-2 heading":
        return f"h2"
    elif block_type == "level-3 heading":
        return f"h3"
    elif block_type == "level-4 heading":
        return f"h4"
    elif block_type == "level-5 heading":
        return f"h5"
    elif block_type == "level-6 heading":
        return f"h6"
    elif block_type == "code":
        return f"pre"
    elif block_type == "quote":
        return f"blockquote"
    elif block_type == "ordered_list":
        return f"ol"
    elif block_type == "unordered_list":
        return f"ul"
    else:
        raise ValueError("invalid block type")

# Returns a list of LeafNodes with li tag, to be nested within a parent ordered/unordered list.
def list_to_inner_html_li(block):
    items = block.split("\n")
    list_children = []
    for item in items:
        print(f"processing item: {item}")
        item_text = item.strip()
        item_text = item_text[2:]
        item_text = item_text.lstrip()
        print(f"cleaned: {item_text}")
        text_nodes = text_to_textnodes(item_text)
        item_html_node = text_node_to_html_node(text_nodes)
        print(f"HTML Node is: {item_html_node}")
        print(f"item_html_node type: {type(item_html_node)}")
        print(f"item_html_node value: {item_html_node.value}")
        if item_html_node.children:
            for child in item_html_node.children:
                print(f"child type: {type(child)}, value: {child.value}")

        li_node = HTMLNode("li", None, [item_html_node])
        list_children.append(li_node)
    return list_children

# Returns the block with the code tags applied.
def code_inner_html(code_lines):
    return "\n".join(code_lines)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    markdown_as_htmlnodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        tag = block_to_html_tag(block_type)
        children = []
        
        if block_type.endswith("heading"):
            content = block.lstrip("#").strip()
            markdown_as_htmlnodes.append(HTMLNode(tag, text_node_to_html_node(text_to_textnodes(content))))
            continue

        if block_type == "ordered_list" or block_type == "unordered_list":
            li_nodes = list_to_inner_html_li(block)
            markdown_as_htmlnodes.append(HTMLNode(tag, None, li_nodes))
            continue

        if block_type == "quote":
            lines = block.split("\n")
            quote_content = ""
            for line in lines:
                quote_content += line[2:]
            markdown_as_htmlnodes.append(HTMLNode(tag, quote_content))
            continue
        
        if block_type == "code":
            lines = block.split("\n")
            code_lines = lines[1:-1]
            code_node = code_inner_html(code_lines).lstrip()
            markdown_as_htmlnodes.append(HTMLNode("pre", None, [HTMLNode("code", code_node)]))
            continue

        markdown_as_htmlnodes.append(HTMLNode(tag, text_node_to_html_node(text_to_textnodes(block))))

    return HTMLNode("div", None, markdown_as_htmlnodes)
        #children = [] #placeholder implement a child return function.
        #HTMLNode(tag, block, children, props)
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_blocktype(block) == "level-1 heading":
            print("found heading")
            heading = block[1:]
            return heading.lstrip()
    raise Exception("no header")