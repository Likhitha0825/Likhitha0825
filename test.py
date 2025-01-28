def process(item):
    entity_data = initialize_entity_data(item)
    subattr_output_list = process_subattr_output(item)
    entity_data["subattrOutput"] = subattr_output_list if subattr_output_list else []
    return entity_data


def initialize_entity_data(item):
    """Initialize the entity data with default values."""
    return {
        "name": item.get("displayProperties", {}).get("displayName", ""),
        "subattrOutput": [],
        "value": [
            {
                "editableData": [
                    {
                        "attrName": None,
                        "attrValue": None
                    }
                ],
                "score": None,
                "highlight": None,
                "displayName": item.get("displayProperties", {}).get("displayName", "")
            }
        ],
        "groupHeader": item.get('groupHeader', ''),
        "displayProperties": {
            "displayStyle": item.get("displayProperties", {}).get("displayStyle", "")
        }
    }


def process_subattr_output(item):
    """Process the 'subattrOutput' of the item and return the list."""
    subattr_output_list = []
    for sub_attr_key, sub_attr_list in item.get("subattrOutput", {}).items():
        for sub_attr in sub_attr_list:
            if sub_attr.get("groupHeader", ""):
                nested_item = process_nested_subattr(sub_attr)
                subattr_output_list.append(nested_item)
            else:
                subattr_output_list = process_non_grouped_subattr(item, sub_attr, subattr_output_list)
    return subattr_output_list


def process_nested_subattr(sub_attr):
    """Process a nested sub-attribute."""
    group_header = sub_attr.get("groupHeader", "")
    nested_item = process(sub_attr)
    nested_item["groupHeader"] = group_header
    return nested_item


def process_non_grouped_subattr(item, sub_attr, subattr_output_list):
    """Process sub-attributes that are not grouped and append them to the output list."""
    attr_value = sub_attr.get("value", [{}])[0].get("attrValue", "")
    editable_data = extract_editable_data(attr_value, sub_attr)
    value = {
        "editableData": editable_data,
        "score": sub_attr.get("score", 0),
        "highlight": sub_attr.get("displayProperties", {}).get("highlight", ""),
        "displayName": sub_attr.get("displayProperties", {}).get("displayName", "")
    }
    if not subattr_output_list:
        subattr_output_list.append(create_default_subattr_output(item))
    subattr_output_list[0]["value"].append(value)
    return subattr_output_list


def extract_editable_data(attr_value, sub_attr):
    """Extract editable data from the attribute value."""
    editable_data = []
    if isinstance(attr_value, dict):
        for key, value in attr_value.items():
            editable_data.append({
                "attrName": key,
                "attrValue": value
            })
    elif isinstance(attr_value, str):
        editable_data.append({
            "attrName": sub_attr.get("displayProperties", {}).get("displayName", ""),
            "attrValue": attr_value
        })
    return editable_data


def create_default_subattr_output(item):
    """Create a default sub-attribute output dictionary."""
    return {
        "name": None,
        "subattrOutput": [],
        "value": [],
        "groupHeader": item.get('groupHeader', ''),
        "displayProperties": {
            "displayStyle": item.get("displayProperties", {}).get("displayStyle", "key_value_pair")
        },
    }
