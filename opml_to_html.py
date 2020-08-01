from base_html.copy_dependancies import cd_main
from base_html.app import app_main
import sys, os

if __name__ == "__main__":
    try:
        if sys.argv[1] and os.path.exists(sys.argv[1]):
            cd_main(sys.argv[1])
            app_main(sys.argv[1])
        else:
            print("Path does not exist. Check whether valid .opml absolute path is passed")
    except IndexError:
        print("Pass .opml file as follows --->  python opml_to_html.py <absolute_path_of_opml>")





