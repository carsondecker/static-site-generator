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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_str = node.text
        remaining_extracted_images = extract_markdown_images(remaining_str)
        while remaining_extracted_images != []:
            current_image_tuple = remaining_extracted_images.pop(0)
            markdown_image = f"![{current_image_tuple[0]}]({current_image_tuple[1]})"
            image_index = remaining_str.find(markdown_image)
            new_nodes.append(TextNode(remaining_str[:image_index], node.text_type))
            new_nodes.append(TextNode(current_image_tuple[0], TextType.IMAGE, current_image_tuple[1]))
            remaining_str = remaining_str[image_index + len(markdown_image):]
        if remaining_str != "":
            new_nodes.append(TextNode(remaining_str, node.text_type))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_str = node.text
        remaining_extracted_links = extract_markdown_links(remaining_str)
        while remaining_extracted_links != []:
            current_link_tuple = remaining_extracted_links.pop(0)
            markdown_link = f"[{current_link_tuple[0]}]({current_link_tuple[1]})"
            link_index = remaining_str.find(markdown_link)
            new_nodes.append(TextNode(remaining_str[:link_index], node.text_type))
            new_nodes.append(TextNode(current_link_tuple[0], TextType.LINK, current_link_tuple[1]))
            remaining_str = remaining_str[link_index + len(markdown_link):]
        if remaining_str != "":
            new_nodes.append(TextNode(remaining_str, node.text_type))
    return new_nodes

def extract_markdown_images(text):
    extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_images

def extract_markdown_links(text):
    extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links