import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Invalid syntax, missing a closing delimiter.")
        new_nodes = []
        for i in range(0, len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(split_text[i], text_type))   
            else:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
        nodes.extend(new_nodes)
    return nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        new_nodes = []
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            nodes.append(node)
            continue
        node_text = node.text
        for i in range(0, len(matches)):
            image_alt = matches[i][0]
            image_link = matches[i][1]
            sections = node_text.split(f"![{image_alt}]({image_link})", 1)
            node_text = sections[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        if sections[1] != "":
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
        nodes.extend(new_nodes)
    return nodes
        
def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        new_nodes = []
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            nodes.append(node)
            continue
        node_text = node.text
        for i in range(0, len(matches)):
            link_alt = matches[i][0]
            link_url = matches[i][1]
            sections = node_text.split(f"[{link_alt}]({link_url})", 1)
            node_text = sections[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
        if sections[1] != "":
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
        nodes.extend(new_nodes)
    return nodes

def text_to_textnodes(text):
    start_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([start_node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
