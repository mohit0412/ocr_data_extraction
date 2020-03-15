import re
import test

def extract_data_nsdl(data):
    result=[]
    range_index=2
    for index in range(len(data)):
        if re.search(r'CAS ID',data[index]):
            result.append(['details']+[data[index]]+re.split(r'(PINCODE)',data[index:index+range_index][-1]))
            #result.append(test.details(['details']+[data[index]]+re.split(r'(PINCODE)',data[index:index+range_index][-1])))
        elif re.search(r'Statement for the period',data[index]):
            result.append(['duration']+[data[index]])
            #result.append(test.duration(['duration']+[data[index]]))
        elif re.search(r'Account Type Account Details',data[index]):
            result.append(['account type']+re.split(r'([0-9]+,[0-9|,]+\.[0-9]{2,4})',data[index:index+range_index][-1]))
        elif re.search(r'ISIN Description|UCC Units Cost',data[index]):
            #result.append(['mutual funds']+data[index:index+range_index])
            result.append(['mutual funds']+re.split(r'(IN[A-Z|0-9]+[0-9])',data[index:index+range_index][-1]))
            #result.append(test.mutual_fund_extraction(['mutual funds']+re.split(r'(IN[A-Z|0-9]+[0-9])',data[index:index+range_index][-1])))
        elif re.search(r'Company Name',data[index]):
            if re.search(r'[0-9]{2}-[A-Z][a-z]{2}-[0-9]{4}',data[index:index+range_index][-1]):
                #result.append(['corporate bond']+data[index:index+range_index])
                result.append(['corporate bond']+re.split(r'(IN[A-Z|0-9]+[0-9])|Page',data[index:index+range_index][-1]))
                #result.append(test.corporate_bond(['corporate bond']+re.split(r'(IN[A-Z|0-9]+[0-9])|Page',data[index:index+range_index][-1])))
            else:
                result.append(['other share']+re.split(r'(IN[A-Z|0-9]+[0-9])|Page',data[index:index+range_index][-1]))
                #result.append(test.mutual_fund_extraction(['other share']+re.split(r'(IN[A-Z|0-9]+[0-9])|Page',data[index:index+range_index][-1])))
        elif re.search(r'Total',data[index]):
            result.append(['Total']+[data[index]])
    return result


def extract_data(file_name='new_result.txt'):
    data={}
    data['record']=[]
    count=1
    date_regex=r'^\d{2}-[A-Z][a-z]{2}-\d{4}|^\d{2}\.\d{2}\.\d{2}|^\d{2}\-[A-Z]{3}\-\d{4}'
    for line in result.split('\n'):
        date=''
        if re.search(date_regex,line):
            date=re.search(date_regex,line).group()
            line=re.sub(date_regex,'',line)
            amount=re.findall(r'[\(\d]+\.\s[\)\d]+|[\d\(]+\.\d+\s[\d\)]$|[\(\d,]+?[\.\,\d\)]+',line)
            if len(amount)>=4:
                data['record'].append({
                    'count': count,
                    'DATE': date.strip(),
                    'Transaction': str(line.split(amount[-4])[0]).strip(),
                    'Amount': str(amount[-4]).strip(),
                    'Units': str(amount[-3]).strip(),
                    'Price': str(amount[-2]).strip(),
                    'Unit': str(amount[-1]).strip()
                })
                count+=1
    with open(file_name+'_'+str(count-1)+'.log', 'w') as outfile:
        json.dump(data, outfile,indent=4)
    return count


def read_hpi(File_data):
    count=0
    result_data=[]
    prev_heading=''
    neg=False
    #word=r'ISIN Description|Total$|End of Statement|CAS ID|Statement for the period'
    word=r'Notes:|PORTFOLIO VALUE|Note:|CAS ID|Statement for the period|Total|Account Type Account Details|ISIN Description|Company Name|Transactions|UCC Units Cost'    
    k = re.compile(word)  
    current_heading=False
    data=''
    for line in File_data:
        count=count+1
        line=line.strip()
        if re.search(k,line):
            if not current_heading:
                current_heading=True
            else:
                if data.strip() and not neg:
                    result_data.append(data.strip())
                #print(data)
            data=''
            #print('................found........................',line) 
            if current_heading:
                word_neg='End of Statement|Notes:|Note:|Total|Transactions'#TOTAL$|
                k2 = re.compile(word_neg, re.I) 
                if re.search(k2,line):
                    neg=True
                else:
                    if prev_heading!=line.strip():
                        result_data.append(line.strip())
                    prev_heading=line.strip()
                    neg=False
        elif current_heading and len(File_data)==count and not neg:
            result_data.append(data.strip())
        else:
            data=data+line+' '
    return(result_data)