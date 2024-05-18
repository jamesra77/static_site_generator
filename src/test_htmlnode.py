import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="https://google.com", children= ["strong"], props={"someProp": "someValue", "otherProp": "otherValue"})
        self.assertEqual(
            f" someProp=\"{node.props["someProp"]}\" otherProp=\"otherValue\"",
            node.props_to_html()
        )

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(
            f"HTMLNode({node.tag}, {node.value}, children: {node.children}, {node.props})",
            repr(node)
        )

    def test_to_html(self):
        leaf_a = LeafNode(tag="a", value="clicky", props={"href": "https://www.google.com"})
        leaf_p = LeafNode(tag="p", value="this is the only thing I can say")
        self.assertEqual(leaf_a.to_html(), '<a href="https://www.google.com">clicky</a>')
        self.assertEqual(leaf_p.to_html(), '<p>this is the only thing I can say</p>')

    def test_to_html_no_tag(self):
        leaf = LeafNode(None, "plain text")
        self.assertEqual(
            leaf.to_html(), "plain text"
        )

    def test_to_html_no_children(self):
        leaf = LeafNode("span", "some inline text")
        self.assertEqual(
            leaf.to_html(), f"<span>some inline text</span>"
        )

    def test_to_html_with_children(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
            ]
        )
        self.assertEqual(
            parent.to_html(),
            "<p><b>bold text</b></p>"
        )

    def test_to_html_with_grandchildren(self):
        child_node = ParentNode(
            "p",
            [
                LeafNode("b", "bold text")
            ]
        )
        parent_node = ParentNode(
            "div",
            [
                child_node
            ]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><b>bold text</b></p></div>"
        )

    def test_to_html_many_children(self):
        parent_node = ParentNode(
            "div",
            [
                LeafNode("b", "some bold text"),
                LeafNode(None, "plain text"),
                LeafNode("i", "italic text")
            ]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>some bold text</b>plain text<i>italic text</i></div>"
        )

    def test_to_html_heading(self):
        parent_node = ParentNode(
            "h1",
            [
                LeafNode("b", "some bold text"),
                LeafNode(None, "plain text"),
                LeafNode("i", "italic text")
            ]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<h1><b>some bold text</b>plain text<i>italic text</i></h1>"
        )
