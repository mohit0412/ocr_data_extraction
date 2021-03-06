import re


def corporate_bond(data):
    data_json={}
    data_json['corporate bond']=[]
    Flag=True
    data_json['corporate_details']=[]
    sum_val=0
    count=0
    for index in range(len(data)):
        date_regex=r'([3][0-1]|[0-2][0-9])-[A-Z][a-z]{2}-[0-9]{4}'
        amount_regex=r'[0-9,]+[\.|-][0-9]+'
        isin_regex=r'IN[A-Z|0-9]+[0-9]'
        if re.search(isin_regex,data[index]):
            Flag=False
            line=data[index:index+2][-1]
            pattern=date_regex+'\s([0-9]{1,3})\s'+amount_regex
            if re.search(pattern,line):
                if len(re.findall(amount_regex,line)) == 3:
                    val=re.findall(amount_regex,line)
                    sum_val=sum_val+float(re.sub(r',','',val[2]))
                    temp={
                        'Isin': re.match(isin_regex,data[index]).group(),
                        'no of bonds': re.search(pattern,line).group(1),
                        'MaturityDate': re.search(date_regex,line).group(),
                        'Coupon Rate/Frequency': val[0],
                        'FaceValue': val[1].replace(',',''),
                        'Value in': val[2].replace(',',''),
                        'bond type': re.search(r'\bFixed\s+Interest\s+Bonds\b',line).group()
                    }
                    line=re.sub(r'\bFixed\s+Interest\s+Bonds\b','',line)
                    line=re.sub(pattern,'',line)
                    line=re.sub(amount_regex,'',line)
                    line=re.sub(date_regex,'',line)
                    line=re.sub(r'\s\s+','',line)
                    temp['CompanyName']=line
                    count=count+1
                    data_json['corporate bond'].append(temp)
                else:
                    print('entry with error')
                    raise
        elif re.search(date_regex,data[index]) and Flag:
            print('error occured in corporate bond')
            raise
    data_json['corporate_details'].append({'TotalCorporateBond':count,'TotalValue':sum_val})
    return(data_json)



def mutual_fund_extraction(mutual_fund):
    data_json={}
    data_json['mutual funds']=[]
    data_json['mutual_details']=[]
    sum_val=0
    count=0
    for index in range(len(mutual_fund)):
        amount_regex=r'[0-9,]+[\.|-][0-9]+'
        isin_regex=r'IN[A-Z|0-9]+[0-9]'
        if mutual_fund[index] and re.search(isin_regex,mutual_fund[index]):
            line=mutual_fund[index:index+2][-1]
            values=re.findall(r'-?[0-9,]+[\.|-][0-9|\.]+',line)
            temp={
                'Isin': re.match(isin_regex,mutual_fund[index]).group()
            }
            if re.search(r'\b([0-9|A-Z]+)\s[0-9,]+[\.|-][0-9]{3}\b',line):
                temp['FolioNumber']=re.search(r'\b([0-9|A-Z]+)\s[0-9,]+[\.|-][0-9]{3}\b',line).group(1)
            if len(values)==7 or len(values)==6 or len(values)==8:
                temp['NumberOfUnits']=values[0].replace(',','')
                temp['AverageCostPerUnits']=values[1]
                temp['InvestmentValue']=values[2].replace(',','')
                temp['current nave']=values[3]
                temp['Value']=values[4].replace(',','')
                sum_val=sum_val+float(re.sub(r',','',values[4]))
                temp['Unrealised Profit/(Loss)']=values[5]
                if len(values)==7:
                    temp['Annualised return']=values[6]
            elif len(values)==4:
                temp['No. of Units']=values[0].replace(',','')
                temp['total cost']=values[1]
                temp['current value']=values[2]
                sum_val=sum_val+float(re.sub(r',','',values[2]))
                temp['Unrealised Profit/(Loss)']=values[3]
            elif len(values)==2:
                temp['No. of Units']=values[0].replace(',','')
                temp['VALUE']=values[1]
                sum_val=sum_val+float(re.sub(r',','',values[1]))
            elif len(values)==3:
                temp['No. of Units']=values[0].replace(',','')
                temp['NAV']=values[1]
                temp['VALUE']= values[2]
                sum_val=sum_val+float(re.sub(r',','',values[2]))
            else:
                print('entry with error')
                raise
            line=re.sub(r'\b([0-9|A-Z]+)\s[0-9,]+[\.|-][0-9]{3}\b','',line)
            line=re.sub(r'-?[0-9,]+[\.|-][0-9|\.]+','',line)
            temp['IsinName']=line
            count=count+1
            data_json['mutual funds'].append(temp)
    data_json['mutual_details'].append({'TotalMutualFund':count,'TotalValue':sum_val})
    return(data_json)


def duration(duration):
    temp={}
    for data in duration:
        date_regex=r'\b[0-9]{2}-[A-Z][a-z]{2}-[0-9]{4}\b'
        if re.search(date_regex,data):
            date_val=re.findall(date_regex,data)
            if len(date_val)==2:
                temp['StatementPeriod']={
                    'from':date_val[0],
                    'to':date_val[1]
                }
    return temp


def details(details):
    temp={}
    for index in range(len(details)):
        if re.search(r'CAS ID:',details[index]):
            temp['CAS ID:']=re.sub(r'CAS ID','',details[index]).strip()
        elif re.search(r'PINCODE',details[index]):
            temp['PINCODE']=re.sub(r':','',details[index+1]).strip()
            break
        else:
            temp['Address']=' '.join([str(elem) for elem in details[index].split(' ')[2:]])
            temp['name']=' '.join([str(elem) for elem in details[index].split(' ')[0:2]])
    return(temp)


def account_type(details):
    string=''
    Flag=False
    temp={}
    data_json={}
    data_json['AccountInfo']=[]
    data_json['account_details']=[]
    sum_val=0
    count=0
    for data in details[1:]:
        if data:
            if re.search(r'([\w]+\sDemat Account)|(Mutual Fund Folios)',data):
                Flag=True
                temp['AccountType']=re.search(r'([\w]+\sDemat Account)|(Mutual Fund Folios)',data).group()
            elif re.search(r'([0-9]+,[0-9|,]+\.[0-9]{2,4})|([0-9]+\.[0-9]{2,4})',data):
                temp['Value']=data.replace(',','')
                sum_val=sum_val+float(re.sub(r',','',data))
                #string+=' '+data
                string=re.sub(r'\s\s+',' ',string)
                string=string.strip()
                temp['No of isin']=re.findall('\d+',string)[-1]
                if re.search(r'([A-z|0-9]+)?\s+?Client?\s+[I|1]D\:?\s?([0-9]+)',string):
                    temp['ClientID']=re.search(r'([A-z|0-9]+)?\s+?Client?\s+[I|1]D\:?\s?([0-9]+)',string).group(2)
                    temp['DpID']=re.sub(r'1N','IN',re.search(r'([A-z|0-9]+)?\s+?Client?\s+[I|1]D\:?\s?([0-9]+)',string).group(1))
                    string=re.sub(r'([A-z|0-9]+)?\s+?Client?\s+[I|1]D\:?\s?([0-9]+).*',' ',string)
                temp['AccountDetails']=string
                count=count+1
                data_json['AccountInfo'].append(temp)
                temp={}
                string=''
            else:
                string+=' '+data
    data_json['account_details'].append({'TotalAccount':count,'GrandTotal':sum_val})
    return(data_json)


def get_val(val):
    data_val=[]
    for list_point in val:
        for point in list_point:
            if point:
                data_val.append(point)
    return(data_val)


def equity(data):
    data_json={}
    data_json['equity']=[]
    data_json['equity_details']=[]
    sum_val=0
    count=0
    for index in range(len(data)):
        amount_regex=r'([0-9]+,[0-9|,]+\.[0-9]{2,4}|[0-9]+\.[0-9]{2,4})\s([0-9|,]+)\s([0-9]+,[0-9|,]+\.[0-9]{2,4}|[0-9]+\.[0-9]{2,4})|([0-9|,]+\.[0-9]{2,4})'
        isin_regex=r'IN[A-Z|0-9]+[0-9]'
        temp={}
        if data[index] and re.search(isin_regex,data[index]):
            temp['ISIN number']=re.match(isin_regex,data[index]).group() 
            line=data[index:index+2][-1]
            if re.search(amount_regex,line):
                val=re.findall(amount_regex,line)
                if len(get_val(val))==4:
                    para=get_val(val)
                    temp['Face value']=para[0]
                    temp['no of share']=para[1]
                    temp['market price']=para[2]
                    temp['value in']=para[3]
                    sum_val=sum_val+float(re.sub(r',','',para[3]))
                    line=re.sub(amount_regex,'',line)
                    line=re.sub(r'\s\s+',' ',line)
                    temp['company name']=line
                elif len(get_val(val))==2:
                    if re.search(r'See Note',line):
                        line=re.sub(r'See Note','',line)
                        line=re.sub(r'\s\s+',' ',line)
                        if len(get_val(re.findall(amount_regex,line)))==3:
                            para2=get_val(re.findall(amount_regex,line))
                            temp['Face value']=para2[0]
                            temp['no of share']=para2[1]
                            temp['market price']='See Note'
                            temp['value in']=para2[2]
                            sum_val=sum_val+float(re.sub(r',','',para2[2]))
                            temp['company name']=line
                    else:
                        print('error in entry')
                        raise
                else:
                    print('error in equity')
                    raise
                count=count+1
                data_json['equity'].append(temp)
    data_json['equity_details'].append({'Totalequitycount':count,'TotalValue':sum_val})
    return(data_json)


def equity_type_2(data):
    data_json={}
    data_json['equity_2_type']=[]
    data_json['equity_2_type_details']=[]
    sum_val=0
    count=0
    for index in range(len(data)):
        amount_regex=r'([0-9]+,[0-9|,]+\.[0-9]{2,4}|[0-9]+\.[0-9]{2,4})\s([0-9|,]+)\s([0-9]+,[0-9|,]+\.[0-9]{2,4}|[0-9]+\.[0-9]{2,4})|([0-9|,]+\.[0-9]{2,4})'
        isin_regex=r'IN[A-Z|0-9]+[0-9]'
        temp={}
        if data[index] and re.search(isin_regex,data[index]):
            temp['ISIN number']=re.match(isin_regex,data[index]).group() 
            line=data[index:index+2][-1]
            if re.search(r'-?[0-9,]+[\.|-][0-9|\.]+',line):
                amount=re.findall(r'-?[0-9,]+[\.|-][0-9|\.]+',line)
                if len(amount)>5:
                    temp['current bal']=amount[0]
                    temp['safkeep bal']=amount[1]
                    temp['pledged bal']=amount[2]
                    temp['market price']=amount[3]
                    temp['value']=amount[4]
                    sum_val=sum_val+float(re.sub(r',','',amount[4]))
                    line=re.sub(r'-?[0-9,]+[\.|-][0-9|\.]+','',line)
                    temp['security']=line
                else:
                    print('error in security')
                    raise
                count=count+1
                data_json['equity_2_type'].append(temp)
    data_json['equity_2_type_details'].append({'totalequitycount':count,'TotalValue':sum_val})
    return(data_json)


def corporate_bond_type_2(data):
    data_json={}
    data_json['corporate_2_type bond']=[]
    data_json['corporate_2_type_details']=[]
    sum_val=0
    count=0
    for index in range(len(data)):
        date_regex=r'([3][0-1]|[0-2][0-9])-[A-Z][a-z]{2}-[0-9]{4}'
        amount_regex=r'[0-9,]+[\.|-][0-9]+'
        isin_regex=r'IN[A-Z|0-9]+[0-9]'
        temp={}
        if data[index] and re.search(isin_regex,data[index]):
            temp['Isin']=re.match(isin_regex,data[index]).group()
            amount=' '.join(map(str, data[index-2:index]))
            pattern=date_regex+'\s([0-9]{1,3})\s'+amount_regex
            if re.search(amount_regex,amount) and re.search(date_regex,amount):
                temp['MaturityDate']=re.search(date_regex,amount).group()
                amount_val=re.findall(amount_regex,amount)
                if len(amount_val)==3 or len(amount_val)==2:
                    line=' '.join(map(str, data[index+1:index+2]))
                    if len(amount_val)==3:
                        temp['Coupon Rate/Frequency']=amount_val[0]
                        temp['FaceValue']=amount_val[1].replace(',','')
                        temp['Value']=amount_val[2].replace(',','')
                        sum_val=sum_val+float(re.sub(r',','',amount_val[2]))
                    else:
                        temp['FaceValue']=amount_val[0]
                        temp['Value']=amount_val[1]
                        sum_val=sum_val+float(re.sub(r',','',amount_val[1]))
                    if re.search(r'\bFixed\s+Interest\s+Bonds\b',line):
                        temp['Interest']=re.search(r'\bFixed\s+Interest\s+Bonds\b',line).group()
                    line=re.sub(r'\bFixed\s+Interest\s+Bonds\b','',line)
                    temp['CompanyName']=line
                else:
                    print('data error')
                    raise
            count=count+1
            data_json['corporate_2_type bond'].append(temp)
    data_json['corporate_2_type_details'].append({'TotalCorporateBond':count,'TotalValue':sum_val})
    return(data_json)