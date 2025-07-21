import os
import sys
import shutil

from copystatic import copy_files_recursive
from generatepage import extract_title, generate_page, generate_pages_recursive



dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
#markdown_path = "./content/index.md" #markdown file path
template_path = "./template.html"
dest_path = "./public/index.html"



def main():
    #Delete and recreate empty public directory for copying contents of static
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"


    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    #Recursive call for copying files from static
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    #Generating html page from md file
    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
    


if __name__ == "__main__":
    main()