import os
from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
import pickle
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup



class NSE:
    def __init__(self):
        self.quote = "https://www.nseindia.com/api/quote-equity?symbol={0}"
        self.trade = 'https://www.nseindia.com/api/quote-equity?symbol={0}&section=trade_info'
        self.nse_history = 'https://www.nseindia.com/api/historical/cm/equity?symbol={0}&series=[%22EQ%22]&from={' \
                           'fromdate}&to={todate}&csv=true '

    @staticmethod
    def getdate(fromdate):
        today = datetime.now()
        now = ((str(today)).split())[0]
        fd = (fromdate.replace('/', ' ')).replace(',', ' ').split()
        fdd = int(fd[0])
        fmm = int(fd[1])
        fyy = int(fd[2])
        no = (now.replace('-', ' ')).split()
        ndd = int(no[2])
        nmm = int(no[1])
        nyy = int(no[0])
        day0 = datetime(nyy, nmm, ndd)
        day1 = datetime(fyy, fmm, fdd)
        delta = (day0 - day1).days
        if delta > 730:
            new_date = ((str(datetime.today() - timedelta(730))).split())[0]
            ndt = ((new_date.split())[0]).split('-')
            newdt = ndt[2] + '-' + ndt[1] + '-' + ndt[0]
        else:
            newdt = (fromdate.replace('/', '-')).replace(',', '-')
        return newdt

    
    def useragent(self):
        # ua = UserAgent()
        # hd = ua.ie
        try:
            ua = UserAgent()
            hd = ua.ie
        except:
            hd = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"}
            
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
        h = self.useragent()
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
        h = self.useragent()
        Trry = 0
        while True:
            print('nse_try',Trry)
            if Trry > 7:
                os.remove(file)
                self.cokie()
            try:
                page1 = requests.get(url, cookies=c, headers=h, timeout=10)
                if str(page1)=='<Response [401]>':
                    os.remove(file)
                    c2 = self.cokie()
                    page = requests.get(url, cookies=c2, headers=h, timeout=10)
                    break
                else:
                    page = page1
                    break
            except:
                pass
            Trry+=1
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
        dt = (((str(datetime.now())).split())[0]).split('-')
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