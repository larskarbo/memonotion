def count_elements(cv):
    props = cv.collection.get_schema_properties()
    print('props: ', props)
    total = 0
    aggregate_params = []
    for prp in props:
        aggregate_params.append({
            "property": prp["slug"],
            "aggregation_type": "not_empty",
            "id": prp["slug"],
        })
    result = cv.build_query(aggregate=aggregate_params).execute()
    for prp in props:
        total += result.get_aggregate(prp["slug"])
    return total

def cv_props(cv):
    arr = cv.collection.get_schema_properties()
    props = list(map(lambda item: item["slug"], arr))
    return props

def get_next_cv(client, block):
    cv2 = False
    for child in block.parent.children:
        if child.type == "collection_view":
            # child
            cv2 = client.get_collection_view(
                child.views[0].id, collection=child.collection)
    if not cv2:
        raise AssertionError("fuck, didn't find database")
    return cv2


def blockToHTML(client, blockID):
    block = client.get_block(blockID)
    print('block.type: ', block.type)
    out = ""
    childrenOut = ""
    if block.type != "image":
        try:
            children = block.get("content")
            for child in children:
                childrenOut += blockToHTML(client, child)
        except Exception as e:
            print(e)
            childrenOut = block.title

    if block.type == "toggle":
        out = "<div class='toggle'>" + block.title + "<div>" + childrenOut + "</div></div>"
    elif block.type == "column_list":
        out = "<div class='column_list'>" + childrenOut + "</div>"
    elif block.type == "column":
        out = "<div class='column'>" + childrenOut + "</div>"
    elif block.type == "bulleted_list":
        out = "<ul><li>" + childrenOut + "</li></ul>"
    elif block.type == "numbered_list":
        out = "<ol><li>" + childrenOut + "</li></ol>"
    elif block.type == "text":
        out = "<p>" + childrenOut + "</p>"
    elif block.type == "quote":
        out = "<p>" + childrenOut + "</p>"
    # image link does not work
    # elif block.type == "image":
    #     print("display_source", block.display_source)
    #     print("source", block.source)
    #     out = "<img src>"
    else:
        return "See link to get content"
    

    return out
