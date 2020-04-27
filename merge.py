import json 
import re
from collections import OrderedDict 

no_of_isin=[]
total_value=[]
account=[]
total_value_account=0
total_claims_value=0
claim_value_list=[]


def check_val(values):
    global total_value, no_of_isin, account
    for data in values:
        if 'No of isin' in data.keys():
            account.append(data)
            no_of_isin.append(int(data['No of isin']))
        if 'Value' in data.keys():
            total_value.append(float(data['Value']))
        

def match_account_details(key,values):
    global total_value, no_of_isin, account
    temp1=0
    temp2=0
    for key1,value1 in values[0].items():
        if re.search(r'TotalValue',key1): 
            temp1=round(float(value1),2)
        else:
            temp2=int(value1)
    index1=-1
    index2=-1
    if temp1 in total_value:
        index1=total_value.index(temp1)
    elif temp2 in no_of_isin:
        index2=no_of_isin.index(temp2)
    if index1!=-1:
        return(account[index1])
    elif index2!=-1:
        return(account[index1])



def merge_data2(list_of_dict):
    global total_value_account,total_claims_value,claim_value_list
    result=OrderedDict()
    index=0
    key_result=''
    for dictionary in list_of_dict:
        if re.search(r'Address|StatementPeriod|PAN|Client ID|DP ID',str(dictionary.keys())):
            if 'ClientDetail' in result.keys():
                result['ClientDetail']+=[dictionary]
            else:
                result['ClientDetail']=[dictionary]
            continue
        for key,value in dictionary.items():
            if re.search(r'AccountInfo|account_details',key):
                if re.search(r'AccountInfo',key):
                    check_val(value)
                    if key in result.keys():
                        result[key]+=value
                    else:
                        result[key]=value
                else:
                    if key in result.keys():
                        value[0]['TotalAccount']+=result[key][0]['TotalAccount']
                        value[0]['GrandTotal']+=result[key][0]['GrandTotal']
                        result[key]=value   
                        total_value_account=value[0]['GrandTotal']
                    else:
                        result[key]=value
            else:
                if len(value)>0:
                    if re.search(r'_details',key):
                        if value[0]['TotalValue']!=0:
                            total_claims_value+=value[0]['TotalValue']
                            result[key_result]+=[{key:value}]
                            claim_value_list.append(value[0])
                            if match_account_details(key,value):
                                result[key_result]=[{'AccountType':match_account_details(key,value)}]+result[key_result]   
                            else:
                                result[key_result]=[{'AccountType':'error'}]+result[key_result]        
                    else:
                        if key in result.keys():
                            index+=1
                            result[key+' '*index]=[{'description':value}]
                            key_result=key+' '*index
                        else:
                            result[key]=[{'description':value}]
                            key_result=key           
    return result


def count_check():
    if total_claims_value==total_value_account:
        return True
    else:
        return False


# op=open('anstemp.txt','w')
# with open('C:/Users/roger/Desktop/work/ocr_work/nsdl_ocr/git/ocr_data_extraction/pdf/comp/kpmenon_intermediate.txt','r') as file:
#     openfile=eval(file.read())
#     rst=merge_data2(openfile)
#     print(claim_value_list)
#     # print(no_of_isin)
#     if count_check():
#         json.dump(rst,op,indent=4)
    
    





    # result=merge_data(openfile)
    # if check_total(result):
    #     result_data=format(result)
    #     with open('test2.log','w') as op:
    #         json.dump(result_data,op,indent=4)
        

    
