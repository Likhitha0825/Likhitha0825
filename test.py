def change(item, chan,audit_data):
    audit=audit_data
    modi_chan = chan
    for sub_attr_key, sub_attr_list in item.get("subattrOutput", {}).items():
        for sub_attr in sub_attr_list:
            group_header = sub_attr.get("groupHeader", "")
            if group_header:
                change(sub_attr, modi_chan,audit)
            else:
                attr_name = sub_attr.get("value", [{}])[0].get("attrName", "")
                attr_value = sub_attr.get("value", [{}])[0].get("attrValue", "")
                for dic in modi_chan:
                    if isinstance(attr_value, str):
                        for dic_key, dic_value in dic.items():
                            if dic_value["oldValue"] == attr_value:
                                sub_attr["value"][0]["attrValue"] = dic_value["newValue"]
                                data = {
                                    "attrName": attr_name,
                                    "oldValue": dic_value["oldValue"],
                                    "newValue": dic_value["newValue"]
                                }
                                audit.append(data)
                    elif isinstance(attr_value, dict):
                        if attr_name in dic:
                            attr_details = dic[attr_name]
                            for key, value in attr_value.items():
                                if attr_details.get("name") == key and attr_details.get("oldValue") == value:
                                    attr_value[key] = attr_details.get("newValue")
                                    data = {
                                        "attrName": attr_details.get("name"),
                                        "oldValue": attr_details.get("oldValue"),
                                        "newValue": attr_details.get("newValue")
                                    }
                                    audit.append(data)
    return item,audit


