import os, shutil
from blocklogic import markdown_to_html_node, extract_title
from pathlib import Path

def get_file_paths():
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(current_dir)

    dst_dir = os.path.join(root_dir, "public")
    src_dir = os.path.join(root_dir, "static")
    return dst_dir, src_dir

def clear_dst_dir(dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    os.mkdir(dst_dir)
    return f"{dst_dir} created blank"

def copy_static(src_dir, dst_dir):
    # Get list of all items in source directory
    items = os.listdir(src_dir)
    
    # For each item in the directory
    for item in items:
        # Create full paths
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        
        if os.path.isfile(src_path):
                print(f"Copying {src_path} to {dst_path}")
                shutil.copy(src_path, dst_path)
        else:
            print("found directory, making duplicate")
            os.mkdir(dst_path)
            copy_static(src_path, dst_path)
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as content_file:
        content_data = content_file.read()
    with open(template_path, "r") as template_file:
        template_data = template_file.read()
    content_html = markdown_to_html_node(content_data)
    content_html = content_html.to_html()
    title = extract_title(content_data)
    template_data = template_data.replace("{{ Title }}", title)
    template_data = template_data.replace("{{ Content }}", content_html)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as output_file:
        output_file.write(template_data)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)

    for item in items:
        src_path = os.path.join(dir_path_content, item)

        if os.path.isfile(src_path) and Path(src_path).suffix == ".md":
            name = Path(src_path).stem
            dst_path = os.path.join(dest_dir_path, name+".html")
            generate_page(src_path, template_path, dst_path)
            continue
        else:
            src_subdir = os.path.join(dir_path_content, item)
            dst_subdir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_subdir, template_path, dst_subdir)