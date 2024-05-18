from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_to_heading,
    markdown_to_html_node,
    block_type_heading,
    block_type_paragraph,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)
import os, shutil, re
from pathlib import Path

def main():
    cwd = os.getcwd()
    copy_dir(f"{cwd}/static")
    generate_pages_recursive("content", "template.html", "public")

def copy_dir(dir, dest=f"{os.getcwd()}/public", rmtree=True):
    # call shutil.rmtree() on public/ dir before anything else (idempotence)
    # set rmtree parameter to True for first function call, all else False
    if rmtree and os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    # if input dir does not exist, then raise an exception
    if not os.path.exists(dir):
        raise ValueError(f"directory {dir} does not exist")

    # if input dir is a regular file, then raise an exception
    if os.path.isfile(dir):
        raise ValueError(f"path {dir} is a regular filepath, it must be a directory")

    # walk the files in the current dir
    files = os.listdir(dir)
    for file in files:
        filepath = os.path.join(dir, file)
        # if the filepath is a regular file, copy it to new dir
        if os.path.isfile(filepath):
            shutil.copy(filepath, dest)
        # if the filepath is a dir, keep recursing
        else:
            next_dest = os.path.join(dest, file)
            copy_dir(filepath, next_dest, rmtree=False)

def extract_title(markdown):
    # need to test this
    child_blocks = markdown_to_blocks(markdown)
    hash_pattern = re.compile(r"#*")
    for block in child_blocks:
        hashes = hash_pattern.match(block).group()
        if len(hashes) == 1:
            title = block.lstrip("# ")
            return title
    raise ValueError("invalid markdown syntax: must contain at least one h1 block")

def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} and placing in {dest_path} using {template_path}")

    # read markdown from from_path
    with open(from_path) as f:
        markdown = f.read()

    # open template
    with open(template_path) as f:
        template = f.read()

    # generate HTML and capture title from markdown
    outer_html_node = markdown_to_html_node(markdown)
    html_content = outer_html_node.to_html()
    title = extract_title(markdown)

    # replace template params with title and HTML content
    html_doc = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # TODO: write doc to dest_path, probably need to make some dirs
    dest = os.path.join(dest_path, "index.html")
    with open (dest, "w") as f:
        f.write(html_doc)

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    # walk the dirs in content_dir_path to to find the index.md's
    files = os.listdir(content_dir_path)
    for file in files:
        content_path = Path(content_dir_path, file)
        print(content_path)
        if os.path.isfile(content_path) and file == "index.md":
            dest_path = Path(dest_dir_path)
            print(dest_path)
            generate_page(content_path, template_path, dest_path)
        else:
            dest_path = Path(dest_dir_path, file)
            print(dest_path)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(content_path, template_path, dest_path)



main()
