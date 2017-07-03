import sqlite3
import dataset


def overlap(dpa_id,value):
    value=value-1

    #dpa_id="urn:newsml:dpa.com:20090101:170319-99-722478/2"
    #value=3
    dpa_id=dpa_id.replace("v-","/")
    db='sqlite:///nex-analysis.db'
    database = dataset.connect(db)
    dpa_text=database["dpa_text"]
    found_entities=database["found_entities"]
    entity=database["entity"]
    tools= database["tools"]
    dpa_text= database["dpa_text"]

    text_list=list(database.query("select rowid, text, title from dpa_text where dpa_id=:dpa_id",dpa_id=dpa_id))
    dpa_id_id=text_list[0]["rowid"]
    text=text_list[0]["text"]
    title=text_list[0]["title"]

    mixed_list=[]
    for x in range (1,6):
        tool_id=x
        tool=list(database.query("""
            select 
            tool
            from tools where 
            rowid=:tool_id
            """,tool_id=tool_id))[0]["tool"]
        entity_list=list(database.query("""
        select 
        start,end,entity_id
        from found_entities 
        where dpa_id =:dpa_id_id and tool_id =:tool_id
        order by start asc""",dpa_id_id=dpa_id_id,tool_id=tool_id))
        for entity in entity_list:
            entity["tool"]=tool
            mixed_list.append(entity)
    overlaps={}
    for entry in mixed_list:
        start=entry["start"]
        end=entry["end"]
        entity_id=entry["entity_id"]
        tool_entry={entry["tool"]:entry["tool"]}
        

        x=1
        for entry_2 in mixed_list:
            start_2=entry_2["start"]
            end_2=entry_2["end"]
            entity_id_2=entry_2["entity_id"]
            if start==start_2 and end==end_2 and entity_id==entity_id_2:
                entity_info=list(database.query("select uri, label, category from entity where rowid=:entity_id",entity_id=entity_id_2))
                uri=entity_info[0]["uri"]
                label=entity_info[0]["label"]
                category=entity_info[0]["category"]
                key="%s_%s"%(start,end)
                entity_dict={key:{
                    "start":start,
                    "end":end,
                    "entity_id":entity_id,
                    "uri":uri,
                    "label":label,
                    "category":category,
                    "counter":x,
                    "tool":tool_entry
                }}
                x=x+1
        if entity_dict[key]["counter"] > value:
            try:
                tool_dict=overlaps[key]["tool"]
                tool_dict.update(entity_dict[key]["tool"])
                entity_dict[key]["tool"]=tool_dict
            except KeyError:
                overlaps.update(entity_dict)
    final_overlap=[]
    for overlap in overlaps:
        if overlaps[overlap]["counter"]>value:
            final_overlap.append(overlaps[overlap])

    length=len(final_overlap)
    word_count=len(text.split())
    try:
        rate_entity=round(word_count/length,1)
    except ZeroDivisionError:
        rate_entity= "No entities found"
    y=0
    text_list=[]
    #print(length)
    final_overlap=sorted(final_overlap, key=lambda x: x["start"])
    for x in range(0,length) :
        part=text[y:int(final_overlap[x]["start"])]
        text_list.append({"status":"text","text":part})
        entity_element=text[int(final_overlap[x]["start"]):int(final_overlap[x]["end"])]
        text_list.append({
            "status":"entity",
            "text":entity_element,
            "uri":final_overlap[x]["uri"],
            "label":final_overlap[x]["label"],
            "category":final_overlap[x]["category"],
            "tool":final_overlap[x]["tool"]
            })
        y=final_overlap[x]["end"]
    end_text=text[y:len(text)]
    text_list.append({"status":"text","text":end_text})
        


    output_overlap={
        "color":"yellow",
        "title":title,
        "length":length,
        "text_list":text_list,
        "rate_entity":rate_entity
    }
    return(output_overlap)