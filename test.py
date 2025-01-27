def change(item, chan, audit_data):
    def update_value(attr_name, attr_value, modifications, audit):
        """Update string or dictionary values and record audit."""
        if isinstance(attr_value, str):
            for mod in modifications:
                for _, mod_value in mod.items():
                    if mod_value["oldValue"] == attr_value:
                        attr_value = mod_value["newValue"]
                        update_audit(attr_name, mod_value["oldValue"], mod_value["newValue"], audit)
        elif isinstance(attr_value, dict):
            for mod in modifications:
                if attr_name in mod:
                    attr_details = mod[attr_name]
                    for key, value in attr_value.items():
                        if attr_details.get("name") == key and attr_details.get("oldValue") == value:
                            attr_value[key] = attr_details["newValue"]
                            update_audit(attr_details["name"], attr_details["oldValue"], attr_details["newValue"], audit)
        return attr_value

    def update_audit(attr_name, old_value, new_value, audit):
        """Record the change in audit."""
        audit.append({
            "attrName": attr_name,
            "oldValue": old_value,
            "newValue": new_value,
        })

    def process_sub_attributes(sub_attributes, modifications, audit):
        """Process each sub-attribute recursively or update its values."""
        for sub_attr_list in sub_attributes.values():
            for sub_attr in sub_attr_list:
                if sub_attr.get("groupHeader"):
                    change(sub_attr, modifications, audit)
                else:
                    attr_data = sub_attr.get("value", [{}])[0]
                    attr_name = attr_data.get("attrName", "")
                    attr_value = attr_data.get("attrValue", "")
                    attr_data["attrValue"] = update_value(attr_name, attr_value, modifications, audit)

    # Start processing sub-attributes
    process_sub_attributes(item.get("subattrOutput", {}), chan, audit_data)
    return item, audit_data
