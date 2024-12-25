import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_to_html2(self):
        node = ParentNode(
            tag="a",
            children=[
                ParentNode("p", [LeafNode("b", "Bold text")]),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            props={
                "href": "https://google.com"
            }
        )
        self.assertEqual(node.to_html(), "<a href=\"https://google.com\"><p><b>Bold text</b></p>Normal text<i>italic text</i>Normal text</a>")
    
    def test_to_html_error(self):
        node = ParentNode()
        with self.assertRaises(ValueError, msg="No tag on parent node."):
            node.to_html()
        
    def test_to_html_error2(self):
        node = ParentNode("a")
        with self.assertRaises(ValueError, msg="No children on parent node."):
            node.to_html()