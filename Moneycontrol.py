
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os,re
import json
import pickle
import requests
import numpy
from lxml import html

class Moneycontrol:
    def __init__(self):
        self.stocklisturl = "https://www.moneycontrol.com/india/stockpricequote/"
        self.latterurl = "https://www.moneycontrol.com/india/stockpricequote/{}"
        self.search = "https://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php?search_data=&cid=&mbsearch_str=&topsearch_type=1&search_str={}"
    def useragent(self):
        ua = UserAgent()
        hd = ua.ie
        header = {
            'Host': 'www.moneycontrol.com',
            'User-Agent': hd,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
            }
        return header

    def cokie(self):
        folder_name ='Temp_file' # this is folder name
        get_path = os.getcwd() # this is path where open programm
        create_path = os.path.join(get_path,folder_name) # create folder path
        try:
            os.mkdir(create_path)
        except FileExistsError:
            pass
        h = self.useragent()
        flist = os.listdir(create_path) # file list
        file = create_path+'\\moneycontrol' # create file path with name
        if 'moneycontrol' in flist:
            with open(file, 'rb')as op:
                cokie = pickle.load(op)
        else:
            page = requests.get('https://www.moneycontrol.com/', timeout=5, headers=h)
            cokie = page.cookies
            with open(file, 'wb')as op:
                pickle.dump(cokie, op)
        return cokie

    def web(self, url):
        get_path = os.getcwd()
        create_path = os.path.join(get_path,'Temp_file')
        file = create_path+'\\moneycontrol'
        c = self.cokie()
        h = self.useragent()
        while True:
            try:
                page1 = requests.get(url, cookies=c, headers=h, timeout=5)
                if str(page1)=='<Response [401]>':
                    os.remove(file)
                    c2 = self.cokie()
                    page = requests.get(url, cookies=c2, headers=h, timeout=5)
                    break
                else:
                    page = page1
                    break
            except:
                pass
        return page
    def findLatter(self,ticket):
        tk = ticket.upper()
        latter = tk[0]
        return latter
    
    def symbole(self,string):
        try:
            st = str(string).split(' ')
            for x in st:
                if x.startswith(':'):
                    snam = x.replace(':','')
                    if snam.isalpha():
                        name = snam
                    elif re.search(r'-',snam):
                        name = snam
            return name
        except:
            pass

    def linkDict(self,url):
        page = self.web(url)
        soup = BeautifulSoup(page.text,'html.parser')
        linkdt = {}
        for x in soup.find_all('td'):
            tagA = str(x.find('a'))
            if tagA != 'None':
                linksoup = BeautifulSoup(tagA,'html.parser')
                for y in linksoup:
                    ylink = y.get('href')
                    ytitle = (((y.text).replace('\t','')).replace('\n',''))
                    linkdt[ytitle]=ylink
            else:
                pass
        return linkdt

    def searchDict(self,url):
        page = self.web(url)
        soup = BeautifulSoup(page.text,'html.parser')
        linkdic = {}
        for x in soup.find_all('td'):
            if 'class="bl_18"'in str(x):
                tagA=x.find('a')
                link = tagA.get('href')
                name = tagA.text
                linkdic[name]=link
            else:
                if 'NSE Id' in str(x):
                    sym = self.symbole(x.text)
                    linkdic[sym]=linkdic.pop(name)
                else:
                    pass
        return linkdic
    
    def matchWord(self,ticket,stockname):
        ticket_list = []
        for x in ((ticket.replace(' ','')).upper()):
            ticket_list.append(ord(x))
        stockname_list = []
        for y in ((stockname.replace(' ','')).upper()):
            stockname_list.append(ord(y))
        matchlist = [x for x in ticket_list if x in stockname_list]
        result = all(map(lambda x, y: x == y, ticket_list, matchlist))
        if len(ticket_list)<len(stockname_list):
            if result :
                median_value = abs((numpy.median(ticket_list))-(numpy.median(stockname_list)))
                mean_value = abs((numpy.mean(ticket_list))-(numpy.mean(stockname_list)))
                std_value = abs((numpy.std(ticket_list))-(numpy.std(stockname_list)))
                if (mean_value<1)and(median_value<1)and(std_value<1):
                    rt = ticket
                else:
                    rt = None
            else:
                rt = None
        else:
            if result:
                notmatch = len([x for x in stockname_list if x not in ticket_list])
                std_value = abs((numpy.std(ticket_list))-(numpy.std(stockname_list)))
                if std_value<1 and notmatch==1 and abs(len(ticket)-len(stockname))==1:
                    rt = ticket
                else:
                    rt = None
            else:
                rt = None
        return rt

    def matchDic(self,dt,ticket):
        mdict ={}
        for x in dt:
            if x == '':
                pass
            else:
                key = self.matchWord(ticket,(x.upper()))
                if key==ticket:
                    value = dt[x]
                    mdict[key]=value
                else:
                    pass
        return mdict
    
    def upperDict(self,dt):
        try:
            udict ={}
            for x in dt:
                key = x.upper()
                value = dt[x]
                udict[key]=value
            return udict
        except:
            pass
##########################################
    def create_path(self):
        folder_name = 'Temp_file'  # this is folder name
        current_dir = os.getcwd()  # this is path
        path = os.path.join(current_dir, folder_name)  # create folder path
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        return path

    def creatname(self,url):
        nstr = (url.replace('https://','')).split('.')
        try:
            str1 = nstr[1]
            # remove any spacial charater 
            sr = (''.join(x for x in str1 if x.isalpha()))
        except IndexError:
            str1 = nstr[0]
            sr = (''.join(x for x in str1 if x.isalpha()))
        except :
            str1 = "Defult"
            sr = (''.join(x for x in str1 if x.isalpha()))
        return sr     
#####################################################
    def findLink(self,ticket):
        # tk = (((ticket.replace(' ','')).replace('.','')).replace('-','')).upper()
        tk = ticket.upper()
        try:
            defaultDict = self.upperDict(self.searchDict(self.search.format(ticket)))
            if tk in defaultDict:
                link = defaultDict[tk]
            else:
                latter = self.findLatter(ticket)
                latterDict = self.matchDic(self.linkDict(self.latterurl.format(latter)),ticket)
                if tk in latterDict:
                    link = latterDict[tk]
                else:
                    otherDict = self.upperDict(self.linkDict(self.latterurl.format('others')))
                    if tk in otherDict:
                        link = otherDict[tk]
                    else:
                        chakelist = self.upperDict(self.linkDict(self.stocklisturl))
                        if tk in chakelist:
                            link = chakelist[tk]
                        else:
                            link = None
        except:
            link = None
        return link
       
    

    def result (self,ticket):
        link = self.findLink(ticket)
        if link != None:
            page = self.web(link)
        else:
            page = self.web(self.search.format(ticket))
        return page


    
    def livePrice(self,ticket):
        page = self.result(ticket)
        soup = BeautifulSoup(page.text,'html.parser')
        price = soup.find(class_='inprice1 nsecp')
        try:
            return price.get_text()
        except:
            return price

# mc = Moneycontrol()
# print(mc.livePrice('BHARTIARTL'))
        

# import Nse
# nse = Nse.NseData()
# df = nse.nifty_50()
# co_name = df['SYMBOL'].iloc[2:50]
# # print(co_name)
# mc = Moneycontrol()
# for x in co_name:
#     print(x)
#     print(x,' = ',mc.livePrice(x))



# mc = Moneycontrol()
# print(mc.result('ABAN'))