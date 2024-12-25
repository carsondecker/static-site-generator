import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
    
    def test_props_to_html2(self):
        node = HTMLNode(props={"src": "styles.css",})
        self.assertEqual(node.props_to_html(), " src=\"styles.css\"")
    
    def test_props_to_html_false(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node.props_to_html(), "")
    
    def test_repr(self):
        child_node = HTMLNode(tag="a")
        node = HTMLNode(tag="a", value="This is text", children=[child_node], props={"href": "https://www.google.com", "target": "_blank",}, )
        self.assertEqual(
            node.__repr__(), "HTMLNode(tag=\"a\", value=\"This is text\", children=\"[HTMLNode(tag=\"a\", value=\"None\", children=\"None\", props=\"\")]\", props=\" href=\"https://www.google.com\" target=\"_blank\"\")"
            )