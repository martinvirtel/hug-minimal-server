import sqlite3
import dataset
import json
from json import JSONDecodeError
import nltk
import itertools
import copy

def evaluation(dpa_id):
    dpa_id=dpa_id.replace("v-","/")
    db='sqlite:///nex-analysis.db'
    database = dataset.connect(db)
    dpa_text=database["dpa_text"]
    found_entities=database["found_entities"]
    entity=database["entity"]
    tools= database["tools"]
    dpa_text= database["dpa_text"]

    text_list=list(database.query("select rowid, text, title from dpa_text where dpa_id=:dpa_id",dpa_id=dpa_id))
    # dpa_id_id=text_list[0]["rowid"]
    text=text_list[0]["text"]
    title=text_list[0]["title"]
    entity_list=list(database.query("""
            select 
            id,start,end,confidence,tools,label,uri,extra
            from entities_view 
            where dpa_id =:dpa_id_id
            order by start asc""",dpa_id_id=dpa_id))
    output_dict={}
    for entity in entity_list:
        try:
            output_dict[entity["id"]].update({entity["tools"]:
                        {"start":entity["start"],
                        "end":entity["end"],
                        "confidence":entity["confidence"],
                        "label":entity["label"],
                        "uri":entity["uri"],
                        "extra":json.dumps(entity["extra"])
                        }
                    
                })
        except KeyError:
            output_dict.update({
                entity["id"]:
                    {entity["tools"]:
                        {"start":entity["start"],
                        "end":entity["end"],
                        "confidence":entity["confidence"],
                        "label":entity["label"],
                        "uri":entity["uri"],
                        "extra":json.dumps(entity["extra"])
                        }
                    
                }
            })

# Marking text
    ll = [[nltk.word_tokenize(w), ' '] for w in text.split()]
    text_list=list(itertools.chain(*list(itertools.chain(*ll))))
    text_dict=[]
    start=0
    for token in text_list:
        token_dict={}
        token_dict["text"]=token
        token_dict["start"]=start
        length_word=len(token)
        end=start+length_word
        token_dict["end"]=start+length_word
        token_dict["key"]="%s_%s"%(start,end)
        start=start+length_word
        text_dict.append(token_dict)
    output_evaluation={
        "text_dict":text_dict,
        "output_dict":json.dumps(output_dict),
        "title":title
    }
    return (output_evaluation)


