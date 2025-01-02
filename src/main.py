import os
import shutil
from textnode import *

def main():
    copy_static_to_public()

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

if __name__ == "__main__":
    main()