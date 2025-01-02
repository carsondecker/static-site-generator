import unittest
from textnode import TextType, TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from converter import text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type, remove_block_markdown, block_to_html_node

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
    
    def test_block_to_block_type_paragraph(self):
        block = ">*1. This is just a misleading paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), (BlockType.HEADING, 4))
    
    def test_block_to_block_type_code(self):
        block = "```This is code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block = "> This\n> is\n> a\n> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_to_block_type_ul(self):
        block = "* This\n* is\n* an\n* unordered\n* list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ol(self):
        block = "1. This\n2. is\n3. an\n4. ordered\n5. list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_remove_block_markdown_paragraph(self):
        block = ">*1. This is just a misleading paragraph"
        self.assertEqual(remove_block_markdown(block, BlockType.PARAGRAPH), ">*1. This is just a misleading paragraph")
    
    def test_remove_block_markdown_heading(self):
        block = "#### This is a heading"
        self.assertEqual(remove_block_markdown(block, BlockType.HEADING), "This is a heading")
    
    def test_remove_block_markdown_code(self):
        block = "```This is code```"
        self.assertEqual(remove_block_markdown(block, BlockType.CODE), "This is code")
    
    def test_remove_block_markdown_quote(self):
        block = "> This\n> is\n> a\n> quote"
        self.assertEqual(remove_block_markdown(block, BlockType.QUOTE), "This\nis\na\nquote")
    
    def test_remove_block_markdown_ul(self):
        block = "* This\n* is\n* an\n* unordered\n* list"
        self.assertEqual(remove_block_markdown(block, BlockType.UNORDERED_LIST), "This\nis\nan\nunordered\nlist")
    
    def test_remove_block_markdown_ol(self):
        block = "1. This\n2. is\n3. an\n4. ordered\n5. list"
        self.assertEqual(remove_block_markdown(block, BlockType.UNORDERED_LIST), "This\nis\nan\nordered\nlist")
    
    def test_block_to_html_node_heading(self):
        block = "#### This is a heading"
        block_type, headingNum = block_to_block_type(block)
        self.assertEqual(block_to_html_node(block, block_type, headingNum).__repr__(), HTMLNode(tag="h4", children=[LeafNode(value="This is a heading")]).__repr__())
    
    def test_block_to_html_node_ol(self):
        block = "1. This\n2. is\n3. an\n4. ordered\n5. list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_to_html_node(block, block_type).__repr__(), HTMLNode(tag="ol", children=[HTMLNode(tag="li", children=[LeafNode(value="This")]), HTMLNode(tag="li", children=[LeafNode(value="is")]), HTMLNode(tag="li", children=[LeafNode(value="an")]), HTMLNode(tag="li", children=[LeafNode(value="ordered")]), HTMLNode(tag="li", children=[LeafNode(value="list")])]).__repr__())
    
    def test_block_to_html_node_quote(self):
        block = "> This\n> is\n> a\n> quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_to_html_node(block, block_type).__repr__(), HTMLNode(tag="blockquote", children=[LeafNode(value="This\nis\na\nquote")]).__repr__())