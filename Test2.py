def extract_column_names(data):
    first_key = next(iter(data.keys()))
    def traverse(data, parent=""):
        column_names = []
        for item in data:
            attr_name = item.get("displayProperties", {}).get("displayName", "")
            subattr = item.get("subattrOutput", {})

            current_name = f"{parent} | {attr_name}" if parent else attr_name

            if subattr:
                for key, subitems in subattr.items():
                    column_names.extend(traverse(subitems, current_name))
            else:
                column_names.append(current_name)

        return column_names

    extracted_names = traverse(data[first_key])
    ans = [name.split(" | ", 1)[-1] for name in extracted_names]
    ans.insert(0,'Name')
    return ans


def output_excel(json_data):
    def helper(name_prefix, top_level_name, json_obj, extracted_data):
        if isinstance(json_obj, list):
            for item in json_obj:
                helper(name_prefix, top_level_name, item, extracted_data)
        elif isinstance(json_obj, dict):
            if "value" in json_obj and isinstance(json_obj["value"], list):
                for val in json_obj["value"]:
                    row_data = {}
                    if "attrName" in val and "attrValue" in val:
                        attr_name = val["attrName"]
                        attr_value = val["attrValue"]
                        if(attr_value is None):
                            attr_value=''
                        display_style = json_obj.get("displayProperties", {}).get("displayStyle", "")

                        if display_style == "key_value_pair":
                            row_data["Name"] = top_level_name
                        else:
                            row_data["Name"] = f"{name_prefix}"

                        if isinstance(attr_value, dict):
                            row_data.update(attr_value)
                            if attr_value is not None:
                                extracted_data.append(row_data)
                        else:
                            row_data[attr_name] = attr_value
                            if json_obj.get("subattrOutput", {}) == {}:
                                extracted_data.append(row_data)
            if "subattrOutput" in json_obj or isinstance(json_obj["subattrOutput"], dict):
                for sub_key, sub_value in json_obj["subattrOutput"].items():
                    new_prefix = f"{name_prefix}|{sub_key}" if name_prefix else sub_key
                    helper(new_prefix, top_level_name, sub_value, extracted_data)

    def clean_dataframe(df):
        columns_to_drop = [col for col in df.columns if any(df["Name"].astype(str).str.contains(col, na=False))]
        rows_to_drop = df["Name"].isin(columns_to_drop)
        empty_rows_mask = df.drop(columns=["Name"], errors='ignore').isna().all(axis=1)
        rows_to_drop = rows_to_drop & empty_rows_mask
        df_cleaned = df.loc[~rows_to_drop].drop(columns=columns_to_drop, errors='ignore')
        df_cleaned = df_cleaned.dropna(axis=1, how='all')
        return df_cleaned

    def move_duplicate_names(df):
        duplicate_names = df["Name"].value_counts()
        duplicate_names = duplicate_names[duplicate_names > 1].index.tolist()
        duplicate_rows = df[df["Name"].isin(duplicate_names)]
        remaining_rows = df[~df["Name"].isin(duplicate_names)]
        return remaining_rows, duplicate_rows

    def remove_redundancy(df):
        if df.empty:
            return df
        name_value = df.iloc[0]["Name"]
        merged_row = {"Name": name_value}
        for col in df.columns:
            if col != "Name":
                merged_row[col] = df[col].dropna().astype(str).unique().tolist()

        merged_row = {k: ", ".join(v) if isinstance(v, list) else v for k, v in merged_row.items()}
        df_cleaned = pd.DataFrame([merged_row])
        return df_cleaned

    def find_previous_attr_name(data, target, prev_attr=None):
        if isinstance(data, dict):
            if "value" in data and isinstance(data["value"], list):
                for item in data["value"]:
                    if isinstance(item, dict) and item.get("attrName") == target:
                        return prev_attr
                    if "attrName" in item:
                        prev_attr = item["attrName"]
            
            for key, value in data.items():
                if key != "value":
                    result = find_previous_attr_name(value, target, prev_attr)
                    if result:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = find_previous_attr_name(item, target, prev_attr)
                if result:
                    return result
        return None
    
    workbook_data = {}
    duplicate_data = {}

    for key, value in json_data.items():
        extracted_data = []
        helper("", key, value, extracted_data)
        workbook_data[key] = extracted_data
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            output_filename = temp_file.name
        with pd.ExcelWriter(output_filename, engine="openpyxl") as writer:
            for sheet_name, data in workbook_data.items():
                if data:
                    df = pd.DataFrame(data)
                    #df.to_excel(writer,index=False,sheet_name='uncleaned')
                    df_cleaned = clean_dataframe(df)
                    df_unique, df_duplicates = move_duplicate_names(df_cleaned)
                    df_uniq=df_unique.dropna(how='all', axis=1)
                    if(len(df_uniq)<2 and len(df_uniq)>0):
                        df_uniq.columns=extract_column_names(json_data)
                    df_uniq.to_excel(writer, index=False, sheet_name=sheet_name[:31])

                    if not df_duplicates.empty:
                        df_no_redundancy = remove_redundancy(df_duplicates)
                        if(len(df_unique) == 0):
                            if(len(df_no_redundancy)<2):
                                df_no_redundancy.columns=extract_column_names(json_data)
                            df_no_redundancy=df_no_redundancy.transpose()
                            df_no_redundancy.to_excel(writer, index=True, sheet_name=f"{sheet_name[:25]}")
                        else:
                            df_uni=df_unique.dropna(how='all', axis=1)
                            if(len(df_uni)<2):
                                df_uni.columns=extract_column_names(json_data)
                            df_uni.to_excel(writer, index=False, sheet_name=sheet_name[:31])
                            df_uni_columns = df_uni.columns.str.strip()
                            df_no_redundancy_columns = df_no_redundancy.columns.str.strip()
                            common_cols = list(set(df_uni_columns) & set(df_no_redundancy_columns))
                            df_no_redundancy = df_no_redundancy.drop(columns=common_cols,errors='ignore')
                            sheet_nam = find_previous_attr_name(json_data,df_no_redundancy.columns[0])
                            df_no_redundancy.insert(0,'Name',[sheet_nam]*len(df_no_redundancy))
                            if(len(df_no_redundancy)<2):
                                if(len(extract_column_names(json_data)) == len(df_no_redundancy.columns)):
                                    df_no_redundancy.columns=extract_column_names(json_data)
                            df_no_redundancy.to_excel(writer, index=False, sheet_name=f"{sheet_nam[:25]}")

        logger.info(f"Excel file '{output_filename}' created successfully!")
        return output_filename

    except Exception as e:
        logger.error(f'An error occurred while writing to Excel: {e}')
