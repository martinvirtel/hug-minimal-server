import os
import sys

from get_text import get_text
from mark_text import mark_text
from overlap import overlap
import hug
import jinja2
from jinja2 import Markup

_HERE=os.path.split(__file__)[0]

PREFIX="/nex-server"

templates=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(_HERE,"templates")))

templates.globals=globals=dict(PREFIX=PREFIX)

api=hug.http(prefixes=PREFIX)

@hug.static("{PREFIX}/static".format(**globals))
def static_dirs() :
    return (os.path.join(_HERE,"static"),)


@api.get("/nex/start",output=hug.output_format.html,examples="nex/start?start=0&end=20")
@hug.cli()
def index(start : int = 0, limit : int=20):
    from index import index
    output_index=index(start, limit)
    pages=output_index["pages"]
    page=(int(start/20)+1)
    pre_position="start=%s&limit=20"%str(start-20)
    post_position="start=%s&limit=20"%str(start+20)
    from get_next import get_next
    #xy="urn:newsml:dpa.com:20090101:170221-99-370286/3"
    xy="urn:newsml:dpa.com:20090101:170307-99-561039/3"
    next_dpa_id=get_next(xy)
    return templates.get_template("index.html").render(**locals())

# def show_index(start: int = 0, search: str = "", order: str = "title") :
#   --- datenbankabfrage sql: sort by .... ; "Blaettern" mit sql limit .....
# count() group by

# dict(a="ambiverse",d="dandelion",t="txtwerk")
@api.get("/nex/{dpa_id}/{tool_code}",output=hug.output_format.html,examples="/nex/urn:newsml:dpa.com:20090101:170226-99-442102/ad/")
@hug.cli()
def compare(dpa_id : str ,tool_code : str) :
    tools=[]
    tool_dict={
        "a":"ambiverse",
        "d":"dandelion",
        "t":"txtwerk",
        "z":"textrazor",
        "y":"aylien"
        # "s":"semantria"
        }
    layouts = [ "", "col-md-6", "col-md-6", "col-md-4","col-md-3","col-md-2","col-md-2","col-md-2"]
    column_class=layouts[ len(tool_code) ]
    print(len(tool_code))
    print(column_class)
    if tool_code == "all":
        for tool in tool_dict:
            tools.append(tool_dict[tool])
            column_class=column_class=layouts[ len(tool_dict) ]
    else:
        for character in tool_code :
            try:
                tool=tool_dict[character]
                tools.append(tool)
            except KeyError:
                xxx="nothing"

    if dpa_id[-3:][0]=="v":
        dpa_id_link=dpa_id[:-3]
    elif dpa_id[-4:][0]=="v":
        dpa_id_link=dpa_id[:-4]
    text_output=get_text(dpa_id)
    #print(text_output)
    l=["a","b","c"]
    output_object=mark_text(text_output,tools)
    #print(output_object[0])
    from get_next import get_next
    next_dpa_id=get_next(dpa_id)
    return templates.get_template("compare.html").render(**locals())
    #return templates.get_template("hello.html").render(**locals())

# @hug.get("/try",output=hug.output_format.html,examples="try")
# @hug.cli()
# def index(start : int = 0, limit : int=20):
#     return templates.get_template("try.html").render(**locals())

@api.get("/nex/{dpa_id}/overlap/{value}",output=hug.output_format.html,examples="/nex/urn:newsml:dpa.com:20090101:170526-99-612882v-2/overlap/3")
@hug.cli()
def overlap(dpa_id : str = "urn:newsml:dpa.com:20090101:170319-99-722478v-2", value : int=3):
    if dpa_id[-3:][0]=="v":
        dpa_id_link=dpa_id[:-3]
    elif dpa_id[-4:][0]=="v":
        dpa_id_link=dpa_id[:-4]
    from overlap import overlap
    output_overlap=overlap(dpa_id,value)
    from get_next import get_next
    next_dpa_id=get_next(dpa_id)
    from get_slugline import get_slugline
    slugline=get_slugline(dpa_id_link)
    return templates.get_template("overlap.html").render(**locals())

@api.get("/nex/{dpa_id}/evaluation",output=hug.output_format.html,examples="/nex/urn:newsml:dpa.com:20090101:170526-99-612882v-2/evaluation")
@hug.cli()
def overlap(dpa_id : str = "urn:newsml:dpa.com:20090101:170319-99-722478v-2"):
    if dpa_id[-3:][0]=="v":
        dpa_id_link=dpa_id[:-3]
    elif dpa_id[-4:][0]=="v":
        dpa_id_link=dpa_id[:-4]
    from evaluation import evaluation
    output_evaluation=evaluation(dpa_id)
    from get_next import get_next
    next_dpa_id=get_next(dpa_id)
    from get_slugline import get_slugline
    slugline=get_slugline(dpa_id_link)
    return templates.get_template("evaluation.html").render(**locals())


if os.environ.get("HOME","").lower() == "/root" :
    @hug.not_found()
    def not_found_handler():
        return "Page Not Found"



if __name__=="__main__" :
    compare.interface.cli()
    index.interface.cli()


"""
git init .
git remote add origin username@189.14.666.666:/home/ubuntu/workspace/project.git
git add .
git commit -m "Initial commit"
"""
