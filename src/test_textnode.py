import unittest

from htmlnode import *
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This is a text node", "bold", "url.com")
        node2 = TextNode("This is a text node", "bold" , "url.com")
        self.assertEqual(node1, node2)

    def test_uneq_text(self):
        node1 = TextNode("This is one text node", "bold")
        node2 = TextNode("This is another text node", "bold")
        self.assertNotEqual(node1, node2)

    def test_uneq_text_type(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node1, node2)

    def test_uneq_url(self):
        node1 = TextNode("This is a text node", "bold", "url.com")
        node2 = TextNode("this is a text node", "bold")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://url.com")
        self.assertEqual(repr(node), f"TextNode({node.text}, {node.text_type}, {node.url})")

    def test_repr_none_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)
        self.assertEqual(repr(node), f"TextNode({node.text}, {node.text_type}, None)")

class TestTextToHTML(unittest.TestCase):
    def test_raw_text(self):
        text_node = TextNode("raw text", "text")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            LeafNode(None, "raw text").to_html()
        )

    def test_bold_text(self):
        text_node = TextNode("bold text", "bold")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            LeafNode("b", "bold text").to_html()
        )

    def test_italic_text(self):
        text_node = TextNode("italic text", "italic")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            LeafNode("i", "italic text").to_html()
        )

    def test_code_tag(self):
        text_node = TextNode("code text", "code")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            LeafNode("code", "code text").to_html()
        )

    def test_link_text(self):
        text_node = TextNode("google", "link", "https://www.google.com")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            LeafNode("a", "google", {"href": "https://www.google.com"}).to_html()
        )

    def test_img_tag(self):
        text_node = TextNode("img tag", "image", "https://imgur.com/img123")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            LeafNode("img", "", {"src": "https://imgur.com/img123", "alt": "img tag"}).to_html()
        )

if __name__ == "__main__":
    unittest.main()
