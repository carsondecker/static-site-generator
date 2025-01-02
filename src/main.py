import os
import shutil
from textnode import *
from converter import markdown_to_html_node

def main():
    copy_static_to_public()
    from_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content/")
    template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "template.html")
    dest_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public/")
    generate_pages_recursive(from_path, template_path, dest_path)

def copy_static_to_public():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    start_path = os.path.join(project_dir, "static")
    dest_path = os.path.join(project_dir, "public")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    recursively_copy_tree(start_path, dest_path)
    
def recursively_copy_tree(curr_path, dest_path):
    dir_list = os.listdir(curr_path)
    for item in dir_list:
        item_path = os.path.join(curr_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_path)
        else:
            new_dest_path = os.path.join(dest_path, item)
            os.mkdir(new_dest_path)
            recursively_copy_tree(item_path, new_dest_path)

def extract_title(markdown):
    header = markdown.splitlines()[0].lstrip()
    if header.startswith("# "):
        return header[2:].lstrip()
    raise Exception("No '# ' in markdown for title.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    markdown = ""
    template_page = ""
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    content = markdown_to_html_node(markdown).to_html()
    final_content = template_content.replace("{{ Title }}", extract_title(markdown)).replace("{{ Content }}", content)
    with open(dest_path, "w") as f:
        f.write(final_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            generate_page(item_path, template_path, os.path.join(dest_dir_path, item.replace(".md", ".html")))
        elif not os.path.isfile(item_path):
            new_dest_path = os.path.join(dest_dir_path, item)
            os.mkdir(new_dest_path)
            generate_pages_recursive(item_path, template_path, new_dest_path)

if __name__ == "__main__":
    main()