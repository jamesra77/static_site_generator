from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_img = "image"

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_img:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise Exception(f"{text_node.text_type} is not a valid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    # iterate over old nodes
    # if old node is of text_type text, split it
    # else, add it to the returned list of new text nodes
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)

        texts = node.text.split(delimiter)
        if len(texts) % 2 == 0:
            raise Exception(f"invalid markdown syntax: unmatched instance of delimiter: {delimiter} found")

        target_nodes = []
        # for text in texts:
        #     if text.startswith(" ") or text.endswith(" "):
        #         target_nodes.append(TextNode(text, text_type_text))
        #     elif text != "":
        #         target_nodes.append(TextNode(text, text_type))
        for i in range(len(texts)):
            if texts[i] == "":
                continue
            if i % 2 == 0:
                target_nodes.append(TextNode(texts[i], text_type_text))
            else:
                target_nodes.append(TextNode(texts[i], text_type))

        new_nodes.extend(target_nodes)

    return new_nodes
