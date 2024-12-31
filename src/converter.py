from textnode import TextType, TextNode
from splitter import split_nodes_image, split_nodes_link, split_nodes_delimiter

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    split_on_images = split_nodes_image(nodes)
    split_on_links = split_nodes_link(split_on_images)
    bolded_nodes = split_nodes_delimiter(split_on_links, "**", TextType.BOLD)
    italicized_nodes = split_nodes_delimiter(bolded_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(italicized_nodes, "`", TextType.CODE)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block.lstrip("\n")
        block.strip()
        if block != "":
            new_blocks.append(block)
    return new_blocks