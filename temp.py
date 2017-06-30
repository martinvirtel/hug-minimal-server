#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib.parse
import urllib.request
import requests
import xml
import dataset






uri= "Q8682"

db='sqlite:///nex-analysis.db'
database = dataset.connect(db)


database = dataset.connect(db)

entity_db=database["entity"]

entity_db.update(dict(
                    label="Test",
                    uri="Q28911"
                    ),["uri"])