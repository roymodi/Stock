import Webscraping
from bs4 import BeautifulSoup
import os
import json

class Moneycontrol:
    def __init__(self):
        self.stocklisturl = "https://www.moneycontrol.com/india/stockpricequote/"
        self.latterurl = "https://www.moneycontrol.com/india/stockpricequote/{}"
        self.stockurl = "https://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php?search_data=&cid=&mbsearch_str=&topsearch_type=1&search_str={}"
    
    def findLatter(self,ticket):
        tk = ticket.upper()
        latter = tk[0]
        return latter

    def linkDict(self,url):
        wbs = Webscraping.Webscraping()
        page = wbs.webpage(url)
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

    def stockList(self,dt):
        stocklist = []
        for x in dt:
            stocklist.append(x)
        return stocklist
    
    def upperDict(self,dt):
        udict ={}
        for x in dt:
            key = ((((x).replace(' ','')).replace('.','')).replace('-','')).upper()
            value = dt[x]
            udict[key]=value
        return udict


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
        tk = (((ticket.replace(' ','')).replace('.','')).replace('-','')).upper()
        latter = self.findLatter(ticket)
        defaultDict = self.upperDict(self.linkDict(self.stocklisturl))
        returnlist = []
        if tk in defaultDict:
            link = defaultDict[tk]
        else:
            latterDict = self.upperDict(self.linkDict(self.latterurl.format(latter)))
            if tk in latterDict:
                link = latterDict[tk]
            else:
                otherDict = self.upperDict(self.linkDict(self.latterurl.format('others')))
                if tk in otherDict:
                    link = otherDict[tk]
                else:
                    chakelist = self.linkDict(self.stockurl.format(ticket))
                    returnlist.extend(self.stockList(chakelist))
                    link = returnlist
        return link
    

    "Don't Delete"
    # def result (self,ticket):
    #     res = self.findLink(ticket)
    #     if type(res) is list:
    #         for x in res:
    #             print(x)
    #     else:
    #         return res
    #