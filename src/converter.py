import re
from enum import Enum
from textnode import TextType, TextNode
from htmlnode import HTMLNode
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
        block.strip(" \n")
        if block != "":
            new_blocks.append(block)
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    LIST_ITEM = "li"

def block_to_block_type(block):
    split_lines = block.split("\n")
    if re.match(r"^(#{1,6})\s", split_lines[0]):
        return BlockType.HEADING, split_lines[0].find(" ") 
    if len(block) > 6 and block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    if all(line.startswith("> ") for line in split_lines):
        return BlockType.QUOTE
    if all(line.startswith("* ") or line.startswith("- ") for line in split_lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(r"^(\d+)\.\s", line) and int(re.match(r"^(\d+)\.\s", line).group(1)) == i + 1 for i, line in enumerate(split_lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def remove_block_markdown(block, block_type):
    match block_type:
        case BlockType.HEADING:
            first_space_index = block.find(" ")
            return block[first_space_index + 1:]
        case BlockType.CODE:
            return block[3:-3]
        case BlockType.QUOTE:
            line_list = []
            for line in block.splitlines():
                first_space_index = line.find(" ")
                line_list.append(line[first_space_index + 1:])
            return "\n".join(line_list)
        case BlockType.UNORDERED_LIST:
            line_list = []
            for line in block.splitlines():
                first_space_index = line.find(" ")
                line_list.append(line[first_space_index + 1:])
            return "\n".join(line_list)
        case BlockType.ORDERED_LIST:
            line_list = []
            for line in block.splitlines():
                first_space_index = line.find(" ")
                line_list.append(line[first_space_index + 1:])
            return "\n".join(line_list)
        case _:
            return block

def block_to_html_node(block, block_type, headingNum=None):
    if block_type == BlockType.ORDERED_LIST or block_type == BlockType.UNORDERED_LIST:
        list_items = []
        cleaned_block = remove_block_markdown(block, block_type)
        for line in cleaned_block.splitlines():
            list_items.append(block_to_html_node(line, BlockType.LIST_ITEM))
        return HTMLNode(tag=block_type.value, children=list_items)
    textnodes = text_to_textnodes(remove_block_markdown(block, block_type))
    htmlnodes = []
    for textnode in textnodes:
        htmlnodes.append(textnode.text_node_to_html_node())
    if block_type == BlockType.HEADING:
        return HTMLNode(tag=f"h{headingNum}", children=htmlnodes)
    if block_type == BlockType.CODE:
        return HTMLNode(tag="pre", children=[HTMLNode(tag="code", children=htmlnodes)])
    return HTMLNode(tag=block_type.value, children=htmlnodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []
    for block in blocks:
        if isinstance(block_to_block_type(block), tuple):
            block_type, headingNum = block_to_block_type(block)
        else:
            block_type = block_to_block_type(block)
            headingNum = None
        htmlnodes.append(block_to_html_node(block, block_type, headingNum))
    return HTMLNode(tag="div", children=htmlnodes)