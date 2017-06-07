import os
import html
import dataset

def index(start, limit):
    # path_original = "/Users/alex/nex-analysis-server/hug-minimal-server"
    # path = "/Users/alex/nex-analysis"

    # os.chdir(path)
    db='sqlite:///nex-analysis.db'
    database = dataset.connect(db)
    # os.chdir(path_original)
    length=len(list(database.query("""
        select 
        dpa_id
        from dpa_text
        """
    )))
    pages=length//20
    if length%20 != 0:
        pages=pages+1
    

    dpa_id_list=list(database.query("""
        select 
        dpa_id,
        title,
        ressort,
        date
        from dpa_text
        limit :limit
        offset :offset
        """,limit=limit, offset=start))
    
    index_list=[]
    for item in dpa_id_list:
        index_dict={}
        dpa_id=item["dpa_id"].replace("/","v-")
        index_dict["dpa_id"]=dpa_id
        link="/nex/%(dpa_id)s/all"%locals()
        pipette="https://pipette.dpa-newslab.com/pipette/#/doc/%s"%dpa_id[:-3]
        index_dict["link"]=link
        index_dict["title"]=item["title"]
        index_dict["ressort"]=item["ressort"]
        index_dict["date"]=item["date"]
        index_list.append(index_dict)
    output_index={"pages":pages,"index_list":index_list}
    return(output_index)


