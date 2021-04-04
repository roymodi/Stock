from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO
import pandas as pd

from Webscraping import Webscraping



class YahooIndia:
    def __init__(self):
        self.purl = "https://in.finance.yahoo.com/quote/{0}?p={0}"
        self.history_url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={dayfrom}&period2={timenow}&interval=1d&events=history"
                           
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

    def historydata(self, stock, dd_mm_yy):
        stock = (stock.upper()) + ".NS"
        now = datetime.utcnow()
        timenow = str(int(now.timestamp()))
        date = (((dd_mm_yy.replace(",", " ")).replace("-", " ")).replace("/", " ")).split(" ")
        dd = int(date[0])
        mm = int(date[1])
        yy = int(date[2])
        hd_datetime = datetime(yy, mm, dd)
        dt = now - hd_datetime
        dayfrom = str(int((now - dt).timestamp()))
        file = self.web(self.history_url.format(stock, dayfrom=dayfrom, timenow=timenow))
        dataframe = pd.read_csv(StringIO(file.text), parse_dates=["Date"])
        return dataframe
