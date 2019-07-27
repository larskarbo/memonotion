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
