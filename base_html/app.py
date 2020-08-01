# Converts the .opml syntax to .html format

import re, shutil, sys, os

div = '<div data-role="collapsible" data-collapsed-icon="carat-d" data-expanded-icon="carat-u" data-mini="true"><h1>'

image_format = '''
<p id="demo" onmouseover="hoverin('{0}')" onmouseout="hoverout('{0}')"> 
{1} <input type="image" id="expand" alt="expand_btn" src="expand-white.png" onclick="buttonclick(event, '{0}')"> 
<img id="{0}" alt="{1}" src="{2}" onclick="myFunction(event, '{0}')" /> 
</p>'''

def external_link(x):
    is_external_link_pattern = re.compile(r'\[.+?\]\(\S+\.\w{2,6}\S*\)')
    is_image_pattern = re.compile(r'!\[.+?\]\(\S+\.\w{2,6}\S*?\)')
    external_link_pattern = re.compile(r"\(.*\)")                               # Pattern to isolate external link
    external_caption_pattern = re.compile(r"\[.*\]")                            # Pattern to isolate caption
    
    is_image = is_image_pattern.findall(x)

    if is_image:
        for i in range(len(is_image)):
            image_link = external_link_pattern.search(is_image[i])             
            image_caption = external_caption_pattern.search(is_image[i])

            link_of_image = image_link.group(0).strip("\(\)")
            caption_of_image = image_caption.group(0).strip("\[\]")
            x = x.replace(is_image[i], image_format.format(caption_of_image.lower().replace(" ", "_"), caption_of_image, link_of_image))
        
    is_external_link = is_external_link_pattern.findall(x)
    if is_external_link:
        for i in range(len(is_external_link)):
            external_link = external_link_pattern.search(is_external_link[i])             
            external_caption = external_caption_pattern.search(is_external_link[i])

            link = external_link.group(0).strip("\(\)")
            caption = external_caption.group(0).strip("\[\]")
            x = x.replace(is_external_link[i], f'<a href="{link}" target="_blank">{caption}</a>')
            
        return x
    else:
        return x


def beautify(line):
    bold_pattern = re.compile(r'\*\*.*?\*\*')
    italics_pattern = re.compile(r'__.*?__')
    strike_pattern = re.compile(r'~~.*?~~')

    bold_result = bold_pattern.findall(line)
    for bold in bold_result:
        x = bold.strip('*')
        line = line.replace(bold, f'<b>{x}</b>')

    italics_result = italics_pattern.findall(line)
    for italics in italics_result:
        x = italics.strip('_')
        line = line.replace(italics, f'<i>{x}</i>')

    strike_result = strike_pattern.findall(line)
    for strike in strike_result:
        x = strike.strip('~')
        line = line.replace(strike, f'<strike>{x}</strike>')

    return line


def remove_cLabel_and_collapsed(line):
    if "colorLabel" in line:
        pattern = re.compile(r'colorLabel=\".{1}\"')
        cLabel = pattern.search(line).group(0)
        line = line.replace(f' {cLabel}', "")
        return line

    elif "collapsed" in line:
        pattern = re.compile(r'collapsed=\".{4,5}\"')
        cLabel = pattern.search(line).group(0)
        line = line.replace(f' {cLabel}', "")
        return line

    else:
        return line


def remove_last_occurence(line, string):
    line = line.rsplit(string, 1)
    line = "".join(line[0:-1])
    return line


def app_main(opml):
    opml_name = opml.rsplit('\\', 1)[-1].split('.')[0]  # gets the filename of the .opml file

    html_src = os.path.abspath("base_html\\base.html")

    html_dir = html_src.rsplit("\\", 1)[0]
    html_dst = f'{html_dir}\\{opml_name}.html'
    result_dir = html_dir.rsplit("\\", 1)[0]

    shutil.copy(html_src, html_dst)


    with open(opml) as f:
        all_lines = f.readlines()                       # Convert all 'lines from file' into 'list of lines'
        all_lines = [x.strip() for x in all_lines]      # Remove whitespace from either side of the 'line'

        start_from = all_lines.index("<body>")+1        # Ignore sentences till '<body>'
        number_of_lines = len(all_lines)

        with open(html_dst, "a") as out:

            output_lines = []

            for i in range(start_from, number_of_lines):  

                line = external_link(f'{all_lines[i]}') 
                line = beautify(line)
                line = remove_cLabel_and_collapsed(line)

                if line.endswith("\">"):                                        # Check whether line is a collapsible header
                    content = line.split(sep="text=\"")[1]                      # To get the string from the opml tag
                    if line == all_lines[i] or line.endswith('">'):
                        content = remove_last_occurence(content, '">') 
                    if "$$" in content:
                        content = content.replace("$$", "$")                    # Replace all "$$" into "$"
                    output_lines.append(f'{div}{content}</h1>\n')

                elif line.endswith("\"/>"):                                     # Check whether line is inside collapsible
                    content2 = line.split(sep="text=\"")[1]                     # To get the string from the opml tag
                    if line == all_lines[i] or line.endswith('"/>'):
                        content2 = content2.replace('"/>', "")
                    if "$$" in content2:
                        content2 = content2.replace("$$", "$")                  # Replace all "$$" into "$"
                    output_lines.append(f'<p>{content2}</p>\n')

                elif line=="</outline>":                                        # Check whether line is end tag of colapsible
                    output_lines.append(f'</div>')

                elif line=='</body>':
                    output_lines.append(line)

                elif line=='</opml>':
                    output_lines.append("<script src='main.js'></script></html>")

                else:
                    print("UNKNOWN CASE")

            out.writelines(output_lines)

    shutil.copy(html_dst, result_dir + "\\" + opml_name)
    os.remove(html_dst)
 

