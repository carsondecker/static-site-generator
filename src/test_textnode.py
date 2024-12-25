import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    
    def test_text_node_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.text_node_to_html_node().__repr__(), LeafNode(value="This is a text node").__repr__())
    
    def test_text_node_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_node_to_html_node().__repr__(), LeafNode(tag="b", value="This is a text node").__repr__())

    def test_text_node_to_html_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_node_to_html_node().__repr__(), LeafNode(tag="i", value="This is a text node").__repr__())
    
    def test_text_node_to_html_code(self):
       node = TextNode("This is a text node", TextType.CODE)
       self.assertEqual(node.text_node_to_html_node().__repr__(), LeafNode(tag="code", value="This is a text node").__repr__())
       
    def test_text_node_to_html_link(self):
       node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
       self.assertEqual(node.text_node_to_html_node().__repr__(), LeafNode(tag="a", value="This is a text node", props={"href": "https://www.boot.dev"}).__repr__())
      
    def test_text_node_to_html_img(self):
       node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
       self.assertEqual(node.text_node_to_html_node().__repr__(), LeafNode(tag="img", value="", props={"src": "https://www.boot.dev", "alt": "This is a text node"}).__repr__())
       

if __name__ == "__main__":
    unittest.main()