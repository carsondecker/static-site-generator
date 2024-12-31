import unittest
from textnode import TextType, TextNode
from converter import text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type

class TestConverter(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ])
    
    def test_text_to_textnode_2(self):
        text = "**Man, ***do *`I `love **spamming **`symbols`"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("Man, ", TextType.BOLD),
            TextNode("do ", TextType.ITALIC),
            TextNode("I ", TextType.CODE),
            TextNode("love ", TextType.TEXT),
            TextNode("spamming ", TextType.BOLD),
            TextNode("symbols", TextType.CODE),
            ])
    
    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(markdown_to_blocks(markdown), ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"])
    
    '''
    def test_block_to_block_type(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.)
    '''
    def test_block_to_block_type_paragraph(self):
        block = ">*1. This is just a misleading paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        block = "```This is code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block = "> This\n> is\n> a> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_to_block_type_ul(self):
        block = "* This\n* is\n* an\n* unordered\n* list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ol(self):
        block = "1. This\n2. is\n3. an\n4. ordered\n5. list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)