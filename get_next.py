import os
import dataset
import random


def get_next (dpa_id):
    #dpa_id = "urn:newsml:dpa.com:20090101:170221-99-370286v-3"
    dpa_id = dpa_id.replace("v-","/")
    # path_original = "/Users/alex/nex-analysis-server/hug-minimal-server"
    # path = "/Users/alex/nex-analysis"
    # os.chdir(path)
    db='sqlite:///nex-analysis.db'
    database = dataset.connect(db)
    # os.chdir(path_original)
    next_dpa_id={}
    #print(dpa_id)
    # #print(list(database.query("""
    #             select 
    #             rowid
    #             from dpa_text
    #             where dpa_id=:dpa_id
    #             """,dpa_id=dpa_id)))
    dpa_id_id=(list(database.query("""
                select 
                rowid
                from dpa_text
                where dpa_id=:dpa_id
                """,dpa_id=dpa_id
                )))[0]["rowid"]
    try:
        next_dpa_id["pre_dpa_id"]=(list(database.query("""
                    select 
                    dpa_id
                    from dpa_text
                    where rowid=:dpa_id_id
                    """,dpa_id_id=str(dpa_id_id-1)
        )))[0]["dpa_id"].replace("/","v-")
    except IndexError:
        next_dpa_id["pre_dpa_id"] = None

    try:
        next_dpa_id["post_dpa_id"]=(list(database.query("""
                    select 
                    dpa_id
                    from dpa_text
                    where rowid=:dpa_id_id
                    """,dpa_id_id=str(dpa_id_id+1)
        )))[0]["dpa_id"].replace("/","v-")
    except IndexError:
        next_dpa_id["post_dpa_id"] = None

    length_text=len(list(database.query("""
                select 
                rowid
                from dpa_text
                """
    )))
    r=random.randint(1,length_text)
    next_dpa_id["random_dpa_id"]=(list(database.query("""
                    select 
                    dpa_id
                    from dpa_text
                    where rowid=:dpa_id_id
                    """,dpa_id_id=r
        )))[0]["dpa_id"].replace("/","v-")

    return(next_dpa_id)