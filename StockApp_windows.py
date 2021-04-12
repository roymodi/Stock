import tkinter as tk
from tkinter import ttk

import os
from tkinter.constants import CENTER, FLAT, HORIZONTAL, LEFT
import numpy
import calendar
from datetime import timedelta
from io import StringIO

import pandas as pd
import pickle
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import datetime


class Webscraping:
    def __init__(self):
        self.proxy_url = "https://sslproxies.org/"

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

    def proxy_generator(self,url):
        response = requests.get(self.proxy_url)
        soup = BeautifulSoup(response.content, 'html5lib')
        proxy = ((list(map(lambda x: x[0] + ':' + x[1], list(
            zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8]))))))[0:100])
        
        jurl = self.creatname(url) + '.json'  # this is for create new name every time url change
        pg_file = self.create_path() + '\\' + jurl
        with open(pg_file, 'w')as op:
            json.dump(proxy, op)

    def jproxy(self,url):
        flist = os.listdir(self.create_path())
        jurl = self.creatname(url) + '.json'  # this is for create new name every time url change
        jp_file = self.create_path() + '\\' + jurl
        if jurl in flist:
            with open(jp_file, 'r')as op:
                jlod = json.load(op)
        else:
            self.proxy_generator(url)
            with open(jp_file, 'r')as op:
                jlod = json.load(op)
        return jlod

    def cokiere(self,url):
        flist = os.listdir(self.create_path())
        nurl = self.creatname(url)  # remove all spacial charater and number # this is for create new name every
        # time url change
        ck_nurl = self.create_path() + '\\' + nurl
        if nurl in flist:
            with open(ck_nurl, 'rb')as op:
                jscokie = pickle.load(op)
        else:
            jscokie = None
        return jscokie

    def webpage(self,url):
        ua = UserAgent()
        jcoke = self.cokiere(url)
        # this is for create new name if every time url change (string value return)
        gjurl = self.creatname(url) + 'goodproxy.json' 
        # this is temp_file in goodproxy.json file link
        wp_gjurl = self.create_path() + '\\' + gjurl
        # this is goodproxy.json file
        file = os.listdir(self.create_path())
        count = 0
        while True:
            hd = ua.random  # random user agent only
            _ua = {'User-Agent': hd}
            try:
                try:
                    with open(wp_gjurl, 'r')as op:
                        old_proxy = json.load(op)
                    res = requests.get(url, proxies=old_proxy, timeout=7, headers=_ua, cookies=jcoke)
                    return res
                    break

                except FileNotFoundError:
                    pxy = (self.jproxy(url))[count]
                    proxy = dict(https=pxy)
                    res = requests.get(url, proxies=proxy, timeout=7, headers=_ua, cookies=jcoke)
                    with open(wp_gjurl, 'w')as op:
                        json.dump(proxy, op)
                    nurl = self.creatname(url)
                    ck_nurl = self.create_path() + '\\' + nurl
                    with open(ck_nurl, 'wb')as f:
                        pickle.dump(res.cookies, f)
                    if count ==100:
                        count -=100
                        self.proxy_generator(url)
                    else:
                        pass
                    return res
                    break

                except :
                    os.remove(wp_gjurl)
                    pxy = (self.jproxy(url))[count]
                    proxy = dict(https=pxy)
                    res = requests.get(url, proxies=proxy, timeout=7, headers=_ua, cookies=jcoke)
                    with open(wp_gjurl, 'w')as op:
                        json.dump(proxy, op)
                    nurl = self.creatname(url)
                    ck_nurl = self.create_path() + '\\' + nurl
                    with open(ck_nurl, 'wb')as f:
                        pickle.dump(res.cookies, f)
                    if count ==100:
                        count -=100
                        self.proxy_generator(url)
                    else:
                        pass
                    return res
                    break

            except:
                pass
            count +=1

class SuperBreakout:
    def __init__(self,dataframe):
        self.si = Indicator(dataframe)
        self.df = dataframe
    def filter(self,df_value):
        try:
            value_str=df_value.str.replace(",","") # this is for remove , 
            value_float= value_str.astype(float)    # thid is for string to float value convert
            value = value_float
        except AttributeError:
            value = df_value
        return value

    def breakout(self):
        dataframe = self.filter(self.df["Close"])
        lcp = dataframe.iloc[-1]
        d5 = self.si.sma(5)
        d10 = self.si.sma(10)
        d15 = self.si.sma(15)
        d50 = self.si.sma(50)
        d100 = self.si.sma(100)
        d200 = self.si.sma(200)
        try:
            if (lcp >= d5)and(lcp >= d10)and(lcp >= d15)and(lcp >= d50)and(lcp >= d100)and(lcp <= d200):
                dt1 = dict(CLOSE=lcp,DMA_200=d200)
                dt2 = dict(DMA_5=d5,DMA_10=d10,DMA_15=d15,DMA_50=d50,DMA_100=d100)
                dt = dict(Main=dt1,Dma=dt2)
            else:
                dt = None
        except:
            pass
        return dt

# Turtle trading
class Turtle:
    def __init__(self,dataframe):
        self.df = dataframe.iloc[::-1].reset_index(drop=True)
        self.df_55 = self.df.iloc[0:55]
        self.df_20 = self.df.iloc[0:20]
        self.lst_low = float((str(dataframe["Low"].iloc[-1])).replace(',',''))
        self.si = Indicator(dataframe)

    def filter(self,df_value):
        try:
            value_str=df_value.str.replace(",","") # this is for remove , 
            value_float= value_str.astype(float)    # thid is for string to float value convert
            value = value_float
        except AttributeError:
            value = df_value
        return value

    def percent(self,per_val,value):
        per_val = per_val
        percent = per_val/100
        result = percent*value
        return result

    def turtle(self,current_price):
        dma_200 = self.si.sma(200)
        dma_50 = self.si.sma(50)
        low = list(self.filter(self.df_20["Low"]))
        high = list(self.filter(self.df_55["High"]))
        low_min = min(low)
        high_max = max(high)
        per_10 = self.percent(10,high_max)
        per_20 = self.percent(20,high_max)
        #rn = dict(Percent_20=per_20,Percent_10=per_10)
        high20 = high_max-per_20
        high10 = high_max-per_10
        if (current_price<=high10) and (current_price>=high20) and (low_min < self.lst_low) and (current_price >= dma_200):
            rt = dict(High_55_days= high_max,Stop_loss_20_days_low= low_min,DMA_200=dma_200,DMA_50=dma_50,Last_Close_price=current_price)
        else:
            rt = None
        return rt
        

class Swing_20days:
    def __init__(self,dataframe):
        self.df = dataframe.iloc[::-1].reset_index(drop=True)
        self.newdf = self.df.iloc[0:20]

    def value(self,df_value):
        try:
            value_str=df_value.str.replace(",","") # this is for remove , 
            value_float= value_str.astype(float)    # thid is for string to float value convert
            value = value_float
        except AttributeError:
            value = df_value
        return value
    def swing(self,Close_price):
        si = Indicator(self.df)
        dma_200 = si.sma(200)
        low = list(self.value(self.newdf["Low"]))
        high = list(self.value(self.newdf["High"]))
        low_min = min(low)
        high_max = max(high)
        if Close_price >= high_max and Close_price >= dma_200:
            rt = dict(High_20_days= high_max,Stop_loss_20_days_low= low_min,DMA_200=dma_200,Last_Close_price=Close_price)
        else:
            rt = None
        return rt



class Pivotpoint:
    def __init__(self, dataframe, day=0):
        self.df = dataframe[::-1].reset_index(drop=True)
        self.day = day
    def main(self):
        ldp = self.df.iloc[self.day]
        high = float(str(ldp['High']).replace(',',''))
        low = float(str(ldp['Low']).replace(',',''))
        close = float(str(ldp['Close']).replace(',',''))
        pp = round(((high+low+close)/3),2)
        r1 = round((2*pp-low),2)
        r2 = round((pp+(high-low)),2)
        r3 = round((pp+2*(high-low)),2)
        s1 = round((2*pp-high),2)
        s2 = round((pp-(high-low)),2)
        s3 = round((pp-2*(high-low)),2)
        rdtstr = 'Main_Pivot_level: '+str(pp)+'\n'+'Up_Resistance_level_1: '+str(r1)+'  Down_Support_lavel_1: '+str(s1)+'\n'+'Up_Resistance_level_2: '+str(r2)+'  Down_Support_lavel_2: '+str(s2)+'\n'+'Up_Resistance_level_3: '+str(r3)+ '  Down_Support_lavel_3: '+str(s3)
        rdt = dict(Main_Pivot_level=pp, Up_Resistance_level_1=r1, Down_Support_lavel_1=s1, Up_Resistance_level_2=r2, Down_Support_lavel_2=s2, Up_Resistance_level_3=r3, Down_Support_lavel_3=s3)
        
        return rdt,rdtstr

class YahooIndia:
    def __init__(self):
        self.purl = "https://in.finance.yahoo.com/quote/{0}?p={0}"
        self.history_url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={dayfrom}&period2={timenow}&interval=1d&events=history"
        self.bank_ = "https://query1.finance.yahoo.com/v7/finance/download/^NSEBANK?period1={dayfrom}&period2={timenow}&interval=1d&events=history&includeAdjustedClose=true"
        self.nifty_ = "https://query1.finance.yahoo.com/v7/finance/download/^NSEI?period1={dayfrom}&period2={timenow}&interval=1d&events=history&includeAdjustedClose=true"
                           
    def web(self, url):
        ws= Webscraping()
        page= ws.webpage(url)
        return page

    def live_price(self, stock):
        stock = (stock.upper()) + ".NS"
        lp_page = self.web(self.purl.format(stock))
        soup = BeautifulSoup(lp_page.content, 'html.parser')
        path = soup.find(class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
        price = path.get_text()
        return price

    def stock_info(self, stock):
        stock = (stock.upper()) + ".NS"
        si_page = self.web(self.purl.format(stock))
        soup = BeautifulSoup(si_page.content, 'html.parser')
        left_tab = soup.find_all(class_='C($primaryColor) W(51%)')
        right_tab = soup.find_all(class_='Ta(end) Fw(600) Lh(14px)')
        key = []
        value = []
        for x in left_tab:
            key.append((x.get_text()))
        for y in right_tab:
            value.append((y.get_text()))
        info = dict(zip(key, value))
        return info

    def timenow(self):
        now = datetime.datetime.utcnow()
        tnow = str(int(now.timestamp()))
        return tnow
    
    def dayfrom(self,dd_mm_yy):
        date = (((dd_mm_yy.replace(",", " ")).replace("-", " ")).replace("/", " ")).split(" ")
        dd = int(date[0])
        mm = int(date[1])
        yy = int(date[2])
        hd_datetime = datetime.datetime(yy, mm, dd)
        now = datetime.datetime.utcnow()
        dt = now - hd_datetime
        dfrom = str(int((now - dt).timestamp()))
        return dfrom

    def historydata(self, stock, dd_mm_yy):
        stock = (stock.upper()) + ".NS"
        file_ = self.web(self.history_url.format(stock, dayfrom=self.dayfrom(dd_mm_yy), timenow=self.timenow()))
        dataframe = pd.read_csv(StringIO(file_.text), parse_dates=["Date"])
        return dataframe
    
    def banknifty(self,dd_mm_yy):
        file_ = self.web(self.bank_.format(dayfrom= self.dayfrom(dd_mm_yy), timenow= self.timenow()))
        dataframe = pd.read_csv(StringIO(file_.text), parse_dates=["Date"])
        return dataframe
    
    def nifty(self,dd_mm_yy):
        file_ = self.web(self.nifty_.format(dayfrom= self.dayfrom(dd_mm_yy), timenow= self.timenow()))
        dataframe = pd.read_csv(StringIO(file_.text), parse_dates=["Date"])
        return dataframe
        


    


class NSE:
    def __init__(self):
        self.quote = "https://www.nseindia.com/api/quote-equity?symbol={0}"
        self.trade = 'https://www.nseindia.com/api/quote-equity?symbol={0}&section=trade_info'
        self.nse_history = 'https://www.nseindia.com/api/historical/cm/equity?symbol={0}&series=[%22EQ%22]&from={' \
                           'fromdate}&to={todate}&csv=true '

    @staticmethod
    def getdate(fromdate):
        today = datetime.datetime.now()
        now = ((str(today)).split())[0]
        fd = (fromdate.replace('/', ' ')).replace(',', ' ').split()
        fdd = int(fd[0])
        fmm = int(fd[1])
        fyy = int(fd[2])
        no = (now.replace('-', ' ')).split()
        ndd = int(no[2])
        nmm = int(no[1])
        nyy = int(no[0])
        day0 = datetime.datetime(nyy, nmm, ndd)
        day1 = datetime.datetime(fyy, fmm, fdd)
        delta = (day0 - day1).days
        if delta > 730:
            new_date = ((str(datetime.today() - timedelta(730))).split())[0]
            ndt = ((new_date.split())[0]).split('-')
            newdt = ndt[2] + '-' + ndt[1] + '-' + ndt[0]
        else:
            newdt = (fromdate.replace('/', '-')).replace(',', '-')
        return newdt

    @property
    def useragent(self):
        ua = UserAgent()
        hd = ua.ie
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5',
                  'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Host': 'www.nseindia.com',
                  'Upgrade-Insecure-Requests': '1', 'User-Agent': hd}
        return header

    def cokie(self):
        folder_name ='Temp_file' # this is folder name
        get_path = os.getcwd() # this is path where open programm
        create_path = os.path.join(get_path,folder_name) # create folder path
        try:
            os.mkdir(create_path)
        except FileExistsError:
            pass
        h = self.useragent
        flist = os.listdir(create_path) # file list
        file = create_path+'\\nseindia' # create file path with name
        if 'nseindia' in flist:
            with open(file, 'rb')as op:
                cokie = pickle.load(op)
        else:
            page = requests.get('https://www.nseindia.com/', timeout=5, headers=h)
            cokie = page.cookies
            with open(file, 'wb')as op:
                pickle.dump(cokie, op)
        return cokie

    def web(self, url):
        get_path = os.getcwd()
        create_path = os.path.join(get_path,'Temp_file')
        file = create_path+'\\nseindia'
        c = self.cokie()
        h = self.useragent
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

    def stock_info(self, ticket):
        stock = ticket.upper()
        page = (self.web(self.quote.format(stock))).json()
        priceinfo = page['priceInfo']
        metadata = page['metadata']
        market_depth_page = (self.web(self.trade.format(stock))).json()
        mdo = market_depth_page['marketDeptOrderBook']
        ti = mdo['tradeInfo']
        var = mdo['valueAtRisk']
        srw = market_depth_page['securityWiseDP']
        stock_data = dict(Company_Info=metadata, Price_Info=priceinfo, TradeInfo=ti, ValueAtRisk=var,
                          SecurityWiseDP=srw)
        return stock_data

    def historydata(self, ticket, from_dd_mm_yy):
        stock = ticket.upper()
        formd = self.getdate(from_dd_mm_yy)
        dt = (((str(datetime.datetime.now())).split())[0]).split('-')
        tod = dt[2] + '-' + dt[1] + '-' + dt[0]
        page = (self.web(self.nse_history.format(stock, fromdate=formd, todate=tod))).text
        newpage = page.replace('ï»¿', '')
        df = pd.read_csv(StringIO(newpage), parse_dates=['Date '])
        df.columns = ['Date', 'Series', 'Open', 'High', 'Low', 'PREV_CLOSE', 'ltp', 'Close', 'vwap', '52W_High',
                      '52W_Low', 'Volume', 'VALUE', 'No_of_trades']
        #newdf = df.replace(',','',regex=True)
        revarsdf = df[::-1].reset_index(drop=True)

        return revarsdf


class NseData(NSE):
    ny50 = 'https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%2050'
    gainer = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers&type=NIFTY&csv=true'
    loser = 'https://www.nseindia.com/api/live-analysis-variations?index=loosers&type=NIFTY&csv=true'
    vol_gain = 'https://www.nseindia.com/api/live-analysis-volume-gainers?mode=laVolumeGainer&csv=true'
    VOLUME = 'https://www.nseindia.com/api/live-analysis-most-active-securities?index=volume&csv=true'
    VALUE = 'https://www.nseindia.com/api/live-analysis-most-active-securities?index=value&csv=true'
    NIFTY200 = 'https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20200'
    NIFTY100 = 'https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20100'

    def __init__(self):
        NSE.__init__(self)

    @staticmethod
    def headline(data):
        head = data[0:109]
        splhead = ((head.replace('ï»¿', '')).replace('\n', '')).replace(' ', '')
        hd = data[0:188]
        yy = data[147:158]
        mm = data[175:186]
        fisthd = '"SYMBOL","Open","High","Low","PREV_CLOSE","Adj Close","CHNG","%CHNG","Volume","VALUE(RS_Lakhs)",' \
                 '"52W_HIGH","52W_LOW","365_DAY_%_CHNG({yy})","30_DAY_%_CHNG({mm})"\n '
        fishead = '"SYMBOL","OPEN","HIGH","LOW","PREV.CLOSE","LTP","%CHNG","VOLUME(Shares)","VALUE","CA"'
        fishead_cha = '"SYMBOL","Open","High","Low","PREV.CLOSE","Adj Close","%CHNG","Volume","VALUE","CA"'
        if splhead == fishead:
            newdata = data.replace(head, (fishead_cha + '\n'))
            df = pd.read_csv(StringIO(newdata), parse_dates=['SYMBOL'])
            #ndf = df.replace(',','',regex=True)
        else:
            chhd = fisthd.format(yy=yy, mm=mm)
            newdata = data.replace(hd, chhd)
            df = pd.read_csv(StringIO(newdata), parse_dates=['SYMBOL'])
            #ndf = df.replace(',','',regex=True)
        return df

    def nifty_50(self):
        page = self.web(self.ny50)
        df = self.headline(page.text)
        return df

    def gainers(self):
        page = (self.web(self.gainer)).text
        repl = page.replace('ï»¿', '')
        df = pd.read_csv(StringIO(repl), parse_dates=['Symbol'])
        return df

    def losers(self):
        page = (self.web(self.loser)).text
        repl = page.replace('ï»¿', '')
        df = pd.read_csv(StringIO(repl), parse_dates=['Symbol'])
        return df

    def volume_gainers(self):
        page = (self.web(self.vol_gain)).text
        repl = page.replace('ï»¿', '')
        df = pd.read_csv(StringIO(repl), parse_dates=['SYMBOL'])
        return df
    def most_active_stock_volume(self):
        page = self.web(self.VOLUME)
        df = self.headline(page.text)
        return df

    def most_active_stock_value(self):
        page = self.web(self.VALUE)
        df = self.headline(page.text)
        return df

    def nifty_100(self):
        page = self.web(self.NIFTY100)
        df = self.headline(page.text)
        return df

    def nifty_200(self):
        page = self.web(self.NIFTY200)
        df = self.headline(page.text)
        return df
        
    def nifty_500(self):
        url = 'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'
        page = requests.get(url)
        df = pd.read_csv(StringIO(page.text),parse_dates=['Company Name'])
        return df
    
    def nse_listed_company(self):
        ua = UserAgent()
        hd = ua.ie
        header = {"Host": "indiancompanies.in",
        "User-Agent": hd,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "TE": "Trailers"}
        url = "https://indiancompanies.in/listed-companies-in-nse-with-symbol/"
        res = requests.get(url,headers=header)
        soup = BeautifulSoup(res.content,'html5lib')
        table = soup.findAll('td')
        temp = []
        tablelist = []
        for x in table:
            tx = x.text
            temp.append(tx)
            if len(temp) == 3:
                tablelist.append(temp.copy())
                temp.clear()
            else:
                pass
        df = pd.DataFrame(tablelist[1:len(tablelist)],columns=tablelist[0])
        return df


class Result:
    def __init__(self, dataframe, start_day=0, total_day=3):
        dataframe.dropna(inplace=True)
        self.df = dataframe[::-1].reset_index(drop=True)
        self.std = start_day
        self.days = total_day + start_day
        self._open = list(self.df['Open'].iloc[self.std:self.days])
        self._high = list(self.df['High'].iloc[self.std:self.days])
        self._low = list(self.df['Low'].iloc[self.std:self.days])
        self._close = list(self.df['Close'].iloc[self.std:self.days])
        
    # noinspection PyBroadException
    @property
    def high(self):
        tem = []
        c = 0
        for x in self._open:
            try:
                ru = (float((str(self._high[c])).replace(',', '')) - float((str(x)).replace(',', '')))
            except AttributeError:
                ru = (self._high[c] - x)
            tem.append(ru)
            c += 1
        ad = sum(tem)
        div = round((ad / len(tem)), 2)
        return div

    # noinspection PyBroadException
    def low(self):
        tem = []
        c = 0
        for x in self._open:
            try:
                ru = (float((str(x)).replace(',', '')) - float((str(self._low[c])).replace(',', '')))
            except AttributeError:
                ru = (x - self._low[c])
            tem.append(ru)
            c += 1
        ad = sum(tem)
        div = round((ad / len(tem)), 2)
        return div

    # noinspection PyBroadException
    def close(self):
        tem = []
        c = 0
        for x in self._open:
            try:
                ru = (float((str(x)).replace(',', '')) - float((str(self._close[c])).replace(',', '')))
            except AttributeError:
                ru = (x - self._close[c])
            tem.append(ru)
            c += 1
        ad = sum(tem)
        div = round((ad / len(tem)), 2)
        return div

    def open(self):
        op = list(reversed(self._open))
        cl = list(reversed(self._close))
        cng = []
        for x in range(len(cl)):
            if x > 0:
                ch = float((((str(cl[x - 1])).replace(',', '')).replace(' ', ''))) - float(
                    (((str(op[x])).replace(',', '')).replace(' ', '')))
                cng.append(ch)

        ad = sum(cng)
        div = round((ad / len(cng)), 2)
        return div

    def first_result(self, percent=100):
        op = round((((self.open()) * percent) / 100), 2)
        hi = round(((self.high * percent) / 100), 2)
        lo = round((((self.low()) * percent) / 100), 2)
        cl = round((((self.close()) * percent) / 100), 2)
        full_value = dict(Open_range=self.open(), High_range=self.high, Low_range=self.low(), Close_rang=self.close())
        percent_value = dict(Percent_value=percent, Open_range=op, High_range=hi, Low_range=lo, Close_rang=cl)
        rt = dict(Full_value=full_value, Percent_value=percent_value)
        return rt

    def market_immotion(self):
        std_1 = 1+self.std
        try:
            self.df['Volume'] = self.df['Volume'].str.replace(",","")
            self.df['Volume'] = self.df['Volume'].astype(float) 
            voldata = self.df['Volume'].iloc[std_1:self.days]
        except AttributeError:
            voldata = self.df['Volume'].iloc[std_1:self.days]
        vol = list(voldata) 
        mean_value = sum(vol)/len(vol)
        volume = self.df['Volume'].iloc[self.std]
        if volume > mean_value:
            signal = '__BUY__'
        else:
            signal = '__SEL__'
        return signal

# noinspection PyGlobalUndefined,PyArgumentList
class DarvasBox:
    def __init__(self, dataframe):
        dataframe.dropna(inplace=True)
        newdf = (dataframe[::-1].reset_index(drop=True)).iloc[0:100]
        reversdf = newdf[::-1].reset_index(drop=True)
        self.df = reversdf
        self.date = self.df['Date']
        self.high = self.df['High']
        self.low = self.df['Low']

    def value(self,df_value):
        try:
            value_str=df_value.str.replace(",","") # this is for remove , 
            value_float= value_str.astype(float)    # thid is for string to float value convert
            value = value_float
        except AttributeError:
            value = df_value
        return value


    def lenth(self,df_value):
        if (len(self.date)) == (len(df_value)):
            ln = len(df_value)
        else:
            ln = 0
        return ln

    @staticmethod
    def weekday(x):
        global no
        date_str = (x.split('-'))
        if date_str[1].isdigit():
            y = int(date_str[0])  # year
            m = int(date_str[1])  # month
            d = int(date_str[2])  # date
            week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            d_num = calendar.weekday(y, m, d)
            day_name = week_day[d_num]
        else:  # this is for Nse dataframe beacuse nse date are defern
            month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            count = 0
            for x in month:
                if x == (date_str[1]):
                    no = count + 1
                    break
                # else:
                #     pass
                count += 1
            d = int(date_str[0])  # year
            m = int(no)  # month
            y = int(date_str[2])
            week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            d_num = calendar.weekday(y, m, d)
            day_name = week_day[d_num]
        return day_name

    @staticmethod
    def chake_wkday(lis, day):  # get days in two list uncomon days
        wk = ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        li = []
        # li.clear()
        for x in wk:
            if x not in lis:
                li.append(x)
                if x == day:
                    break
        return li

    @staticmethod
    def wklis_clear(wklis, wkday):
        new = wklis.copy()
        if len(wklis) == 7:
            new.clear()
        elif (len(wklis) < 7) and wkday == 'Friday':
            new.clear()
        # else:
        #     pass
        return new

    @staticmethod
    def tmp_lis(plis, wklis, wday):
        rt = []
        if len(plis) == 5:
            rt.clear()
        elif len(wklis) == 0:
            rt.clear()
        elif (len(plis) < 5) and (wday == 'Friday'):
            rt.clear()
        else:
            rt.extend(plis)
        return rt

    @staticmethod
    def array(plis, wklis, wd):
        newlis = []
        if (len(wklis) == 7) and (len(plis) <= 5):
            newlis = plis.copy()
        elif (len(wklis) < 7) and (len(plis) < 5) and (wd == 'Friday'):
            newlis = plis.copy()
        # else:
        #     pass
        return newlis

    def main(self,value):
        wklis = []
        mainlis = []
        pricelis = []
        count = 0
        for x in range(self.lenth(value)):
            only_date = ((str(self.date[count])).split())[0]
            wkday = self.weekday(only_date)
            price = float((str(value[count])).replace(',', ''))
            mainlis.append((self.array(pricelis, wklis, wkday))) # array creat pricelist and add mainlis
            wklis = self.wklis_clear(wklis, wkday) # this is creat new wklis
            pricelis=self.tmp_lis(pricelis, wklis, wkday) # this is creat new pricelis 
            mainlis = list(filter(None, mainlis))  # filter [] empity list in mainlist
            if wkday == 'Friday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Monday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Tuesday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Wednesday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Thursday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            else:
                pass
            count += 1
        return mainlis,pricelis
    
    def days(self):
        wkl = (self.main(self.value(self.high)))[0]
        lswkln = len(wkl[-1])
        prwkln = len((self.main(self.value(self.high)))[1])
        return lswkln,prwkln

    def box(self):
        high_tup = self.main(self.value(self.high))
        high_1st = round((max((high_tup[0])[-1])),2)
        high_2nd = round((max(high_tup[1])),2)

        low_tup = self.main(self.value(self.low))
        low_1st = round((min((low_tup[0])[-1])),2)
        low_2nd = round((min(low_tup[1])),2)
        
        main_dict = dict(Darvas_High=high_1st,Darvas_Low=low_1st)
        sub_dict = dict(Presend_week_High=high_2nd,Presend_week_Low=low_2nd)
        return main_dict,sub_dict

        

# noinspection PyGlobalUndefined
class Indicator:
    def __init__(self, DataFrame):
        self.df = DataFrame.iloc[::-1].reset_index(drop=True)
        cpl = self.df["Close"]
        self.close_price_list = list(reversed(list(cpl)))

    # noinspection PyBroadException
    def lenthlist(self, n):
        temp = []
        count = 0
        for x in self.close_price_list:
            try:
                temp.append(float(x.replace(',', '')))
            except AttributeError:
                temp.append(x)
            if count == n:
                break
            count += 1
        return temp

    def rsi(self, num):
        cpl = list(reversed(self.lenthlist(num)))
        tmp = [0]
        change = [0]
        gain = [0]
        lose = [0]
        for x in cpl:
            tmp.append(x)
            if len(tmp) == 3:
                ch = float(tmp[1]) - float(tmp[2])
                change.append(ch)
                tmp.pop(1)
                if (change[1]) < 0:
                    lose.append(abs(change[1]))
                    change.pop(1)
                else:
                    gain.append(change[1])
                    change.pop(1)
        average_gain = sum(gain) / 14
        average_lose = sum(lose) / 14
        rs = average_lose / average_gain 
        rsi_ = 100 - (100 / (1 + rs))
        rsi = round(rsi_, 2)
        return rsi

    def sma(self, no):
        cplis = self.lenthlist(no)
        cplenth = len(cplis)
        sma = round((sum(cplis) / cplenth), 2)
        return round(sma, 2)

    def ema(self, days):
        sma = self.sma(days)
        k = 2 / (days + 1)
        clpric = (self.lenthlist(0))[0]
        ema = clpric * k + sma * (1 - k)
        return round(ema, 2)

    def macd(self):
        global condition
        macd_line = self.ema(12)
        signal_line = self.ema(26)
        zero_line = self.ema(9)

        bull = macd_line > signal_line
        bear = macd_line < signal_line
        bulst1 = macd_line > zero_line
        bulst2 = signal_line > zero_line
        barst1 = macd_line < zero_line
        barst2 = signal_line < zero_line

        if bull and barst1 and barst2:
            condition = 'Bullish_crossover'
        elif bear and bulst1 and bulst2:
            condition = 'Bearish_crossover'
        elif bull and bulst1 and bulst2:
            condition = 'Strong_bullish_trend'
        elif bear and barst1 and barst2:
            condition = 'Strong_bearish_trend'
        elif bull and bulst1 and barst2:
            condition = 'Wipshaw'
        elif bear and bulst2 and barst1:
            condition = 'Wipshaw'

        return condition
    
    def bollinger_bands(self):
        stdlist = self.lenthlist(20)
        bbstd = numpy.std(stdlist)
        bbsma = self.sma(20)
        upper = round((bbsma + (bbstd * 2)),2)
        lower = round((bbsma - (bbstd*2)),2)
        bbresult = dict(Upper_Band=upper, Middle_Band=bbsma, Lower_Band=lower)
        return bbresult

class MainFrame(tk.Frame):
    def __init__(self,window,*args,**kwargs):
        tk.Frame.__init__(self,window,*args,**kwargs)
        self.window = window

        # Frame 1 label combobox
        self.wd1 = tk.Frame(self.window)
        self.wd1.pack()

        self.lb_1 = tk.Label(self.wd1,text='Nse Stock list:')
        self.lb_1.pack(side= LEFT)
        self.cmbovr = tk.StringVar()
        self.cmbo_1 = ttk.Combobox(self.wd1, width= 27, textvariable= self.cmbovr)
        self.cmbo_1['values'] = (
            'Nifty_50_stock_list',
            'Top_gainers_stock_list',
            'Top_losers_stock_list',
            'Volume_gainers_stock_list',
            'Most_active_stock_volume_list',
            'Most_active_stock_value_list',
            'Nifty_100_Company_stock_list',
            'Nifty_200_Company_stock_list',
            'Nifty_500_Company_stock_list',
            'Nse_listed_all_Company_list',
            'BankNifty_nse_index',
            'Nifty50_nse_index'
            )
        self.cmbo_1.current(0)
        self.cmbo_1.pack(side=LEFT)

        # Frame 2 label spinbox radiobutton
        self.wd2 = tk.Frame(self.window)
        self.wd2.pack()
        self.lb_2 = tk.Label(self.wd2, text= 'Range :')
        self.lb_2.pack(side= LEFT)
        self.spbox_1 = tk.IntVar()
        self.spbox_1 = tk.Spinbox(self.wd2, width= 3, from_= 0, to=9)
        self.spbox_1.pack(side= LEFT)

        self.spaceLabel = tk.Label(self.wd2,text="  ")
        self.spaceLabel.pack(side= LEFT)
        self.rdb = tk.IntVar()
        self.rbb_1 = tk.Radiobutton(self.wd2, text= 'Today', variable= self.rdb, value= 1, command= self.radiobtn)
        self.rbb_1.pack(side= LEFT)
        self.rbb_2 = tk.Radiobutton(self.wd2, text= 'Twomorrow', variable= self.rdb, value= 0, command= self.radiobtn)
        self.rbb_2.pack(side= LEFT)


        # Frame 3 radiobutton
        self.wd3 = tk.Frame(self.window)
        self.wd3.pack()
        self.lb_3 = tk.Label(self.wd3,text="Trading type     ")
        self.lb_3.pack(side= LEFT)
        self.rdb1 = tk.IntVar()
        self.rbb_3 = tk.Radiobutton(self.wd3, text= 'Delivery', variable= self.rdb1, value= 1, command= self.radiobtn)
        self.rbb_3.pack(side= LEFT)
        self.rbb_4 = tk.Radiobutton(self.wd3, text= 'Intraday', variable= self.rdb1, value= 0, command= self.radiobtn)
        self.rbb_4.pack(side= LEFT)

        # Frame 4 label Entry
        self.wd4 = tk.Frame(self.window)
        self.wd4.pack()
        self.lb_4 = tk.Label(self.wd4, text= 'Minmum value')
        self.lb_4.pack(side= LEFT)
        self.ent_1vr = tk.IntVar()
        self.ent_1 = tk.Entry(self.wd4, width= 5, bd= 2,textvariable=self.ent_1vr)
        self.ent_1.pack(side= LEFT)

        self.lb_5 = tk.Label(self.wd4, text= 'Maximum value')
        self.lb_5.pack(side= LEFT)
        self.ent_2vr = tk.IntVar()
        self.ent_2 = tk.Entry(self.wd4, width= 5,bd= 2,textvariable=self.ent_2vr)
        self.ent_2.pack(side= LEFT)

        # Frame 5 Progressbar label Entry
        self.wd5 = tk.Frame(self.window)
        self.wd5.pack()
        self.progress = ttk.Progressbar(self.wd5, orient= HORIZONTAL, length=210, mode='determinate')
        self.progress.pack(side= LEFT)

        self.lb_5 = tk.Label(self.wd5,text='')
        self.lb_5.pack(side= LEFT)
        self.barlabl = tk.Entry(self.wd5, width= 5,relief = FLAT)
        self.barlabl.pack(side= LEFT)

        # Frame 6 progress bar percentage
        self.wd6 = tk.Frame(self.window)
        self.wd6.pack()
        self.btn_1 = tk.Button(self.wd6, text= 'Click', command= self.click_press, width= 10)
        self.btn_1.pack(side= LEFT)

    def radiobtn(self):
        num = self.rdb.get()
        return num

    def bokerage(self,closeprice):
        position = int(self.rdb1.get())
        if position == True:
            rate = round((float((closeprice/100)*0.24)),2)
            bok = 'Delivery_Bokerage_of_stock: '+(str(rate))+"  DP charges 21 rupees per share"
        else:
            bok = 'Intraday_Bokerage_of_stock: '+(str(round((float((closeprice/100)*0.16)),2)))
        return bok

    def create_path(self):
        folder_name = 'Temp_file'  # this is folder name
        current_dir = os.getcwd()  # this is path
        path = os.path.join(current_dir, folder_name)  # create folder path
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        return path

    def writefile(self,fname,data):
        with open(fname,'a')as op:
            op.write(data)

    def trading(self,df,fname,data):
        dfname = fname.replace(fname[-6],'')
        filename = self.create_path()+"\\"+fname
        name = self.create_path()+"\\"+"Swing_trading___"+dfname
        name_ = self.create_path()+"\\"+"Turtle_trading__"+dfname
        name_sb = self.create_path()+"\\"+"Super_Breakout"+dfname
        ls_cp = float((str(df['Close'].iloc[-1])).replace(',',''))
        sw = Swing_20days(df)
        sw_val = sw.swing(ls_cp)
        position = int(self.rdb1.get())
        tt = Turtle(df)
        tutd = tt.turtle(ls_cp)
        sb = SuperBreakout(df)
        bo = sb.breakout()
        if position == True:
            if sw_val != None:
                self.writefile(name,data)
            else:
                pass
            if tutd != None:
                self.writefile(name_,data)
            else:
                pass
            if bo != None:
                self.writefile(name_sb,data)
            else:
                pass
        else:
            self.writefile(filename,data)
    
    def getdata(self,df,preday=0, totalday=3): # preday=0 means twomorrow prediction
        srp = Result(df, preday, totalday)
        srp_ = srp.first_result()['Full_value']
        m_i = srp.market_immotion()
        si = Indicator(df)
        dma = si.sma(200)
        ema8 = si.ema(8)
        ema20 = si.ema(20)
        ema50 = si.ema(50)
        rsi_ = si.rsi(14)
        macd_ = si.macd()
        b_bands = si.bollinger_bands()
        db = DarvasBox(df)
        db_ = db.box()
        ls_cp = float((str(df['Close'].iloc[-1])).replace(',',''))
        ls_op = float((str(df['Open'].iloc[-1])).replace(',',''))
        ls_hi = float((str(df['High'].iloc[-1])).replace(',',''))
        ls_lo = float((str(df['Low'].iloc[-1])).replace(',',''))
        vol1 = df['Volume'].iloc[-1]
        date1 = ((str(df['Date'].iloc[-1])).split())[0]
        voldata1 = 'Volume:  Today('+date1+' = '+str(vol1)+')'
        vol2=df['Volume'].iloc[-2]
        date2=((str(df['Date'].iloc[-2])).split())[0]
        voldata2 = ', Afterday('+date2+' = '+str(vol2)+')'
        pp = Pivotpoint(df,preday)
        ppdata = (pp.main())[1]
        sw = Swing_20days(df)
        sw_val = sw.swing(ls_cp)
        tt = Turtle(df)
        tutd = tt.turtle(ls_cp)
        sb = SuperBreakout(df)
        bk = sb.breakout()
        rt = 'Last_Open_price: '+str(round((ls_op),2))+',   Last_Close_price: '+\
        str(round((ls_cp),2))+'\n'+'Last_High_price:  '+str(round((ls_hi),2))+\
        '   Last_Low_price:  '+str(round((ls_lo),2))+'\n\n'+voldata1+voldata2+\
        '\n\n'+'Pivot_point: '+str(ppdata)+'\n\n'+'Stock_range: '+str(srp_)+'\n\n'+\
        'EMA(8): '+str(ema8)+',  EMA(20): '+str(ema20)+',  EMA(50): '+str(ema50)+"  200_DMA: "+str(dma)+\
        ',   RSI: '+str(rsi_)+'\n\n'+'DarvasBox: '+str(db_)+'\n\n'+'Bollinger_bands: '+\
        str(b_bands)+'\n\n'+'Macd: '+macd_+'\n'+'Market_immotion :'+m_i+'\n\nSwing_trading: \n'+\
        str(sw_val)+'\n\n'+"Turtle_trading: \n"+str(tutd)+'\n\n'+"Super_Breakout: \n"+str(bk)
        return rt
    
    def collectdate(self):
        # collect date one year before
        dt = datetime.datetime.now()
        yr = str((int(dt.strftime("%Y")))-1) # 1 == one year
        mo = str(dt.strftime("%m"))
        dy = str(dt.strftime("%d"))
        newdate = str(dy+','+mo+','+yr)
        return newdate
    
    def hisdata(self,x):
        newdate = self.collectdate()
        yf = YahooIndia()
        ns = NSE()
        try:
            df = ns.historydata(x,newdate)
        except ValueError:
            df = yf.historydata(x,newdate)
        return df
    
    def suggestion(self,df):
        db = DarvasBox(df)
        days = db.days()
        fst = days[0]
        sec = days[1]
        if (fst > sec):
            re = fst + sec
        else:
            re = fst
        return re
    
    def tigger(self,val,df):
        if val < 3:
            re = self.suggestion(df)
        else :
            re = val
        return re

    # main funtion
    def main(self,file,nsclp,tt):
        st = str(tt)
        today = datetime.datetime.now()
        thetime = str(today.strftime("%c"))
        rmv = str(thetime[11:20])
        now = thetime.replace(rmv,'')
        preday = int(self.rdb.get())
        spinbox = int(self.spbox_1.get())
        maximum = float(self.ent_2vr.get())
        if maximum == 0 :
            rnpv = 1000000000000000
        else:
            rnpv = int(maximum)
        minmum = float(self.ent_1vr.get())
        filen = len(file)
        count = filen
        for x in file:
            self.barlabl.delete(0,'end')
            try:
                clp = float((str(nsclp.iloc[filen-count])).replace(',',''))
                bok = self.bokerage(clp)
                if rnpv >= clp and clp >= minmum:
                    df = self.hisdata(x)
                    if df.empty:
                        continue
                    else:
                        try:
                            total_day = self.tigger(spinbox,df)
                            rang = " Range= "+str(total_day)
                            data = '\n\n'+str(filen-count)+'. '+'NSE:'+x+'             '+bok+'\n\n'+str(self.getdata(df,preday,total_day))+'\n\n\n'
                            filename = str(now)+' '+st+rang+" .txt"
                            self.trading(df,filename,data)
                        except:
                            pass
                else:
                    pass
            except AttributeError:
                df = self.hisdata(x)
                if df.empty:
                        continue
                else:
                    lcp = float((str(df['Close'].iloc[-1])).replace(',',''))
                    bok = self.bokerage(lcp)
                    if rnpv >= lcp and lcp >= minmum:
                        try:
                            total_day = self.tigger(spinbox,df)
                            rang = " Range= "+str(total_day)
                            data = '\n\n'+str(filen-count)+'. '+'NSE:'+x+'           '+bok+'\n\n'+str(self.getdata(df,preday,total_day))+'\n\n\n'
                            filename = str(now)+' '+st+rang+" .txt"
                            self.trading(df,filename,data)
                        except :
                            pass
                    else:
                        pass
            count-=1
            self.barlabl.insert(0,str(round((((filen-count)+1)*(100/filen))))+'%')
            self.progress['value']=round((((filen-count)+1)*(100/filen)),2)
            self.wd5.update_idletasks()

    # nifty index main funtion
    def nifty_index(self,ticket):
        spinbox = int(self.spbox_1.get())
        pday = int(self.rdb.get())
        newdate = self.collectdate()
        fname = self.create_path()+"\\"+ticket+".txt"
        yf = YahooIndia()
        if ticket == "BankNifty_nse_index":
            df = yf.banknifty(newdate)
            ttday = self.tigger(spinbox,df)
            data = str(self.getdata(df,pday,ttday))
            nd = data.split("\n")
            newdata = nd[0]+"\n"+nd[1]+"\n\n"+nd[5]+"\n"+nd[6]+"\n"+nd[7]+"\n"+nd[8]+"\n\n"+nd[10]+"\n\n"+nd[14]+"\n\n"+nd[18]+"\n"+nd[19]
            self.writefile(fname,newdata)
        else:
            df = yf.nifty(newdate)
            ttday = self.tigger(spinbox,df)
            data = str(self.getdata(df,pday,ttday))
            nd = data.split("\n")
            newdata = nd[0]+"\n"+nd[1]+"\n\n"+nd[5]+"\n"+nd[6]+"\n"+nd[7]+"\n"+nd[8]+"\n\n"+nd[10]+"\n\n"+nd[14]+"\n\n"+nd[18]+"\n"+nd[19]
            self.writefile(fname,newdata)
        # update prograss bar and value 
        self.barlabl.insert(0,'100'+'%')
        self.progress['value']=100
        self.wd5.update_idletasks()

    def click(self):
        nse = NseData()
        tt = self.cmbovr.get()
        if tt == 'Nifty_50_stock_list':
            n50 = nse.nifty_50()
            n50clp = n50['Adj Close'].iloc[1:51]
            n50list = n50['SYMBOL'].iloc[1:51]
            self.main(n50list,n50clp,tt)
        elif tt == 'Top_gainers_stock_list':
            tg = nse.gainers()
            tgclp = tg['Prev. Close'].iloc[0:20]
            tglist = tg['Symbol'].iloc[0:20]
            self.main(tglist,tgclp,tt)
        elif tt == 'Top_losers_stock_list':
            tl = nse.losers()
            tlclp = tl['Prev. Close'].iloc[0:15]
            tllist = tl['Symbol'].iloc[0:15]
            self.main(tllist,tlclp,tt)
        elif tt == 'Volume_gainers_stock_list':
            tvg = nse.volume_gainers()
            tvgclp = None
            tvglist = tvg['SYMBOL'].iloc[0:25]
            self.main(tvglist,tvgclp,tt)
        elif tt == 'Most_active_stock_volume_list':
            masvol = nse.most_active_stock_volume()
            masvolcpl = masvol['Adj Close'].iloc[0:20]
            masvollist = masvol['SYMBOL'].iloc[0:20]
            self.main(masvollist,masvolcpl,tt)
        elif tt == 'Most_active_stock_value_list':
            masval = nse.most_active_stock_value()
            masvalclp = masval['Adj Close'].iloc[0:20]
            masvallist = masval['SYMBOL'].iloc[0:20]
            self.main(masvallist,masvalclp,tt)
        elif tt == 'Nifty_100_Company_stock_list':
            n100 = nse.nifty_100()
            n100.dropna(subset=['SYMBOL','Adj Close'])
            n100ls = n100['SYMBOL'].iloc[0:101]
            n100clp = n100['Adj Close'].iloc[0:101]
            self.main(n100ls,n100clp,tt)
        elif tt == 'Nifty_200_Company_stock_list':
            n200 = nse.nifty_200()
            n200.dropna(subset=['SYMBOL','Adj Close'])
            n200ls = n200['SYMBOL'].iloc[0:201]
            n200clp = n200['Adj Close'].iloc[0:201]
            self.main(n200ls,n200clp,tt)
        elif tt == 'Nifty_500_Company_stock_list':
            n500 = nse.nifty_500()
            n500ls = n500['Symbol'].iloc[0:501]
            clp = None
            self.main(n500ls,clp,tt)
        elif tt == 'Nse_listed_all_Company_list':
            nallc = nse.nse_listed_company()
            nallcls = nallc['SYMBOL']
            clp = None
            self.main(nallcls,clp,tt)
        else:
            self.nifty_index(tt)

    def click_press(self):
        self.btn_1.config(text="Busy", state="disabled")
        self.btn_1.update()
        self.click()
        self.btn_1.update()
        self.btn_1.config(text="Click", state="normal")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock technical analysis")
        self.geometry('260x150')
        self.resizable(False,False)


if __name__=="__main__":
    app = App()
    MainFrame(app)
    app.mainloop()