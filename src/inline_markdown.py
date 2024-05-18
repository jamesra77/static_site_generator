from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_img,
    text_type_link,
)

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    # iterate over old nodes
    # if old node is of text_type text, split it
    # else, add it to the returned list of new text nodes
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.extend([node])
            continue # no need to apply the rest of the logic to node

        texts = node.text.split(delimiter)
        if len(texts) % 2 == 0:
            print(node)
            raise Exception(f"invalid markdown syntax: unmatched instance of delimiter: {delimiter} found near {texts[0]} and {texts[1]}")

        split_nodes = []
        for i in range(len(texts)):
            if texts[i] == "":
                continue
            # first attempt this conditional was checking for texts that started or ended with " "
            if i % 2 == 0:
                split_nodes.append(TextNode(texts[i], text_type_text))
            else:
                split_nodes.append(TextNode(texts[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            parts = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown - image section not properly closed")
            if parts[0] != "":
                new_nodes.append(
                    TextNode(parts[0], text_type_text)
                )
            new_nodes.append(TextNode(image[0], text_type_img, image[1]))
            original_text = parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    # lets do this one iteratively instead of recursively
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:
            parts = original_text.split(f"[{link[0]}]({link[1]})", 1)
            # again, don't think this check is needed but w/e - willing to be wrong
            if len(parts) != 2:
                raise ValueError("invalid markdown - link section isn't closed")

            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))

            # if parts[0] == "" or parts[1] == "":
            #     new_nodes.append(
            #         TextNode(link[0], text_type_link, link[1])
            #     )
            # else:
            #     new_nodes.extend(
            #         [
            #             TextNode(parts[0], text_type_text),
            #             TextNode(link[0], text_type_link, link[1])
            #         ]
            #     )
            original_text = parts[1]
            # if len(extract_markdown_links(original_text)) == 0:
            #     new_nodes.append(TextNode(original_text, text_type_text))
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    nodes = split_nodes_delimiter([node], "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def extract_markdown_images(text):

    # pull out all markdown image strings using regex
    img_regex = r"!\[(.*?)\]\((.*?)\)"
    image_matches = re.findall(img_regex, text)
    return image_matches

def extract_markdown_links(text):
    link_regex = r"\[(.*?)\]\((.*?)\)"
    link_matches = re.findall(link_regex, text)
    return link_matches
