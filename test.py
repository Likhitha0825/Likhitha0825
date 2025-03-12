def validate(self):
        jsonstr = output_json(self.output_json)
        list_dfs,name_dic=output_excel(jsonstr)
        index_list=get_index_list_bs(name_dic)
        final_dict=[]
        for index in index_list:
            work_dict=list_dfs[index]
            work_dict.columns = map(str.lower, work_dict.columns)
            p_li=[]
            for nm in work_dict['name']:
                p_li.append(nm.split('|')[1])
            work_dict['pageNum']=p_li        
            BankStatement.validate(work_dict)
            list(work_dict['name'])
            alr_added=[]
            temp_dict={}
            self.check_pass_or_fail(work_dict,alr_added,temp_dict)
            for i in temp_dict:
                k="Page"+str(i)+" "
                if temp_dict[i]["Passed"]:
                    x='|'.join(temp_dict[i]["Passed"])
                    tpdict={}
                    tpdict["attr_name"]=k+x
                    tpdict["attr_status"]="Passed"
                    final_dict.append(tpdict)
                if temp_dict[i]["Failed"]:
                    tfdict={}
                    x='|'.join(temp_dict[i]["Failed"])
                    tfdict["attr_name"]=k+x
                    tfdict["attr_status"]="Failed"
                    final_dict.append(tfdict)               
            valid_str=json.dumps(final_dict)
            self.validation_dict=valid_str      
        return
