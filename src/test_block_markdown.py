import unittest

from block_markdown import (
    markdown_to_blocks,
    is_ordered_list,
    block_to_block_type,
    block_to_paragraph,
    block_to_heading,
    block_to_code,
    block_to_quote,
    block_to_unordered_list,
    block_to_ordered_list,
    markdown_to_html_node,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
)
from htmlnode import ParentNode, LeafNode

class TestMarkdownToBlocks(unittest.TestCase):
    def test_one_multiline_mdblock(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""

        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
        )

    def test_two_multiline_mdblocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_is_ordered_list(self):
        self.assertEqual(
            is_ordered_list("""1. yes indeed, this is an ordered list
2. second item on said list
3. third item, threeish... yes
4. even numbers are kool"""),
            True
        )

    def test_block_to_block_type_all_types(self):
        self.assertEqual(
            block_to_block_type("```haxor```"),
            block_type_code
        )
        self.assertEqual(
            block_to_block_type("## some h2 text"),
            block_type_heading
        )
        self.assertEqual(
            block_to_block_type("some good ol' paragraph text"),
            block_type_paragraph
        )
        self.assertEqual(
            block_to_block_type(">meme arrows"),
            block_type_quote
        )
        self.assertEqual(
            block_to_block_type("* unordered list item 1\n* unordered list item 2"),
            block_type_unordered_list
        )
        self.assertEqual(
            block_to_block_type("1. first ol item\n2. second ol item\n3. third ol item, cool"),
            block_type_ordered_list
        )

class TestBlockToHtml(unittest.TestCase):
    def test_block_to_paragraph(self):
        para_text = "this is some *paragraph* text, it has **bold** and *italic* children, and even a [link](https://www.google.com)!"
        para_node = ParentNode(
                "p",
                [
                    LeafNode(None, "this is some "),
                    LeafNode("i", "paragraph"),
                    LeafNode(None, " text, it has "),
                    LeafNode("b", "bold"),
                    LeafNode(None, " and "),
                    LeafNode("i", "italic"),
                    LeafNode(None, " children, and even a "),
                    LeafNode("a", "link", {"href": "https://www.google.com"}),
                    LeafNode(None, "!")
                ]
            )
        self.assertEqual(
            block_to_paragraph(para_text),
            para_node
        )

    def test_block_to_heading(self):
        h1 = "# some h1 text with an inline `code` block"
        h2 = "## some h2 text with an inline *italic* node and **bold** node"
        h6 = "###### some h6 text with *italic* text and an image ![an image](https://www.coolpics.com/img.png)"
        h1_node = ParentNode(
            "h1",
            [
                LeafNode(None, "some h1 text with an inline "),
                LeafNode("code", "code"),
                LeafNode(None, " block")
            ]
        )
        h2_node = ParentNode(
            "h2",
            [
                LeafNode(None, "some h2 text with an inline "),
                LeafNode("i", "italic"),
                LeafNode(None, " node and "),
                LeafNode("b", "bold"),
                LeafNode(None, " node")
            ]
        )
        h6_node = ParentNode(
            "h6",
            [
                LeafNode(None, "some h6 text with "),
                LeafNode("i", "italic"),
                LeafNode(None, " text and an image "),
                LeafNode("img", "", {"src": "https://www.coolpics.com/img.png", "alt": "an image"})
            ]
        )
        self.assertEqual(
            block_to_heading(h1),
            h1_node
        )
        self.assertEqual(
            block_to_heading(h2),
            h2_node
        )
        self.assertEqual(
            block_to_heading(h6),
            h6_node
        )

    def test_block_to_code(self):
        code_text = "```uber l33t hax0r code block```"
        code_block_node = ParentNode(
            "pre",
            [
                ParentNode(
                    "code",
                    [
                        LeafNode(None, "uber l33t hax0r code block")
                    ]
                )
            ]
        )
        self.assertEqual(
            block_to_code(code_text),
            code_block_node
        )

    def test_block_to_quote(self):
        blockquote_text = """> le epic meme arrows.
> who are you quoting?
> multiline strings in python are weird.
> there I said it"""
        blockquote_node = ParentNode(
            "blockquote",
            [LeafNode(None, "le epic meme arrows. who are you quoting? multiline strings in python are weird. there I said it")]
        )
        self.assertEqual(
            block_to_quote(blockquote_text),
            blockquote_node
        )

    def test_block_to_unordered_list(self):
        ul_text = """* first item
* second *item*
* third **item**"""
        ul_node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "first item")]),
                ParentNode("li", [LeafNode(None, "second "), LeafNode("i", "item")]),
                ParentNode("li", [LeafNode(None, "third "), LeafNode("b", "item")])
            ]
        )
        self.assertEqual(
            block_to_unordered_list(ul_text),
            ul_node
        )

    def test_block_to_ordered_list(self):
        ol_text = """1. first item
2. second *item*
3. third **item**"""
        ol_node = ParentNode(
            "ol",
            [
                ParentNode("li", [LeafNode(None, "first item")]),
                ParentNode("li", [LeafNode(None, "second "), LeafNode("i", "item")]),
                ParentNode("li", [LeafNode(None, "third "), LeafNode("b", "item")])
            ]
        )
        self.assertEqual(
            block_to_ordered_list(ol_text),
            ol_node
        )

    def test_markdown_to_html_node(self):
        markdown = """a simple paragraph block

# an h1 block

```int main()```

> some quoted text
> on multiple lines

no attribution

* first item
* second item

1. first thing
2. second thing"""
        div_node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode(None, "a simple paragraph block")]
                ),
                ParentNode(
                    "h1",
                    [LeafNode(None, "an h1 block")]
                ),
                ParentNode(
                    "pre",
                    [ParentNode("code", [LeafNode(None, "int main()")])]
                ),
                ParentNode(
                    "blockquote",
                    [LeafNode(None, "some quoted text on multiple lines")]
                ),
                ParentNode(
                    "p",
                    [LeafNode(None, "no attribution")]
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "first item")]),
                        ParentNode("li", [LeafNode(None, "second item")])
                    ]
                ),
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode(None, "first thing")]),
                        ParentNode("li", [LeafNode(None, "second thing")])
                    ]
                )
            ]
        )
        self.assertEqual(
            markdown_to_html_node(markdown),
            div_node
        )

if __name__ == "__main__":
    unittest.main()
