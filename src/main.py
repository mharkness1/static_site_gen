from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from delimiter import split_nodes_link, split_node_delimiter, split_nodes_image, text_to_textnodes
from blocklogic import block_to_blocktype, markdown_to_html_node, extract_title
from file_management import get_file_paths, copy_static, clear_dst_dir, generate_page, generate_pages_recursive

def static_to_public():
    dst_dir, src_dir = get_file_paths()
    clear_dst_dir(dst_dir)
    copy_static(src_dir, dst_dir)
    return

def main():
    static_to_public()
    generate_pages_recursive("content/", "template.html", "public/")
    #generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
	main()
