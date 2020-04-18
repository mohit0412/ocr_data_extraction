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
            if 'extra' in result.keys():
                result['extra']+=[dictionary]
            else:
                result['extra']=[dictionary]
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
                    



# with open('C:/Users/roger/Downloads/shwetajohari.log','r') as file:
#     openfile=eval(file.read())
#     result=merge_data(openfile)
#     with open('test2.log','w') as op:
#         json.dump(result,op,indent=4)
