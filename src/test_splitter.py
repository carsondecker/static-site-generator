import unittest
from splitter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" word", TextType.TEXT),
            ])
    
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            ])
    
    def test_split_nodes_delimiter_italics(self):
        node = TextNode("This is text with a word at the end that is *italicized*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a word at the end that is ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            ])
    
    def test_split_nodes_delimiter_starting_delimiter(self):
        node = TextNode("**This text** starts with a bolded phrase", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This text", TextType.BOLD),
            TextNode(" starts with a bolded phrase", TextType.TEXT),
            ])
        
    def test_split_nodes_delimiter_ending_delimiter(self):
        node = TextNode("This text ends with a **bolded phrase**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This text ends with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            ])
    
    def test_split_nodes_delimiter_multiple_phrases(self):
        node = TextNode("This is text with **two different bolded phrases**, isn't that **crazy**?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("two different bolded phrases", TextType.BOLD),
            TextNode(", isn't that ", TextType.TEXT),
            TextNode("crazy", TextType.BOLD),
            TextNode("?", TextType.TEXT),
            ])
    
    def test_split_notes_delimiter_multiple_nodes(self):
        node1 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        node2 = TextNode("This is text with **two different bolded phrases**, isn't that **crazy**?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            TextNode("This is text with ", TextType.TEXT),
            TextNode("two different bolded phrases", TextType.BOLD),
            TextNode(", isn't that ", TextType.TEXT),
            TextNode("crazy", TextType.BOLD),
            TextNode("?", TextType.TEXT),
            ])
    
    def test_split_nodes_delimiter_error(self):
        node = TextNode("This is **invalid markdown syntax", TextType.TEXT)
        with self.assertRaises(Exception, msg="Missing matching delimiter \"**\""):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)