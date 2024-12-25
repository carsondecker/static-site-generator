import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    
    def test_to_html2(self):
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_to_html_false(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertNotEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")