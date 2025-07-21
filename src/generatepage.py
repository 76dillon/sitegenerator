import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if len(line) > 1:
            if line[0] == "#" and line[1] != "#":
                return line[1:].strip()
    raise Exception("No title found in markdown file")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    #Verify if destination path exists. If not, create it
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    items = os.listdir(dir_path_content)
    for item in items:
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(from_path) and len(item) > 4:
            #Check if it's a markdown file
            if item[-3:] ==  ".md":
                dest_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #Making directories in destination if they don't exist
    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    #Retrieve contents of md file 
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    #Extract title
    title = extract_title(markdown_content)
    
    #Use html template to generate the full html string for the dest_path file
    with open(template_path, "r") as f:
        full_html = f.read()
    
    #Relace {{ Title }} and {{ Content }} in template with the actual title and html contents
    full_html = full_html.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

