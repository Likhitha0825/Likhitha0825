 name_dic  is {0: 'Account Statement -1', 1: 'Bank Details -1'}


def output_excel(extract_json, template_name):
    try:
        global append_name
        data = json.loads(extract_json)
        li = []
        excel_dic = {}
        if template_name.startswith("Financial Statement"):
            recr2(data)
            li = list(data.keys())
            for i in li:
                excel_dic[i] = pd.DataFrame(append_name[i])
            list_dfs = []
            name_dic = {}
            for i in excel_dic:
                list_dfs.append(excel_dic[i])
            for i, j in enumerate(li):
                if len(j) <= 31:
                    name_dic[i] = j
                else:
                    name_dic[i] = j.replace("Statement of", "")
        elif template_name == "Bank Statement":
            check_multiple_extractions(data)
            bs_dic = data["Bankstatements"][0]
            new_data = data["Bankstatements"][0]["Bankstatement - 1"][0]
            recr2(new_data)
            li = list(new_data.keys())
            list_dfs = []
            name_dic = {}
            for k in bs_dic.keys():
                excel_dic = {}
                new_data = data["Bankstatements"][0][k][0]
                recr2(new_data)
                li = list(new_data.keys())
                for i in li:
                    excel_dic[i + " -" + k[-1]] = pd.DataFrame(append_name[i])
                for j in excel_dic:
                    list_dfs.append(excel_dic[j])
                add_num = int(k[-1]) - 1
                add_num *= 2
                get_name_dic(li, name_dic, add_num, k)
        return list_dfs, name_dic
    except Exception as e:
        logger.exception(f"Output Excel: {e}")
