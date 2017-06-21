# -*- coding: utf-8 -*-
import requests
import xml
import json
from requests.auth import HTTPBasicAuth
import urllib.request
from credentials import user,pw
from xml.etree import ElementTree

def get_slugline(dpa_id_link):
    url="https://pipette.dpa-newslab.com/pipette/api/doc-raw/%s" % dpa_id_link


    response=requests.get(url, auth=HTTPBasicAuth(user, pw))
    text=str(response.content,"utf-8")
    root=ElementTree.fromstring(text)
    
    
    # slugline=root.findall(".//{http://iptc.org/std/nar/2006-10-01/}slugline//text()")
    
    slugline=root.find(".//{http://iptc.org/std/nar/2006-10-01/}slugline").text
   
    return(slugline)



if __name__ == "__main__" :
    print(get_slugline("urn:newsml:dpa.com:20090101:170221-99-370286"))