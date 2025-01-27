def change(item, chan, audit_data):
    def update_audit(attr_name, old_value, new_value, audit):
        """Add an audit entry."""
        audit.append({
            "attrName": attr_name,
            "oldValue": old_value,
            "newValue": new_value
        })

    def update_string_value(sub_attr, attr_name, attr_value, modifications, audit):
        """Update string values in sub_attr if they match modification criteria."""
        for mod in modifications:
            for mod_key, mod_value in mod.items():
                if mod_value["oldValue"] == attr_value:
                    sub_attr["value"][0]["attrValue"] = mod_value["newValue"]
                    update_audit(attr_name, mod_value["oldValue"], mod_value["newValue"], audit)

    def update_dict_value(attr_name, attr_value, modifications, audit):
        """Update dictionary values in sub_attr if they match modification criteria."""
        for mod in modifications:
            if attr_name in mod:
                attr_details = mod[attr_name]
                for key, value in attr_value.items():
                    if attr_details.get("name") == key and attr_details.get("oldValue") == value:
                        attr_value[key] = attr_details.get("newValue"]
                        update_audit(attr_details.get("name"), attr_details.get("oldValue"), attr_details.get("newValue"), audit)

    def process_sub_attr(sub_attr, modifications, audit):
        """Process a single sub_attr."""
        attr_name = sub_attr.get("value", [{}])[0].get("attrName", "")
        attr_value = sub_attr.get("value", [{}])[0].get("attrValue", "")

        if isinstance(attr_value, str):
            update_string_value(sub_attr, attr_name, attr_value, modifications, audit)
        elif isinstance(attr_value, dict):
            update_dict_value(attr_name, attr_value, modifications, audit)

    def traverse_sub_attributes(sub_attributes, modifications, audit):
        """Recursively traverse and process sub-attributes."""
        for sub_attr_list in sub_attributes.values():
            for sub_attr in sub_attr_list:
                if sub_attr.get("groupHeader", ""):
                    change(sub_attr, modifications, audit)
                else:
                    process_sub_attr(sub_attr, modifications, audit)

    # Main logic
    traverse_sub_attributes(item.get("subattrOutput", {}), chan, audit_data)
    return item, audit_data
