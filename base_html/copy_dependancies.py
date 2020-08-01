# Copies all folders and files on which the output .html depends on, like "katex", "jquery-mobile", etc to the output folder named after the input .opml file

import os, shutil

def cd_main(opml_name):
    opml_name = opml_name.rsplit('\\', 1)[-1].split('.')[0]             # Gets the filename of the .opml file
    
    katex = os.path.abspath("katex")
    jquery_mobile = os.path.abspath("jquery-mobile")
    expand_image = os.path.abspath("base_html\\expand-white.png")
    source_css = os.path.abspath("base_html\\source.css")
    main_js = os.path.abspath("base_html\\main.js")

    katex_jquerymob = [katex, jquery_mobile]                            # list of directories

    css_js_image = [source_css, main_js, expand_image]                  # list of files

    try:
        os.mkdir(opml_name)                                       # create an empty output directory
    except:
        pass

    for path in katex_jquerymob:
        folder_name = path.split('\\')[-1]                              # Get directory name from path
        
        try:
            shutil.copytree(path, f"{opml_name}\\{folder_name}")        # Copy directory to output directory
        except FileExistsError:
            shutil.rmtree(f"{opml_name}\\{folder_name}")                # Remove directory if exists ...
            shutil.copytree(path, f"{opml_name}\\{folder_name}")        # ... and copy it to output directory again

    for files in css_js_image:
        shutil.copy(files, f"{opml_name}")                              # Copy all files to output directory

