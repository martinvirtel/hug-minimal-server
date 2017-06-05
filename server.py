import os
import sys

import hug

import jinja2
from jinja2 import Markup

_HERE=os.path.split(__file__)[0]

templates=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(_HERE,"templates")))



@hug.static("/static")
def static_dirs() :
    return (os.path.join(_HERE,"static"),)



@hug.get("/hello/{who}/",output=hug.output_format.html,examples="martin?age=48")
@hug.cli()
def index():
    return templates.get_template("index.html").render(**locals())
def hello(age : int ,who) :
    """ Ein Gruss """
    age=age+2
    liste=[
            { "name": "Eins"},
            { "name": "Zwei "}
    ]
    return templates.get_template("compare.html").render(**locals())


if __name__=="__main__" :
    hello.interface.cli()


"""
git init .
git remote add origin username@189.14.666.666:/home/ubuntu/workspace/project.git
git add .
git commit -m "Initial commit
"""