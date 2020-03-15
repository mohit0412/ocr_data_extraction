import re


def corporate_bond(data):
    data_json={}
    data_json['record']=[]
    for index in range(len(data)):
        date_regex=r'([3][0-1]|[0-2][1-9])-[A-Z][a-z]{2}-[0-9]{4}'
        amount_regex=r'[0-9,]+[\.|-][0-9]+'
        isin_regex=r'IN[A-Z|0-9]+[0-9]'
        if re.search(isin_regex,data[index]):
            line=data[index:index+2][-1]
            pattern=date_regex+'\s([0-9]{1,3})\s'+amount_regex
            if re.search(pattern,line):
                if len(re.findall(amount_regex,line)) == 3:
                    val=re.findall(amount_regex,line)
                    temp={
                        'ISIN number': re.match(isin_regex,data[index]).group(),
                        'no of bonds': re.search(pattern,line).group(1),
                        'Maturity Date': re.search(date_regex,line).group(),
                        'Coupon Rate/Frequency': val[0],
                        'Face Value Per Bond in': val[1],
                        'Value in': val[2],
                        'bond type': re.search(r'\bFixed\s+Interest\s+Bonds\b',line).group()
                    }
                    line=re.sub(r'\bFixed\s+Interest\s+Bonds\b','',line)
                    line=re.sub(pattern,'',line)
                    line=re.sub(amount_regex,'',line)
                    line=re.sub(date_regex,'',line)
                    line=re.sub(r'\s\s+','',line)
                    temp['company name']=line
                    data_json['record'].append(temp)
                else:
                    print('entry with error')
    return(data_json)



def mutual_fund_extraction(mutual_fund):
    data_json={}
    data_json['record']=[]
    for index in range(len(mutual_fund)):
        amount_regex=r'[0-9,]+[\.|-][0-9]+'
        isin_regex=r'IN[A-Z|0-9]+[0-9]'
        if re.search(isin_regex,mutual_fund[index]):
            line=mutual_fund[index:index+2][-1]
            values=re.findall(r'\b[0-9,]+[\.|-][0-9]+\b',line)
            temp={
                'ISIN number': re.match(isin_regex,mutual_fund[index]).group(),
                'Folio No.':re.search(r'\b([0-9|A-Z]+)\s[0-9,]+[\.|-][0-9]{3}\b',line).group(1)  
            }
            if len(values)==2:
                temp['No. of Units']=values[0]
                temp['VALUE']=values[1]
            else:
                temp['No. of Units']=values[0]
                temp['NAV']=values[1]
                temp['VALUE']= values[2]
            line=re.sub(r'\b([0-9|A-Z]+)\s[0-9,]+[\.|-][0-9]{3}\b','',line)
            line=re.sub(r'\b[0-9,]+[\.|-][0-9]+\b','',line)
            temp['company name']=line
            data_json['record'].append(temp)
    return(data_json)


def duration(duration):
    for data in duration:
        date_regex=r'\b[0-9]{2}-[A-Z][a-z]{2}-[0-9]{4}\b'
        if re.search(date_regex,data):
            date_val=re.findall(date_regex,data)
            if len(date_val)==2:
                temp={
                    'from':date_val[0],
                    'to':date_val[1]
                }
    return temp


def details(details):
    temp={}
    for index in range(len(details)):
        if re.search(r'CAS ID:',details[index]):
            temp['CAS ID:']=re.sub(r'CAS ID:','',details[index]).strip()
        elif re.search(r'PINCODE',details[index]):
            temp['PINCODE:']=re.sub(r':','',details[index+1]).strip()
            break
        else:
            temp['Address']=' '.join([str(elem) for elem in details[index].split(' ')[2:]])
            temp['name']=' '.join([str(elem) for elem in details[index].split(' ')[0:2]]) 
    return(temp)













