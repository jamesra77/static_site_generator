from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import *
import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    # # fp implementation
    # blocks = list(filter(lambda b: b != "", map(lambda b: b.strip(), markdown.split("\n\n"))))
    # return blocks

    # procedural implementation
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks

def block_to_block_type(block):
    if block.startswith("#"):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif block.startswith(">"):
        return block_type_quote
    elif block.startswith(("- ", "* ")):
        return block_type_unordered_list
    elif is_ordered_list(block):
        return block_type_ordered_list
    else:
        return block_type_paragraph

def is_ordered_list(block):
    items = block.split("\n")
    i = 0
    while i < len(items):
        item = items[i]
        if not item.startswith(f"{i + 1}. "):
            return False
        i += 1
    return True

def block_to_paragraph(block):
    lines = block.split("\n")
    text = " ".join(lines)

    child_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)
    return ParentNode(
        "p",
        child_nodes
    )

def block_to_heading(block):
    # need to consider number of #'s for heading type (h1, h2, h3, etc)
    hash_pattern = re.compile(r"#*")
    hashes = hash_pattern.match(block).group()
    tag = ""
    if len(hashes) == 1:
        tag = "h1"
    elif len(hashes) == 2:
        tag = "h2"
    elif len(hashes) == 3:
        tag = "h3"
    elif len(hashes) == 4:
        tag = "h4"
    elif len(hashes) == 5:
        tag = "h5"
    elif len(hashes) == 6:
        tag = "h6"
    else:
        raise ValueError("invalid heading type")

    child_nodes = []
    text_nodes = text_to_textnodes(block.lstrip("# ")) # remove leading #'s, do this in other function?
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)

    return ParentNode(
        tag,
        child_nodes
    )

def block_to_code(block):
    # return a <pre> ParentNode, and it only has one child node
    # namely, the <code> node (which is a ParentNode itself)
    # assuming a code block node can have inline children, seems weird though
    child_nodes = []
    code_lines = block.strip("`").split("\n")
    code_text = " ".join(code_lines)
    text_nodes = text_to_textnodes(code_text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)
    code_block_node = ParentNode(
        "code",
        child_nodes
    )
    return ParentNode(
        "pre",
        [code_block_node]
    )


def block_to_quote(block):
    # seems pretty simple, just needs child inline nodes and <blockquote> tag
    # each line is prepended with a "> ", need to handle this
    quote_lines = block.split("\n")

    stripped_lines = []
    for quote_line in quote_lines:
        no_arrow_line = quote_line.lstrip("> ")
        stripped_lines.append(no_arrow_line)
    no_arrows_quote  = " ".join(stripped_lines)

    text_nodes = text_to_textnodes(no_arrows_quote)
    child_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)

    return ParentNode(
        "blockquote",
        child_nodes
    )

def block_to_unordered_list(block):
    # need to handle child nodes by giving them <li> tags
    # maybe similar logic to code block funciton
    list_items = block.split("\n")

    child_nodes = []
    for list_item in list_items:
        text_nodes = text_to_textnodes(list_item[1:].lstrip(" "))

        list_item_nodes = []
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            list_item_nodes.append(html_node)
        child_nodes.append(
            ParentNode(
                "li",
                list_item_nodes
            )
        )
    return ParentNode(
        "ul",
        child_nodes
    )

def block_to_ordered_list(block):
    # virtually identical to unordered list function?
    list_items = block.split("\n")
    ol_pattern = re.compile(r"\d+\. ")

    child_nodes = []
    for list_item in list_items:
        text_nodes = text_to_textnodes(re.sub(ol_pattern, "", list_item))

        list_item_nodes = []
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            list_item_nodes.append(html_node)
        child_nodes.append(
            ParentNode(
                "li",
                list_item_nodes
            )
        )
    return ParentNode(
        "ol",
        child_nodes
    )

def markdown_to_html_node(markdown):
    child_blocks = markdown_to_blocks(markdown)

    # need to handle stripping the relevant leading and trailing characters
    # either here or block_to_xxx functions
    child_nodes = []
    for child_block in child_blocks:
        block_type = block_to_block_type(child_block)
        if block_type == block_type_paragraph:
            child_nodes.append(block_to_paragraph(child_block))
        elif block_type == block_type_heading:
            child_nodes.append(block_to_heading(child_block))
        elif block_type == block_type_quote:
            child_nodes.append(block_to_quote(child_block))
        elif block_type == block_type_code:
            child_nodes.append(block_to_code(child_block))
        elif block_type == block_type_unordered_list:
            child_nodes.append(block_to_unordered_list(child_block))
        elif block_type == block_type_ordered_list:
            child_nodes.append(block_to_ordered_list(child_block))
        else:
            raise ValueError(f"{block_type} is not a valid block type")

    return ParentNode(
        "div",
        child_nodes
    )
