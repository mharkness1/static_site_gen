import unittest
from blocklogic import markdown_to_blocks, block_to_blocktype, markdown_to_html_node

class TestBlockLogic(unittest.TestCase):
    def test_block_markdown_to_blocks(self):

        assert markdown_to_blocks("Block 1\n\nBlock 2") == ["Block 1", "Block 2"]

        assert markdown_to_blocks("Block 1\n\n\n\nBlock 2") == ["Block 1", "Block 2"]

        assert markdown_to_blocks("* Item 1\n* Item 2\n\nNext Block") == ["* Item 1\n* Item 2", "Next Block"]

        assert markdown_to_blocks("Block 1\n\n    \n\nBlock 2") == ["Block 1", "Block 2"]
    
    def test_block_type_heading(self):

        assert block_to_blocktype("# Heading 1") == "level-1 heading"

        assert block_to_blocktype("## Heading 2") == "level-2 heading"

    def test_block_type_failure(self):
        with self.assertRaises(Exception):
            block_to_blocktype("#No Space Here")

        with self.assertRaises(Exception):
            block_to_blocktype("########### Too many hashes")
    
    def test_block_type_code(self):

        assert block_to_blocktype("``` This is code. ```") == "code"

        assert block_to_blocktype("``` This isn't code") == "paragraph"

        assert block_to_blocktype("`````") == "paragraph"

        assert block_to_blocktype("```This is code.``` But this is also code``` all of this is code```") == "code"

        assert block_to_blocktype("``` All of these many lines \n are all code. \n everyone of them ```") == "code"
    
    def test_block_type_quotes(self):

        assert block_to_blocktype("> quote") == "quote"
        
        assert block_to_blocktype("> quote \n> >> oops") == "quote"

        assert block_to_blocktype(">quote\n>quote") == "quote"

        assert block_to_blocktype(">quote\n not quote") == "paragraph"
    
    def test_block_type_unordered_list(self):

        assert block_to_blocktype("- list\n- list 1\n* list2\n- list 4") == "unordered_list"

        assert block_to_blocktype("- list\n not a list") == "paragraph"

    def test_block_type_ordered_list(self):

        assert block_to_blocktype("1. One \n2. Two\n3. Three") == "ordered_list"
        
        with self.assertRaises(Exception):
            block_to_blocktype("1. One\n3. Three\n2. Two") == "paragraph"

        with self.assertRaises(Exception):
            block_to_blocktype("1. One #nothing\n2. Two\n- three") == "paragraph"

        assert block_to_blocktype("1.One Wrong\n2.Two Wrong\n3. Right") == "paragraph"

    def test_block_type_paragraph(self):
        
        assert block_to_blocktype("This is a paragraph") == "paragraph"
    
        assert block_to_blocktype("This is 1. not an ordered list") == "paragraph"

    def test_markdown_to_html_node(self):
        # Test paragraph
        assert markdown_to_html_node("This is a paragraph").to_html() == "<div><p>This is a paragraph</p></div>"
        
        # Test heading
        assert markdown_to_html_node("# Heading").to_html() == "<div><h1>Heading</h1></div>"
        
        # Test unordered list
        md_list = """* Item 1
    * Item 2"""
        assert markdown_to_html_node(md_list).to_html() == "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        
        # Test code block
        md_code = """```
    print('hello')
    ```"""
        assert markdown_to_html_node(md_code).to_html() == "<div><pre><code>print('hello')</code></pre></div>"
        
        # Test blockquote
        assert markdown_to_html_node("> Quote").to_html() == "<div><blockquote>Quote</blockquote></div>"
        
        # Test inline formatting in list
        md_formatted_list = """* Item **bold**
    * Item *italic*"""
        assert markdown_to_html_node(md_formatted_list).to_html() == "<div><ul><li>Item <b>bold</b></li><li>Item <i>italic</i></li></ul></div>"

    def test_block_to_blocktype_unordered_list_WHO_KNOWS(self):
        list_block = "* Item 1\n* Item 2\n* Item 3"
        assert block_to_blocktype(list_block) == "unordered_list"
        
        list_block_with_dash = "- Item 1\n- Item 2\n- Item 3"
        assert block_to_blocktype(list_block_with_dash) == "unordered_list"


if __name__ == "__main__":
    unittest.main()