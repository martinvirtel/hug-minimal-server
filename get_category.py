#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""This functions gives the category 'person','location','organisation' or 'None' from the wikidata uri"""
import urllib.parse
import urllib.request
import requests
import xml
import dataset

session=requests.session()
db='sqlite:///nex-analysis.db'
database = dataset.connect(db)
uris=list(database.query("select uri, rowid, category from entity order by rowid desc"))
entity_db=database["entity"]

for uri_ in uris:
    uri=uri_["uri"]
    category_start=uri_["category"]
    # print(uri_["label"])
    # Person:
    if uri != None:
        url_person= "".join(("https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=ASK%20%7B%20wd%3A",uri,"%20wdt%3AP31%2Fwdt%3AP279*%20wd%3AQ5%2C%20wd%3AQ215627%20%7D"))
        response_person = session.get(url_person)
        text_person=response_person.text
        y_person=text_person.find("true")
        if y_person > -1:
            #print("Person")
            x=2
        # Organisation:
        url_organisation= "".join(("https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=ASK%20%7B%20wd%3A",uri,"%20wdt%3AP31%2Fwdt%3AP279*%20wd%3AQ43229%7D"))
        response_organisation = session.get(url_organisation)
        text_organisation=response_organisation.text
        y_organisation=text_organisation.find("true")
        if y_organisation > -1:
            #print("Organisation")
            x=2

        # Location:
        # auch moeglich: https://www.wikidata.org/wiki/Q2221906 Geographicl Point
        # url_location= "".join(("https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=ASK%20%7B%20wd%3A",uri,"%20wdt%3AP31%2Fwdt%3AP279*%20wd%3AQ1496967%2Cwd%3AQ82794%2Cwd%3AQ618123%7D"))
        # response_location = session.get(url_location)
        response_location=session.get("https://query.wikidata.org/bigdata/namespace/wdq/sparql",params=dict(query="""
            ASK { wd:%(uri)s wdt:P31/wdt:P279* wd:Q1496967 }
        """ % **locals()))
        text_location=response_location.text
        y_location=text_location.find("true")
        if y_location > -1:
            #print("Location")
            x=2

        if y_person > -1:
            category="person"
        elif y_location > -1:
            category="location"
        elif y_organisation > -1:
            category="organisation"
        else:
            category=None
        #print("Category is: ",category)
        
        entity_db.update(dict(
                        category=category,
                    uri=uri
                    ),["uri"])

