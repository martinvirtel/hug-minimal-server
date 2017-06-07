import sqlite3
import dataset
import os

def get_text (dpa_id):
    dpa_id=dpa_id.replace("v-","/")

    # path_original = "/Users/alex/nex-analysis-server/hug-minimal-server"
    # path = "/Users/alex/nex-analysis"

    # os.chdir(path)

    db='sqlite:///nex-analysis.db'


    database = dataset.connect(db)
    dpa_text=database["dpa_text"]
    # os.chdir(path_original)
    try:
        #text=dpa_text.find_one(dpa_id=dpa_id)["text"]
        text=list(database.query("select text from dpa_text  where dpa_id LIKE :dpa_id",dpa_id=dpa_id))[0]["text"]
        title=list(database.query("select title from dpa_text  where dpa_id LIKE :dpa_id",dpa_id=dpa_id))[0]["title"]
        text_output={
            "text":text,
            "title":title,
            "dpa_id":dpa_id
        }
    except IndexError:
        text_output={
            "text":"",
            "title":"No text found for this dpa-id"
        }
    
    return(text_output)
