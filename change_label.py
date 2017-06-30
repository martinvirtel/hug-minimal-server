#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""since there were some mistakes in the label, this function gets the right label from the wikidata uri"""

import urllib.parse
import urllib.request
import requests
import xml
import dataset






db='sqlite:///nex-analysis.db'
database = dataset.connect(db)
uris=list(database.query("select uri from entity"))
entity_db=database["entity"]
for uri in uris:
    try:
        if uri["uri"]!= "" or uri["uri"]== None : 
            url= "".join(("https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=PREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%20%0APREFIX%20wd%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fentity%2F%3E%20%0Aselect%20%20*%0Awhere%20%7B%0A%20%20%20%20%20%20%20%20wd%3A",uri["uri"],"%20rdfs%3Alabel%20%3Flabel%20.%0A%20%20FILTER%20(langMatches(%20lang(%3Flabel)%2C%20%22DE%22%20)%20)%0A%20%20%20%20%20%20%7D%20%0ALIMIT%201"))
            response = urllib.request.urlopen(url)
            text=response.read()
            text=text.decode("utf-8")
            start=text.find("<literal xml:lang='de'>")
            length=23
            if start<0:
                start=text.find("<literal xml:lang='de-ch'>")
                length=26
            if start<0:
                start=text.find("<literal xml:lang='de-at'>")
                length=26
            end=text.find("</literal>")
            label=text[start+length:end]
            #print(label)
           
            
        
        if start > 1:
            print(label)
            entity_db.update(dict(
                            label=label,
                      uri=uri["uri"]
                      ),["uri"])
        else:
            print("no label found")
    except TypeError:
        print("TypeError")
print("Final: ",x)