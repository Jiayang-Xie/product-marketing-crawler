#-*- coding: utf-8 -*-
#import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv
import urllib.request
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
import random
import time
import csv
import lxml
import datetime
import matplotlib.pyplot as plt
from translate import Translator
## 01 input the table and extract the PMCID
import re
with open('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Miltenyi_MACS_China_last_5Y2.txt') as f:
    content = f.read()
pattern = r'PMCID: PMC(\d+)'
PMCID = re.findall(pattern,content)

with open('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_China_last 5Y_new.txt') as f:
    content = f.read()
pattern = r'PMCID: PMC(\d+)'
PMCID = re.findall(pattern,content)
'''
with open('pbmcid_output.txt','w') as f:
    for p in PMCID:
        f.write('PMC%s\n' % p)
'''  

##
agent_list = [
	"Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	"Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
	"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
	"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
	"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
	"Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
	]




## 02 get the target information according to the PMCID

from bs4 import BeautifulSoup
import csv
import lxml

#miltenyi[1707:]
if __name__=='__main__':
    for p in PMCID[3097:]:
        time.sleep(random.uniform(0.5, 2)) # 随机等待时间是0.5秒和1秒之间的一个小数
        url_var= 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC'+ str(p)
        #url_var= 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9295468'
        '''
        header_var = {"User-Agent":
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}
        '''
        header_var = {'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}#random.choice(agent_list)}
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))  # 访问http协议时，设置重传请求最多三次
        s.mount('https://', HTTPAdapter(max_retries=3))  # 访问https协议时，设置重传请求最多三次
        #s.config['keep_alive'] = False # keep the connection not alive 
        req = requests.get(url = url_var, headers = header_var)
        html = req.content.decode('utf-8')  
        #req.close()
        bes =BeautifulSoup(html,'lxml')
        
        pmc_id = 'PMC'+str(p) # 00 get the PMCID
        title = bes.find(attrs={'class': 'content-title'}).get_text().replace('\n','').replace('\r','') # 01 get the article title
        try:
            product = str(bes.find_all(string=re.compile('[Mm]iltenyi'))).replace('\n','').replace('\r','') # 02 get the related product
        except AttributeError:
            product = 'none'
        # get the author information
        author = bes.find('head').find_all(name='meta',attrs={'name':'citation_author'})
        if len(author) > 1:
            first_author = author[0].attrs['content']# 03 the first author
            second_author = author[1].attrs['content']# 04 the second author
            corauthor1 =author[-1].attrs['content'] # 05 the first corresponding author
            corauthor2 =author[-2].attrs['content'] # 06 the second corresponding author
        else:
            second_author = "none"# 04 the second author
            corauthor2 = "none" # 06 the second corresponding author
        #get the department information
        affiliation_all = bes.find_all(attrs={'class':'fm-affl'})
        affiliation1 = affiliation_all[0].get_text()    #07 the first affiliation
        #affiliation1 =bes.find(attrs={'id':'Aff1'}).get_text() #07 the first affiliation
        affiliation1 = affiliation1.replace('1','',1).replace('\n','').replace('\r','')
        affiliation1 = affiliation1.strip()
        if len(affiliation_all) > 1:
            affiliation2 = affiliation_all[1].get_text() 
            #affiliation2 =bes.find(attrs={'id':'Aff2'}).get_text() #08 the second affiliation
            affiliation2 = affiliation2.replace('2','',1).replace('\n','').replace('\r','')
        else:
            affiliation2 = "none"
        # get the received,accepted and published date information
        try:
             received =  bes.find(attrs={'class':'fm-pubdate half_rhythm'}).get_text().split(';')[0] #09 the received date  
             received = received.replace('Received','')
             accepted =  bes.find(attrs={'class':'fm-pubdate half_rhythm'}).get_text().split(';')[-1] #10 the accepted date  
             accepted = accepted.replace('Accepted','').replace('.','')   
        except AttributeError:
            received = 'none'
            accepted = 'none'
        try:
            published = bes.find(attrs={'class':'fm-vol-iss-date'}).get_text()
            published = published.replace('Published online','').replace('.','') # the published date
        except AttributeError:
            published = 'none' 
        try:
            doinumber = bes.find(attrs={'class':'doi'}).get_text()
        except AttributeError:
            doinumber = 'none' 
        journal = bes.find('head').find(attrs={'name':'citation_journal_title'})
        journal =journal.attrs['content']  # get the journal name
        result = [pmc_id,journal,title,doinumber,first_author,second_author,corauthor1,corauthor2,affiliation1,affiliation2,received,accepted,published,product] 
        print('the result is done')     
        with open("C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Miltenyi_MACS_China_last_5Y_result.txt","a" ) as f:
            for element in result:
                 f.write(element+';')
            f.write("\n")
        print('No.'+str(PMCID.index(p)) + ' test,the article PMC'+p+' was done!')   
        

### 2.1 add the email and other information or complement information        
    
 if __name__=='__main__':
    for p in PMCID[321:]:
        time.sleep(random.uniform(0.5, 2)) # 随机等待时间是0.5秒和1秒之间的一个小数
        url_var= 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC'+ str(p)
        #url_var= 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9295468'
        '''
        header_var = {"User-Agent":
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}
        '''
        header_var = {'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}#random.choice(agent_list)}
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))  # 访问http协议时，设置重传请求最多三次
        s.mount('https://', HTTPAdapter(max_retries=3))  # 访问https协议时，设置重传请求最多三次
        #s.config['keep_alive'] = False # keep the connection not alive 
        req = requests.get(url = url_var, headers = header_var)
        html = req.content.decode('utf-8')  
        #req.close()
        bes =BeautifulSoup(html,'lxml')
        
        pmc_id = 'PMC'+str(p) # 00 get the PMCID
        try:
            email1 = bes.find(attrs={'class':'oemail'}).get_text()
        except AttributeError:
            doinumber = 'none' 
        result = [pmc_id,email1]      
        with open("C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_STEMCELL_MACS_China_last_5Y_email.txt","a" ) as f:
            for element in result:
                 f.write(element+';')
            f.write("\n")
        print('No.'+str(PMCID.index(p)) + ' test,the article PMC'+p+' was done!')      
    

####  test and verify block #################################

if __name__=='__main__':
        url_var= 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4643994'
        header_var = {"User-Agent":
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"}
        req = requests.get(url = url_var, headers = header_var)
        html = req.content.decode('utf-8')  
        bes =BeautifulSoup(html,'lxml')
        
        pmc_id = 'PMC9563191'#+str(p) # 00 get the PMCID
        
        title = bes.find(attrs={'class': 'content-title'}).get_text().replace('\n','').replace('\r','') # 01 get the article title
        product = str(bes.find_all(string=re.compile('[Mm]iltenyi'))) # 02 get the related product
        # get the author information
        author = bes.find('head').find_all(name='meta',attrs={'name':'citation_author'})
        first_author = author[0].attrs['content']# 03 the first author
        second_author = author[1].attrs['content']# 04 the second author
        corauthor1 =author[-1].attrs['content'] # 05 the first corresponding author
        corauthor2 =author[-2].attrs['content'] # 06 the second corresponding author
        #get the department information
        affiliation_all = bes.find_all(attrs={'class':'fm-affl'})
        affiliation1 = affiliation_all[0].get_text()    #07 the first affiliation
        #affiliation1 =bes.find(attrs={'id':'Aff1'}).get_text() #07 the first affiliation
        affiliation1 = affiliation1.replace('1','',1).replace('\n','').replace('\r','')
        if len(affiliation_all) > 1:
            affiliation2 = affiliation_all[1].get_text() 
            #affiliation2 =bes.find(attrs={'id':'Aff2'}).get_text() #08 the second affiliation
            affiliation2 = affiliation2.replace('2','',1).replace('\n','').replace('\r','')
        else:
            affiliation2 = "none"
        # get the received,accepted and published date information
        received =  bes.find(attrs={'class':'fm-pubdate half_rhythm'}).get_text().split(';')[0] #09 the received date  
        received = received.replace('Received','')
        accepted =  bes.find(attrs={'class':'fm-pubdate half_rhythm'}).get_text().split(';')[-1] #10 the accepted date  
        accepted = accepted.replace('Accepted','').replace('.','')
        published = bes.find(attrs={'class':'fm-vol-iss-date'}).get_text()
        published = published.replace('Published online','').replace('.','') # the published date  
        doinumber = bes.find(attrs={'class':'doi'}).get_text()
        
        journal = bes.find('head').find(attrs={'name':'citation_journal_title'})
        journal =journal.attrs['content']  # get the journal name
        
        result = [pmc_id,journal,title,doinumber,first_author,second_author,corauthor1,corauthor2,affiliation1,affiliation2,received,accepted,published,product] 
        print('the result is done')   
        with open("C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Miltenyi_MACS_China_last_5Y_result_test.txt","a" ) as f:
            for element in result:
                 f.write(element+';')
            f.write("\n")
        print('No.'+str(PMCID.index(p)) + ' test,the article PMC'+p+' was done!') 

### 03 convert the result from txt to csv format


txt_miltenyi = 'C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Miltenyi_MACS_China_last_5Y_result_final.txt'
txt_stemcell ='C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_China_last 5Y_new_result_final.txt'

csv_miltenyi = 'C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Miltenyi_MACS_China_result.csv'
csv_stemcell = 'C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_China_result.csv'

# clean the result




with open(txt_miltenyi, 'r') as txt_file,open(csv_miltenyi,'w',newline='') as csv_file:
    # get the information from txt row by row
    for line in txt_file:
        #the ';' separate the line 
        filed = line.strip().split(r';')
        csv_file.write(';'.join(filed)+'\n')

# another method to do the covert
import pandas as pd

df = pd.read_csv(txt_miltenyi,delimiter=';')
df.columns = ['PMCID', 'journal','title','doinumber,','1st_author','2nd_author','1stcor_author','2ndcor_author','1st_affiliation','2nd_affiliation',
              'received','accepted','publishd','product']   
df.to_csv(csv_miltenyi,index=None,encoding='utf-8-sig')


if __name__=='__main__':
    def remove_upprintable_chars(p):
        return ''.join(x for x in p if x.isprintable())
    with open(txt_stemcell, 'r') as txt_file,open("C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_China_last 5Y_new_result_final.txt","a" ) as f:
        for line in txt_file:
            filed = line.strip().split(';')
            while '' in filed:
                filed.remove('')
            filed[3] = remove_upprintable_chars(filed[3])
            product= filed[13:]
            product= [s.replace("(",'!').replace(')','!').replace("'","").replace('"','').replace('–','-') for s in product]
            product = remove_upprintable_chars(product)
            #product = eval(''.join(str(i)for i in product))
            product = str(product).replace(';',',')
            filed = filed[0:13]
            filed.append(str(product))
            for element in filed:
                f.write(element+';')
            f.write("\n")
        txt_file.close()



## test and verify block #################################################################

if __name__=='__main__':
    def remove_upprintable_chars(p):
        return ''.join(x for x in p if x.isprintable())  
    with open(txt_miltenyi, 'r') as txt_file,open("C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Miltenyi_MACS_China_last_5Y_result_text.txt","a" ) as f:
        filed= txt_file.readlines()[18]
        filed = filed.strip().split(';')
        txt_file.close()
        while '' in filed:
            filed.remove('')
        print(filed)
        filed[3] = remove_upprintable_chars(filed[3])
        product= filed[13:]
        product= [s.replace("(",'!').replace(')','!').replace("'","").replace('"','').replace('–','-') for s in product]
        product = remove_upprintable_chars(product)
        #product = eval(''.join(str(i)for i in product))
        product = str(product).replace(';',',')
        filed = filed[0:13]
        filed.append(str(product))
        for element in filed:
            f.write(element+';')
        f.write("\n")
                

if __name__=='__main__':
    def remove_upprintable_chars(p):
        return ''.join(x for x in p if x.isprintable())
    with open(txt_stemcell, 'r') as txt_file,open("C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_China_last 5Y_new_result_test.csv","w",newline='',
                                                  encoding='utf-8-sig') as f:
        writer = csv.writer(f,delimiter=';')
        for line in txt_file:
            filed = line.strip().split(';')
            while '' in filed:
                filed.remove('')
            filed[3] = remove_upprintable_chars(filed[3])
            product= filed[13:]
            product= [s.replace("(",'!').replace(')','!').replace("'","").replace('"','').replace('–','-') for s in product]
            product = remove_upprintable_chars(product)
            #product = eval(''.join(str(i)for i in product))
            product = str(product).replace(';',',')
            filed = filed[0:13]
            filed.append(str(product))
            writer.writerow(filed)
        txt_file.close()

##### 04 data cleanup #####

df = pd.read_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_China_result.csv',sep=',',encoding='utf-8',header=0)

# 4.1 remove the characters of the time
df['accepted'] = df['accepted'].str.strip(' ')
df['revised'] = df['revised'].str.strip(' ')
df['published'] = df['published'].str.strip(' ')

# construct the date format for converting to the datetime
df['accepted'] = df['accepted'].str.replace(' ','-')
df['accepted'] = df['accepted'].str.pad(9,side='right',fillchar='-')
df['accepted'] = df['accepted'].str.pad(10,side='right',fillchar='1')
# revised
df['revised'] = df['revised'].str.replace(' ','-')
df['revised'] = df['revised'].str.pad(9,side='right',fillchar='-')
df['revised'] = df['revised'].str.pad(10,side='right',fillchar='1')
# published
df['published'] = df['published'].str.replace(' ','-')
df['published'] = df['published'].str.pad(9,side='right',fillchar='-')
df['published'] = df['published'].str.pad(10,side='right',fillchar='1')
#convert to the datetime
df['accepted'] =pd.to_datetime(df['accepted'],format='%Y-%b-%d',errors='coerce')  
df['revised'] = pd.to_datetime(df['revised'],format='%Y-%b-%d',errors='coerce') 
df['published'] =pd.to_datetime( df['published'],format='%Y-%b-%d',errors='coerce')  
# add a year column(published)
df['year'] = df['published'].dt.year

df.to_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test1.csv',index=None,encoding='utf-8-sig')

##### 4.2 location and affiliation extraction#####
## 4.2.1 translate the location to chinese##
## translator module##
def translate_text(text):
    translator = Translator(to_lang="zh")
    translation = translator.translate(text)
    return translation
print(Translator(from_lang="en",to_lang="zh").translate(df.iloc[6,8]))
df['单位'] = df['affiliation1'].map(translate_text)
word1 = Translator(from_lang="en",to_lang="zh").translate(df.iloc[6:19,8])

## baidu translate api##
import requests
import random
import json
from hashlib import md5
# set you own appid/appkey
appid = '20240506002043427'
appkey = 'd6t3rzfatB7UHik0VXOI'

from_lang ='en'
to_lang ='zh'

endpoint ='http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path
query ='this is a test sentence'
# generate salt and sign
def make_md5(s,encoding ='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def baidu_api(query,from_lang,to_lang):
    salt =random.randint(37268,65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    #build requests
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    #send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    #print(json.dumps(result, indent=4, ensure_ascii=False))
    return result["trans_result"][0]['dst']
# translate 

df['单位'] = df['affiliation1'].apply(lambda x: baidu_api(str(x),from_lang='en',to_lang='zh'))


word1 = df.iloc[17:20,8].apply(lambda x: baidu_api(str(x),from_lang='en',to_lang='zh'))
word1 = df.iloc[17:20,8].apply(baidu_api(str(df.iloc[17:20,8]),from_lang='en',to_lang='zh'))
print(word1)
df.to_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test1.csv',index=None,encoding='utf-8-sig')

df = pd.read_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test1.csv',sep=',',encoding='utf-8',header=0)
### 4.2.2 split the location 
import cpca
import jionlp as jio
df['单位1'] = df['单位'] .str.replace(',','')
df['单位1'] = df['单位1'] .str.replace('，','')
df['单位1'] = df['单位1'] .str.replace('、','')
df['单位1'] = df['单位1'] .str.strip(' ')
#df = cpca.transform(df.iloc[0:5,16])

provin =[]
city1 =[]
county1=[]
for i in df['单位1']:
    loca = jio.parse_location(i)
    provin.append(loca['province'])
    city1.append(loca['city'])
    county1.append(loca['county'])
df['省份'] = provin
df['市'] = city1
df['区'] = county1
df.to_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test2.csv',index=None,encoding='utf-8-sig')

## 05 extract the target reagent
df['产品'] = df['product'].str.extract(r'([Ee]asy[Ss]ep.{0,35})',expand=True)

df.to_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test3.csv',index=None,encoding='utf-8-sig')

### insert the email information into the datasheet
df = pd.read_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test3.csv',sep=',',encoding='utf-8',header=0)
df_email = pd.read_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_STEMCELL_MACS_China_last_5Y_email.txt',sep=';',encoding='utf-8',header=None,names=['PMCID','email','none'])
df_email = df_email.iloc[:,0:2]
df_email['email'] = df_email['email'].apply(lambda x: x[::-1])
df1 =pd.merge(df_email,df, on='PMCID')
df1.to_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test4.csv',index=None,encoding='utf-8-sig')
df1 = pd.read_csv('C:/Users/jiayangx/Desktop/marketing/digital mapping/PMC_Stemcell_EasySep_test4.csv',sep=',',encoding='utf-8',header=0)



###05 datavisualization####
## 5.1 pie chart of the affiliation of different provinces
# 假设 df 是你的 DataFrame，包含一个名为 'category' 的列
df1 = df1.dropna(subset=['省份'])
# 统计每个类别的数量
category_counts = df1['省份'].value_counts()

# 取排名前9的类别
top_9_categories = category_counts.head(9)

# 计算其余类别的数量
other_count = category_counts[9:].sum()

# 将其余类别的数量添加到排名前9的类别中，构建新的 Series
top_categories = pd.concat([top_9_categories, pd.Series({'其他': other_count})])

# 绘制扇形图
plt.figure(figsize=(8, 8))
top_categories.plot(kind='pie', autopct='%1.1f%%',labels= top_categories.index)
plt.title('Top 9 Categories and Others')
plt.ylabel('')  # 去除y轴标签
plt.show()

##5.2 bar chart of the publish time course
# Count occurrences of each year
year_counts = df['year_column'].value_counts().sort_index()

# Create a bar chart
plt.figure(figsize=(10, 6))  # Set the size of the figure
year_counts.plot(kind='bar', color='skyblue')  # Plot a bar chart
plt.title('Occurrences of Years')  # Set the title of the plot
plt.xlabel('Year')  # Set the label for the x-axis
plt.ylabel('Count')  # Set the label for the y-axis
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid lines for the y-axis
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()  # Display the plot
