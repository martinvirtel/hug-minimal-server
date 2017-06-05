import os
import sys

from get_text import get_text
from mark_text import mark_text
import hug
import jinja2
from jinja2 import Markup

_HERE=os.path.split(__file__)[0]

templates=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(_HERE,"templates")))



@hug.static("/static")
def static_dirs() :
    return (os.path.join(_HERE,"static"),)


@hug.get("/nex/start",output=hug.output_format.html,examples="nex/start?start=0&end=20")
@hug.cli()
def index(start : int = 0, limit : int=20):
    from index import index
    output_index=index(start, limit,)
    pages=output_index["pages"]
    page=(int(start/20)+1)
    pre_position="start=%s&limit=20"%str(start-20)
    post_position="start=%s&limit=20"%str(start+20)
    from get_next import get_next
    xy="urn:newsml:dpa.com:20090101:170221-99-370286/3"
    # xy="urn:newsml:dpa.com:20090101:170307-99-561039/3"
    next_dpa_id=get_next(xy)
    return templates.get_template("index.html").render(**locals())
    
# def show_index(start: int = 0, search: str = "", order: str = "title") :
#   --- datenbankabfrage sql: sort by .... ; "Blaettern" mit sql limit .....
# count() group by 

# dict(a="ambiverse",d="dandelion",t="txtwerk")
@hug.get("/nex/{dpa_id}/{tool_code}",output=hug.output_format.html,examples="urn:newsml:dpa.com:20090101:170226-99-442102/2/")
@hug.cli()
def compare(dpa_id : str ,tool_code : str) :
    tools=[]
    tool_dict={
        "a":"ambiverse",
        "d":"dandelion",
        "t":"txtwerk"
        # "z":"textrazor",
        # "y":"aylien",
        # "s":"semantria"
        }
    layouts = [ "", "col-md-6", "col-md-6", "col-md-4","col-md-3","col-md-2","col-md-2","col-md-2"]
    column_class=layouts[ len(tool_code) ]
    print(column_class)
    if tool_code == "all":
        for tool in tool_dict:
            tools.append(tool_dict[tool])
    else:
        for character in tool_code :
            try:
                tool=tool_dict[character]
                tools.append(tool)
            except KeyError:
                xxx="nothing"
    
    dpa_id_link=dpa_id[:-3]
    text_output=get_text(dpa_id)
    l=["a","b","c"]
    output_object=mark_text(text_output,tools)
    print(output_object)
    from get_next import get_next
    next_dpa_id=get_next(dpa_id)
    return templates.get_template("compare.html").render(**locals())
    #return templates.get_template("hello.html").render(**locals())

@hug.get("/try",output=hug.output_format.html,examples="try")
@hug.cli()
def index(start : int = 0, limit : int=20):
    return templates.get_template("try.html").render(**locals())
    
    
    
if __name__=="__main__" :
    compare.interface.cli()
    index.interface.cli()


"""
git init .
git remote add origin username@189.14.666.666:/home/ubuntu/workspace/project.git
git add .
git commit -m "Initial commit"
"""