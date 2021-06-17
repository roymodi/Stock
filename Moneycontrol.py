from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os,re
import json
import pickle
import requests
import re

class Moneycontrol:
    def __init__(self):
        self.sug_url = "https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php?classic=true&query={}&type=1&format=json&callback=suggest1"
        self.latterurl = "https://www.moneycontrol.com/india/stockpricequote/{}"

    def create_path(self):
        folder_name = 'Temp_file'  # this is folder name
        current_dir = os.getcwd()  # this is path
        path = os.path.join(current_dir, folder_name)  # create folder path
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        return path
    
    def useragent(self):
        ua = UserAgent()
        hd = ua.ie
        header = {
            'Host': 'www.moneycontrol.com',
            'Origin':'https://www.moneycontrol.com',
            'Referer':'https://www.moneycontrol.com/',
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
        h = self.useragent()
        flist = os.listdir(self.create_path()) # file list
        file = self.create_path()+'\\moneycontrol' # create file path with name
        if 'moneycontrol' in flist:
            with open(file, 'rb')as op:
                cokie = pickle.load(op)
        else:
            page = requests.get('https://www.moneycontrol.com/', timeout=5, headers=h)
            cokie = page.cookies
            with open(file, 'wb')as op:
                pickle.dump(cokie, op)
        return cokie
    
    def web(self,url,host='None'):
        file = self.create_path()+'\\moneycontrol'
        c = self.cokie()
        if host == 'None':
            h = self.useragent()
        else:
            h = self.useragent()
            h['Host'] = 'priceapi.moneycontrol.com'
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
    
    def find_id(self,link):
        def filter_id_(id_):
            sh = re.search('amp;',id_)
            if sh != None:
                idd = id_.replace('amp;','')
            else:
                idd = id_
            return idd
        try:
            page = self.web(link)
            tag = re.search('inditrade', page.text)
            span1 = (tag.span())[0]
            span2 = ((tag.span())[1])+97
            line = (page.text)[span1:span2]
            nseid = filter_id_((line.split("'"))[1])
            mcid = (line.split("'"))[3]
            return nseid,mcid,page
        except:
            pass
    
    def suggestion(self,ticket):
        page = self.web(self.sug_url.format((ticket.upper())))
        tup_page = (eval((page.text).replace('suggest1','')))
        temp = {}
        for x in tup_page:
            dt = dict(x)
            if 'No Result Available' != dt['pdt_dis_nm']:
                try:
                    link = (dt['link_src']).replace('\t','')
                    nseid = (((dt['pdt_dis_nm']).split('\t'))[2]).replace(', ','')
                    temp[nseid] = link
                except:
                    pass
            else:
                pass
        return temp

    def mc_sug_id(self,symbole):
        ticket = symbole.upper()
        dt = self.suggestion(ticket)
        try:
            link = dt[ticket] if (not dt)==False else None # chake dict(dt) are empty or not
            if link != None:
                mctup = self.find_id(link)
                if ticket == mctup[0]:
                    page = mctup[2]
                    mcid = mctup[1]
                else:
                    pass
                return mcid,page
        except:
            pass
        
    
    
    
    def matchWord(self,symbole,stockname):
        ticket = symbole.upper()
        def char_list(ticket):
            num_list = []
            for x in ((ticket.replace(' ','')).upper()):
                num_list.append(ord(x))
            return num_list

        tik = char_list(ticket)
        stk = char_list(stockname)
        tmp = 0
        c = 0
        for x in tik:
            try:
                if x==stk[c]:
                    tmp += 1
            except:
                pass
            c+=1
        
        st_len = len(stk)

        m_value = abs(((tmp*100)/st_len))

        return m_value
    
    def matchDict(self,dt,symbole):
        ticket = symbole.upper()
        temp = {}
        for x in dt:
            if x == '':
                pass
            else:
                temp[x] = self.matchWord(ticket,x)
        def sort_Dict(dt):
            temp_dt = {}
            for x in sorted(dt.values()):
                for y in dt:
                    if dt[y]==x:
                        temp_dt[y] = dt[y]
            return temp_dt
        rt = sort_Dict(temp)
        return rt
    
    def findLatter(self,ticket):
        tk = ticket.upper()
        latter = tk[0]
        return latter
    
    def linkDict(self,latter): # latter argument class delete
        file_list = os.listdir(self.create_path())
        fileName = self.create_path()+'\\'+latter+'.json'
        if latter +'.json' in file_list:
            with open(fileName, 'r')as op:
                linkdt = json.load(op)
        else:
            page = self.web(self.latterurl.format(latter))
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
            with open(fileName, 'w')as op:
                json.dump(linkdt, op)
        return linkdt
    
    def mc_latter_id(self,dt,ticket):
        symbole = ticket.upper()
        keys = reversed(list(dt))
        for x in keys:
            print(x)
            link = (self.linkDict(self.findLatter(symbole)))[x]
            st_id = self.find_id(link)
            if st_id == None:
                pass
            elif x == symbole:
                return st_id[1],st_id[2]
                break
            elif st_id[0] == symbole:
                return st_id[1],st_id[2]
                break
            else:
                pass
    
    def find_page(self,symbole):
        ticket = symbole.upper()
        sug = self.mc_sug_id(ticket)
        if sug != None:
            mc_id = sug[0]
            page = sug[1]
            return mc_id,page
        else:
            latter = self.findLatter(ticket)
            latterDict = self.linkDict(latter)
            m_dict = self.matchDict(latterDict,ticket)
            if (not m_dict) != True:
                m_id = ((self.mc_latter_id(m_dict,ticket))[0])
                page = (self.mc_latter_id(m_dict,ticket))[1]
                return m_id,page
            else:
                pass


