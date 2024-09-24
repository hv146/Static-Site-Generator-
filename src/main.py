import shutil
import os 
from pathlib import Path
from block_markdown import (markdown_to_html_node, extract_title)
from htmlnode import *

def main():
    copy_contents("/Users/haovu/personalProject/SSG/static", 
                  "/Users/haovu/personalProject/SSG/public")

    generate_page_recursive("/Users/haovu/personalProject/SSG/content",
                  "/Users/haovu/personalProject/SSG/template.html",
                  "/Users/haovu/personalProject/SSG/public"
                  )


def copy_contents(src, dest):
    if not os.path.exists(src):
        raise ValueError("Source path does not exist")
    if not os.path.exists(dest):
        os.mkdir(dest)

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    current_dir = os.listdir(src)

    for node in current_dir:
        current_path = os.path.join(src, node)
        if os.path.isfile(current_path):
            shutil.copy(current_path, dest)
            print(f"Copied {current_path} to {dest}")
        else:
            new_dest = os.path.join(dest, node)
            os.mkdir(new_dest)
            copy_contents(current_path, new_dest)
            
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md_file:
        md_content = md_file.read()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    if not os.path.exists(dest_path.split("/index.html")[0]):
        os.makedirs(dest_path.split("/index.html")[0])

    node = markdown_to_html_node(md_content)
    html = node.to_html()
    title = extract_title(md_content)

    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    with open(dest_path, "w") as html_file:
        html_file.write(template_content)



def generate_page_recursive(dir_path_content, template_path, des_dir_path):
    current_dir = os.listdir(dir_path_content)

    for item in current_dir:
        current_path = os.path.join(dir_path_content, item)
        if os.path.isfile(current_path):
            generate_page(current_path, template_path, des_dir_path + "/" + "index.html")
        else:
            new_des = os.path.join(des_dir_path, item)
            generate_page_recursive(current_path, template_path, new_des)

    



main()


