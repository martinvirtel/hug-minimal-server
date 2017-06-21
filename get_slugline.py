# -*- coding: utf-8 -*-
import requests
import xml
import json
from requests.auth import HTTPBasicAuth
import urllib.request
from credentials import user,pw
from xml.etree import ElementTree

def get_slugline(dpa_id_link):
    url="https://pipette.dpa-newslab.com/pipette/api/doc-raw/%s"%dpa_id_link


    response=requests.get(url, auth=HTTPBasicAuth(user, pw))
    text=str(response.content,"utf-8")
    #x=json.loads(text)

    dpa_keywords=[]


    # for x in range(1,10):
    #     start_keyword=text.find('<keyword rank="%i">'%x)
    #     end_keyword=text[start_keyword:].find("</keyword>")
    #     print(start_keyword,end_keyword)
    #     if start_keyword != -1 and end_keyword != -1:
    #         keyword=text[start_keyword+18:end_keyword+start_keyword]
    #         keyword=str(keyword)
    #         dpa_keywords.append(keyword)

    start_custom=text.find('separator="/">')
    end_custom=text.find("</slugline>")
    slugline=[]
    custom_text=text[start_custom+14:end_custom]
    custom_text=str(custom_text)
    slugline=custom_text.split("/")

    return(slugline)

