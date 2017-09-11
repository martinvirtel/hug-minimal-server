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


# Sessions





@hug.static("/static")
def static_dirs() :
    return (os.path.join(_HERE,"static"),)



@hug.get("/hello/{who}/",output=hug.output_format.html)
@hug.cli()
def hello(request, age : int ,who=None) :
    session=request.context["session"]
    session["counter"]=session.get("counter",0)+1
    return templates.get_template("hello.html").render(**locals())


# Set up session store

from hug.middleware import SessionMiddleware
from hug.store import InMemoryStore

session_store = InMemoryStore()
__hug__.http.add_middleware(SessionMiddleware(session_store, cookie_name='session',cookie_secure=False))


if __name__=="__main__" :
   api(os.path.split(__file__)[1]).cli()
