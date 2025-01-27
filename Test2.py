def change(item, chan, audit_data):
    def update_string_value(attr_name, attr_value, modi_chan, audit):
        for dic in modi_chan:
            for dic_key, dic_value in dic.items():
                if dic_value["oldValue"] == attr_value:
                    updated_value = dic_value["newValue"]
                    attr_value = updated_value  # Update the value directly
                    audit.append({
                        "attrName": attr_name,
                        "oldValue": dic_value["oldValue"],
                        "newValue": updated_value
                    })
                    return attr_value

    def update_dict_value(attr_name, attr_value, modi_chan, audit):
        
    with dict value still ruy or loop
