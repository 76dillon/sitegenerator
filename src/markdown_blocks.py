from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "unordered_list"
    ULIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH
                

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block) #Identify the block type
        #Quote
        if block_type == BlockType.QUOTE:
            quote_node = parse_quote_block(block)
            html_nodes.append(quote_node)
        #Unordered List 
        elif block_type == BlockType.ULIST:
            ulist_node = parse_ulist_block(block)
            html_nodes.append(ulist_node)
        #Ordered List
        elif block_type == BlockType.OLIST:
            olist_node = parse_olist_block(block)
            html_nodes.append(olist_node)
        #Code
        elif block_type == BlockType.CODE:
            code_node = parse_code_block(block)
            html_nodes.append(code_node)
        #Paragraph
        elif block_type == BlockType.PARAGRAPH:
            paragraph_node = parse_paragraph_block(block)
            html_nodes.append(paragraph_node)
        #Heading
        elif block_type == BlockType.HEADING:
            heading_node = parse_heading_block(block)
            html_nodes.append(heading_node)
        else: 
            raise Exception("Unrecognized block type")
    parent_node = ParentNode("div", children=html_nodes)
    return parent_node

def parse_quote_block(block):
    lines = block.split("\n")
    filtered_lines = []
    for line in lines:
        if line.startswith(">"):
            line = line[1:].strip()
            if line == "":
                continue
            filtered_lines.append(line)
    text = " ".join(filtered_lines)
    children = text_to_children(text)
    quote_node = ParentNode("blockquote", children=children)
    return quote_node

def parse_ulist_block(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_text = line[2:].strip()
        if line_text == "":
            continue
        grandchildren = text_to_children(line_text)
        child = ParentNode("li", children=grandchildren)
        children.append(child)
    ulist_node = ParentNode("ul", children=children)
    return ulist_node

def parse_olist_block(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_text = line[3:].strip()
        if line_text == "":
            continue
        grandchildren = text_to_children(line_text)
        child = ParentNode("li", children=grandchildren)
        children.append(child)
    olist_node = ParentNode("ol", children=children)
    return olist_node

def parse_code_block(block):
    code_text = block[4:-3]
    code_text_node = TextNode(code_text, TextType.CODE)
    child = text_node_to_html_node(code_text_node)
    code_node = ParentNode("pre", children=[child])
    return code_node

def parse_paragraph_block(block):
    lines = block.split("\n")
    text = " ".join(lines).strip()
    children = text_to_children(text)
    paragraph_node = ParentNode("p", children=children)
    return paragraph_node

def parse_heading_block(block):
    lines = block.split("\n")
    level = len(lines[0].split(" ")[0])
    tag = f"h{level}"
    text = lines[0][level+1:].strip()
    children = text_to_children(text)
    heading_node = ParentNode(tag, children=children)
    return heading_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(tn) for tn in text_nodes]
    return html_nodes

def main():
    md = """
This is **bolded** paragrap
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    md2 = """
> This is a
> blockquote block

this is paragraph text

"""
    nodes = markdown_to_html_node(md2)
    html = nodes.to_html()
    print(html)


if __name__ == "__main__":
    main()