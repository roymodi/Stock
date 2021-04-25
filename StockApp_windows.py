import tkinter as tk
from tkinter import ttk

import os
from tkinter.constants import CENTER, FLAT, HORIZONTAL, LEFT
from datetime import timedelta
from io import StringIO

import pandas as pd
import datetime

import stock_indicator
import darvasbox
import stock_range_predction
import Nse
import datetime
import Pivot_point
from Swing_20days import Swing_20days
import Turtle_trading
import SuperBreakout

import requests
from fake_useragent import UserAgent

"pyinstaller StockApp_windows.py -w --onefile"

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
        self.progress = ttk.Progressbar(self.wd5, orient= HORIZONTAL, length=210, mode='determinate',takefocus=True,maximum=100)
        self.progress.pack(side= LEFT)

        self.lb_5 = tk.Label(self.wd5,text='')
        self.lb_5.pack(side= LEFT)
        self.barlabl = tk.Entry(self.wd5, width= 5,relief = FLAT)
        self.barlabl.pack(side= LEFT)

        # Frame 6 progress bar percentage
        self.wd6 = tk.Frame(self.window)
        self.wd6.pack()
        # Button 
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
        filename = self.create_path()+"\\"+fname
        position = int(self.rdb1.get())
        if position == True:
            dfname = fname.replace(fname[-6],'')
            name = self.create_path()+"\\"+"Swing_trading___"+dfname
            name_ = self.create_path()+"\\"+"Turtle_trading__"+dfname
            name_sb = self.create_path()+"\\"+"Super_Breakout"+dfname
            ls_cp = float((str(df['Close'].iloc[-1])).replace(',',''))
            sw = Swing_20days(df)
            sw_val = sw.swing(ls_cp)
            tt = Turtle_trading.Turtle(df)
            tutd = tt.turtle(ls_cp)
            sb = SuperBreakout.SuperBreakout(df)
            bo = sb.breakout()
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
        srp = stock_range_predction.Result(df, preday, totalday)
        srp_ = srp.first_result()['Full_value']
        m_i = srp.market_immotion()
        si = stock_indicator.Indicator(df)
        dma = si.sma(200)
        ema8 = si.ema(8)
        ema20 = si.ema(20)
        ema50 = si.ema(50)
        rsi_ = si.rsi(14)
        macd_ = si.macd()
        b_bands = si.bollinger_bands()
        db = darvasbox.DarvasBox(df)
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
        pp = Pivot_point.Pivotpoint(df,preday)
        ppdata = (pp.main())[1]
        sw = Swing_20days(df)
        sw_val = sw.swing(ls_cp)
        tt = Turtle_trading.Turtle(df)
        tutd = tt.turtle(ls_cp)
        sb = SuperBreakout.SuperBreakout(df)
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
        ns = Nse.NSE()
        try:
            df = ns.historydata(x,newdate)
        except ValueError:
            df = ns.historydata(x,newdate)
        return df
    
    def suggestion(self,df):
        db = darvasbox.DarvasBox(df)
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

    def nifty_index(self,ticket):
        bank_ = "https://query1.finance.yahoo.com/v7/finance/download/^NSEBANK?period1={dayfrom}&period2={timenow}&interval=1d&events=history&includeAdjustedClose=true"
        nifty_ = "https://query1.finance.yahoo.com/v7/finance/download/^NSEI?period1={dayfrom}&period2={timenow}&interval=1d&events=history&includeAdjustedClose=true"
        ua = UserAgent()
        hd = ua.ie
        header = {'User-Agent': hd}
        spinbox = int(self.spbox_1.get())
        pday = int(self.rdb.get())
        newdate = self.collectdate()
        fname = self.create_path()+"\\"+ticket+".txt"
        if ticket == "BankNifty_nse_index":
            page = requests.get(bank_.format(dayfrom=self.dayfrom(newdate),timenow= self.timenow()),headers=header)
            df = pd.read_csv(StringIO(page.text), parse_dates=["Date"])
            ttday = self.tigger(spinbox,df)
            data = str(self.getdata(df,pday,ttday))
            nd = data.split("\n")
            newdata = nd[0]+"\n"+nd[1]+"\n\n"+nd[5]+"\n"+nd[6]+"\n"+nd[7]+"\n"+nd[8]+"\n\n"+nd[10]+"\n\n"+nd[14]+"\n\n"+nd[18]+"\n"+nd[19]
            self.writefile(fname,newdata)
        else:
            page = requests.get(nifty_.format(dayfrom=self.dayfrom(newdate),timenow= self.timenow()),headers=header)
            df = pd.read_csv(StringIO(page.text), parse_dates=["Date"])
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
        nse = Nse.NseData()
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