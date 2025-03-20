    def check_pass_or_fail(self,work_dict,alr_added,temp_dict):
        for i,row in work_dict.iterrows():
            try:
                d2=None
                d1 = parse(str(row['transaction date']).strip(), fuzzy=True)
                if d1.year<2000 or d1.year>date.today().year:
                    raise InvalidDate
                if Bank.VAL_DATE in row.keys():
                    d2=parse(str(row[Bank.VAL_DATE]).strip(), fuzzy=True)
                    if d2.year<2000 or d2.year>date.today().year:   
                        raise InvalidDate
            except Exception as f:
                row['conf_score']=60
                logger.info(f'Exception inside validate bank as {f}')
            li=row["name"].split('|')
            ind=li[1]
            if ind not in alr_added:
                alr_added.append(ind)
                temp_dict[ind]={}
                temp_dict[ind]["Passed"]=[]
                temp_dict[ind]["Failed"]=[]
            self.populate_pass_or_fail(row,temp_dict,ind,li)
