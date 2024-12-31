import re
from enum import Enum
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
        block.strip(" \n")
        if block != "":
            new_blocks.append(block)
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h1"
    CODE = "code"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def block_to_block_type(block):
    split_lines = block.split("\n")
    if re.match(r"^(#{1,6})\s", split_lines[0]):
        return BlockType.HEADING
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
            return block.replace("> ", "")
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