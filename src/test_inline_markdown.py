import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_img,
    text_type_link,
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_text(self):
        node = TextNode("this text node has a `code block` in it, actually it has `two`", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("this text node has a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" in it, actually it has ", text_type_text),
                TextNode("two", text_type_code)
            ]
        )

    def test_bold_text(self):
        node = TextNode("this text has some **bold** text", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("this text has some ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" text", text_type_text)
            ]
        )

    def test_italic_text(self):
        node = TextNode("this text has some *italic* text", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("this text has some ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode( " text", text_type_text)
            ]
        )

    def test_multiple_code_texts(self):
        node1 = TextNode("this text has a `code` block in it", text_type_text)
        node2 = TextNode("this text has a different `code block` in it", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "`", text_type_code),
            [
                TextNode("this text has a ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" block in it", text_type_text),
                TextNode("this text has a different ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" in it", text_type_text)
            ]
        )

    def test_non_text_node(self):
        node1 = TextNode("*this whole thing is italic text*", text_type_italic)
        node2 = TextNode("only one *word* here is italic", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "*", text_type_italic),
            [
                TextNode("*this whole thing is italic text*", text_type_italic),
                TextNode("only one ", text_type_text),
                TextNode("word", text_type_italic),
                TextNode(" here is italic", text_type_text)
            ]
        )

class TestExtractMarkDownImages(unittest.TestCase):
    def test_extract_one_markdown_image(self):
        text = "hello world! i'm a computah look at me ![a pic of me](https://securewebsite.com/img/computah.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("a pic of me", "https://securewebsite.com/img/computah.png")]
        )

    def text_extract_multiple_markdown_images(self):
        text = "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        )

class TestExtractMarkDownLinks(unittest.TestCase):
    def test_extract_one_markdown_link(self):
        text = "this text has [one](https://google.com/LMAO) link in it"
        self.assertEqual(
            extract_markdown_links(text),
            [("one", "https://google.com/LMAO")]
        )

    def test_extract_multiple_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        )

class TestSplitNodesImageAndLink(unittest.TestCase):
    def test_split_one_image(self):
        text = "this text has precisely one image: ![an image](https://www.image.com/img/imglol.png), that was it haha"
        node = TextNode(text, text_type_text)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("this text has precisely one image: ", text_type_text),
                TextNode("an image", text_type_img, "https://www.image.com/img/imglol.png"),
                TextNode(", that was it haha", text_type_text)
            ]
        )

    def test_split_two_images_one_node(self):
        text = "this text has 2 images one here: ![first image lol](https://www.image.com/img/img1.png) - and here's the other: ![second image, heh](https://www.image.com/img/img2.jpg); nice very cool images"
        node = TextNode(text, text_type_text)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("this text has 2 images one here: ", text_type_text),
                TextNode("first image lol", text_type_img, "https://www.image.com/img/img1.png"),
                TextNode(" - and here's the other: ", text_type_text),
                TextNode("second image, heh", text_type_img, "https://www.image.com/img/img2.jpg"),
                TextNode("; nice very cool images", text_type_text)
            ]
        )

    def test_split_multiple_nodes_one_image(self):
        node1 = TextNode("a normal text node", text_type_text)
        node2 = TextNode("this text has precisely one image: ![an image](https://www.image.com/img/imglol.png), that was it haha", text_type_text)
        self.assertEqual(
            split_nodes_image([node1, node2]),
            [
                TextNode("a normal text node", text_type_text),
                TextNode("this text has precisely one image: ", text_type_text),
                TextNode("an image", text_type_img, "https://www.image.com/img/imglol.png"),
                TextNode(", that was it haha", text_type_text)
            ]
        )

    def test_split_multiple_nodes_multiple_images(self):
        node1 = TextNode("a normal text node", text_type_text)
        node2 = TextNode("this text has precisely one image: ![an image](https://www.image.com/img/imglol.png), that was it haha", text_type_text)

        text = "this text has 2 images one here: ![first image lol](https://www.image.com/img/img1.png) - and here's the other: ![second image, heh](https://www.image.com/img/img2.jpg); nice very cool images"
        node3 = TextNode(text, text_type_text)

        self.assertEqual(
            split_nodes_image([node1, node2, node3]),
            [
                TextNode("a normal text node", text_type_text),
                TextNode("this text has precisely one image: ", text_type_text),
                TextNode("an image", text_type_img, "https://www.image.com/img/imglol.png"),
                TextNode(", that was it haha", text_type_text),
                TextNode("this text has 2 images one here: ", text_type_text),
                TextNode("first image lol", text_type_img, "https://www.image.com/img/img1.png"),
                TextNode(" - and here's the other: ", text_type_text),
                TextNode("second image, heh", text_type_img, "https://www.image.com/img/img2.jpg"),
                TextNode("; nice very cool images", text_type_text)
            ]
        )

    def test_split_nodes_image_at_front(self):
        node = TextNode("![first thing in text](https://www.frontrunner.com/images/img.png) the first thing here is the image", text_type_text)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("first thing in text", text_type_img, "https://www.frontrunner.com/images/img.png"),
                TextNode(" the first thing here is the image", text_type_text),
            ]
        )

    def test_split_nodes_image_at_end(self):
        node = TextNode("in this one, the image comes at the end ![latter day image](https://www.caboose.com/img/buttslol.png)", text_type_text)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("in this one, the image comes at the end ", text_type_text),
                TextNode("latter day image", text_type_img, "https://www.caboose.com/img/buttslol.png"),
            ]
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text)
            ]
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_all_node_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_img, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev")
            ]
        )

if __name__ =="__main__":

    unittest.main()
