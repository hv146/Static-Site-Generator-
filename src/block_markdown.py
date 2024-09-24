from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.strip("# ") 
    raise Exception("No title")
                
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children


def markdown_to_blocks(documnet):

    blocks = documnet.split("\n\n")
    filter_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filter_blocks.append(block)

    return filter_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ","### ", "#### ", "##### ", "###### ")):
        return block_type_heading

    if len(lines) > 0 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("-"):
                return block_type_paragraph
        return block_type_ulist

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
            return block_type_olist
    return block_type_paragraph


        
def heading_to_html(block):
    levels = 0

    for char in block:
        if char == "#":
            levels += 1
        else: 
            break

    if levels + 1 >= len(block):
        raise ValueError(f"Invalid Heading Level: {levels}")

    text = block[levels + 1:]
    children = text_to_children(text)

    return ParentNode(f"h{levels}", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote")

        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []

    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def code_to_html_node(block):
    if not block.startswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])







