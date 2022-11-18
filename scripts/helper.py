# Series of functions used to filter JSON objects returned via the iControl REST API




# Return a generator object containing the value of the key from the json input
def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():     
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)


def filter_keys(json_dict,keys):
    filtered_dict = {}
    for column in keys.keys():    
        value = item_generator(json_dict,keys[column])
        filtered_dict[column] = next(value)      
    return filtered_dict


def filter_restobject(rest_response,keys):
    if(isinstance(rest_response,list)):
        filtered = []
        for item in rest_response:
            item_dict = item.asdict()
            filtered.append( filter_keys(item_dict,keys))
    else:
        dict = rest_response.asdict()
        filtered = filter_keys(dict,keys)

    return filtered
