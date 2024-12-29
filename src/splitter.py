import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        remaining_str = node.text
        while remaining_str != "":
            first_location = remaining_str.find(delimiter)
            if first_location == -1:
                new_nodes.append(TextNode(remaining_str, TextType.TEXT))
                remaining_str = ""
                break
            if first_location != 0:
                new_nodes.append(TextNode(remaining_str[:first_location], TextType.TEXT))
            remaining_str = remaining_str[first_location + len(delimiter):]
            second_location = remaining_str.find(delimiter)
            if second_location == -1:
                raise Exception(f"Missing matching delimiter \"{delimiter}\"") 
            if second_location != 0:
                new_nodes.append(TextNode(remaining_str[:second_location], text_type))
            remaining_str = remaining_str[second_location + len(delimiter):]
    return new_nodes

def extract_markdown_images(text):
    extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_images

def extract_markdown_links(text):
    extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links