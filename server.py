"""
minimal hug server

"""

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



@hug.get("/hello/{who}/",output=hug.output_format.html)
@hug.cli()
def hello(age : int ,who=None) :
    return templates.get_template("hello.html").render(**locals())


if __name__=="__main__" :
    hug.API(__name__,os.path.split(__file__)[1]).cli()
