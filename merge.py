import json 
import re
from collections import OrderedDict 

def add_details(sum,value):
    if list(value[0].keys())[0] in sum:
        sum[list(value[0].keys())[0]]+=value[0][list(value[0].keys())[0]]
    else:
        sum[list(value[0].keys())[0]]=value[0][list(value[0].keys())[0]]
    if list(value[0].keys())[1] in sum:
        sum[list(value[0].keys())[1]]+=value[0][list(value[0].keys())[1]]
    else:
        sum[list(value[0].keys())[1]]=value[0][list(value[0].keys())[1]]
    return sum


def merge_data(list_of_dict):
    index=1
    prev_key=''
    visit_key=[]
    result=OrderedDict()
    sum={}
    len_total=0
    for dictionary in list_of_dict:
        len_total+=1
        if len(dictionary.keys())!=2:
            if 'ParsedData' in result.keys():
                result['ParsedData']+=[dictionary]
            else:
                result['ParsedData']=[dictionary]
            continue
        for key,value in dictionary.items():
            key=key.strip()
            if re.search('_details',key):
                add_details(sum,value)
                if len_total==len(list_of_dict):
                    result[next(reversed(result))]+=[sum]
            elif type(value)==list:
                if prev_key==key and prev_key:
                    result[key+str(index)]+=value
                    #print('....',key)
                else:
                    if key in visit_key:
                        result[next(reversed(result))]+=[sum]
                        index+=1
                        result[key+str(index)]=value
                        #print('++',key)
                    else:
                        if result:
                            result[next(reversed(result))]+=[sum]
                        result[key+str(index)]=value
                        #print('+++',key)
                    sum={}
                visit_key.append(key)
                prev_key=key
            else:
                pass
    return result
                    
def check_total(result):
    total2=0
    total=0
    for data in result:
        if re.search(r'AccountInfo',data):
            total2+=round(float(result[data][-1]['GrandTotal']),2)
        elif not re.search(r'ParsedData',data):
            total+=round(float(result[data][-1]['TotalValue']),2)
    if total2==total:
        print('matched',total2-total)
        return True
    else:
        return False
       

def format(result):
    account_data={}
    result_data={}
    for data in result:
        if re.search(r'ParsedData',data):
            result_data[data]=result[data]
        elif re.search(r'AccountInfo',data):
            #print(data,result[data])
            result_data[data]=result[data]
            for line in result[data][0:-1]:
                account_data[line['Value']]=line
        else:
            for key,value in account_data.items():
                if round(float(key),2)==round(float(result[data][-1]['TotalValue']),2):
                    if result[data]:
                        result_data[data]={'details':value,'description':result[data]}
                else:
                    if result[data]:
                        result_data[data]={'details_error':'error','description':result[data]}
    return result_data
        




# with open('C:/Users/roger/Downloads/shwetajohari.log','r') as file:
#     openfile=eval(file.read())
#     result=merge_data(openfile)
#     if check_total(result):
#         result_data=format(result)
#         with open('test2.log','w') as op:
#             json.dump(result_data,op,indent=4)
        

    
