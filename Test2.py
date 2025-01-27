def change(item, chan, audit_data):
    def process_string_value(sub_attr, attr_name, attr_value, modi_chan, audit):
        for dic in modi_chan:
            for dic_key, dic_value in dic.items():
                if dic_value["oldValue"] == attr_value:
                    sub_attr["value"][0]["attrValue"] = dic_value["newValue"]
                    audit.append({
                        "attrName": attr_name,
                        "oldValue": dic_value["oldValue"],
                        "newValue": dic_value["newValue"]
                    })

    def process_dict_value(sub_attr, attr_name, attr_value, modi_chan, audit):
        for dic in modi_chan:
            if attr_name in dic:
                attr_details = dic[attr_name]
                for key, value in attr_value.items():
                    if attr_details.get("name") == key and attr_details.get("oldValue") == value:
                        attr_value[key] = attr_details.get("newValue"]
                        audit.append({
                            "attrName": attr_details.get("name"),
                            "oldValue": attr_details.get("oldValue"),
                            "newValue": attr_details.get("newValue")
                        })

    def process_sub_attr(sub_attr, modi_chan, audit):
        attr_name = sub_attr.get("value", [{}])[0].get("attrName", "")
        attr_value = sub_attr.get("value", [{}])[0].get("attrValue", "")

        if isinstance(attr_value, str):
            process_string_value(sub_attr, attr_name, attr_value, modi_chan, audit)
        elif isinstance(attr_value, dict):
            process_dict_value(sub_attr, attr_name, attr_value, modi_chan, audit)

    def traverse_sub_attributes(item, modi_chan, audit):
        for sub_attr_list in item.get("subattrOutput", {}).values():
            for sub_attr in sub_attr_list:
                group_header = sub_attr.get("groupHeader", "")
                if group_header:
                    change(sub_attr, modi_chan, audit)
                else:
                    process_sub_attr(sub_attr, modi_chan, audit)

    # Start processing
    traverse_sub_attributes(item, chan, audit_data)
    return item, audit_data
