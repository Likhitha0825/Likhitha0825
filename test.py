def change(item, chan, audit_data):
    def update_audit(attr_name, old_value, new_value):
        audit_data.append({
            "attrName": attr_name,
            "oldValue": old_value,
            "newValue": new_value
        })

    def update_attr_value(attr_name, attr_value, modifications):
        for mod in modifications:
            for _, mod_value in mod.items():
                if isinstance(attr_value, str) and mod_value["oldValue"] == attr_value:
                    update_audit(attr_name, mod_value["oldValue"], mod_value["newValue"])
                    return mod_value["newValue"]
                if isinstance(attr_value, dict) and attr_name in mod:
                    attr_details = mod[attr_name]
                    new_value = attr_details.get("newValue")
                    if attr_details["name"] in attr_value and attr_value[attr_details["name"]] == attr_details["oldValue"]:
                        attr_value[attr_details["name"]] = new_value
                        update_audit(attr_details["name"], attr_details["oldValue"], new_value)
        return attr_value

    def process_sub_attr(sub_attr, modifications):
        attr_data = sub_attr.get("value", [{}])[0]
        attr_data["attrValue"] = update_attr_value(
            attr_data.get("attrName", ""),
            attr_data.get("attrValue", ""),
            modifications
        )

    def traverse_attributes(sub_attributes, modifications):
        for sub_attr_list in sub_attributes.values():
            for sub_attr in sub_attr_list:
                (change if sub_attr.get("groupHeader") else process_sub_attr)(sub_attr, modifications)

    traverse_attributes(item.get("subattrOutput", {}), chan)
    return item, audit_data
