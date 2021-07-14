import tkinter as tk
from tkinter.constants import END, FLAT, HORIZONTAL, LEFT
from tkinter import ttk
import Nse
import darvasbox
import datetime
import pandas as pd
import os

"pyinstaller stock_delivery.py -w --onefile"


class Trading:
    def __init__(self,dataframe,profit_val):
        self.pf_val = float(profit_val)
        self.rawdf = dataframe
        self.df = dataframe.iloc[::-1].reset_index(drop=True)
        self.close_price = float((str(self.df['Close'].iloc[0])).replace(',',''))
    def value(self,df_value):
        try:
            value_str=df_value.str.replace(",","") # this is for remove , 
            value_float= value_str.astype(float)    # thid is for string to float value convert
            value = value_float
        except AttributeError:
            value = df_value
        return value
    def profit(self,mval):
        cal = ((mval/100)*self.pf_val)+mval
        rcal = round(cal,2)
        return rcal
    def swing_20days(self):
        high = self.df['High'].iloc[0:20]
        hval = self.value(high)
        buy_val = max(hval)
        terget = self.profit(buy_val)  #((buy_val/100)*pro_val)+buy_val
        close = self.close_price
        return buy_val,terget,close
    def Darvasbox(self):
        db = darvasbox.DarvasBox(self.rawdf)
        box = db.box()
        dHigh = (box[0])['Darvas_High']
        terget = self.profit(dHigh)
        close = self.close_price
        return dHigh,terget,close
    def turtle_trading(self):
        pass

class MainFrame(tk.Frame):
    def __init__(self,window,*args,**kwargs):
        tk.Frame.__init__(self,window,*args,**kwargs)
        self.window = window

        # Frame 1
        self.frm1 = tk.Frame(self.window)
        self.frm1.pack()
        # Label 1
        self.lbl1 = tk.Label(self.frm1,text='Nse Catagory : ')
        self.lbl1.pack(side= LEFT)
        # Combobox
        self.cmvar1 = tk.StringVar()
        self.combox1 = ttk.Combobox(self.frm1,width=27, textvariable=self.cmvar1)
        self.combox1['values'] = (
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
        )
        self.combox1.current(0)
        self.combox1.pack(side=LEFT)

        # Frame 2
        self.frm2 = tk.Frame(self.window)
        self.frm2.pack()
        # Label 2
        self.lbl2 = tk.Label(self.frm2,text='Trading Theory : ')
        self.lbl2.pack(side=LEFT)
        # Combobox
        self.cmvar2 = tk.StringVar()
        self.combox2 = ttk.Combobox(self.frm2,width=25,textvariable=self.cmvar2)
        self.combox2['values']=(
            'Swing_20_days',
            'Darvasbox_trading',
            'Turtle_trading'
        )
        self.combox2.current(0)
        self.combox2.pack(side=LEFT)


        # Frame 3
        self.frm3 = tk.Frame(self.window)
        self.frm3.pack()
        # Label 3
        self.lbl3 = tk.Label(self.frm3,text='Take Profit  ')
        self.lbl3.pack(side=LEFT)
        # Entry 1
        self.ent1   = tk.Entry(self.frm3,width=5)
        self.ent1.insert(0,8) # insert defult value '8'
        self.ent1.pack(side=LEFT)
        # Label 4
        self.lbl4 = tk.Label(self.frm3,text=" %               ")
        self.lbl4.pack(side=LEFT)
        # Button
        self.btn1 = tk.Button(self.frm3,text='Click',width=10,command=self.click)
        self.btn1.pack(side=LEFT)

        # Frame 5
        self.frm5 = tk.Frame(self.window)
        self.frm5.pack()
        # Progressbar
        self.progress = ttk.Progressbar(self.frm5,orient=HORIZONTAL,length=200,mode='determinate',takefocus=True,maximum=100)
        self.progress.pack(side=LEFT)
        # Label 5
        self.lbl5 = tk.Label(self.frm5,text='')
        self.lbl5.pack(side=LEFT)
        # Entry 2
        self.ent2 = tk.Entry(self.frm5,width=5,relief=FLAT)
        self.ent2.pack(side=LEFT)
    
    def click(self):
        self.btn1.config(text='Busy',state='disabled')
        self.btn1.update()
        self.combo()
        self.btn1.config(text='Click',state='normal')
        self.btn1.update()
    
    def main(self,cmplist,clplist,title):
        nse = Nse.NSE()
        profit = self.ent1.get()
        theroy = self.cmvar2.get()
        stocklist = []
        buylist = []
        tergetlist = []
        closepricelist = []
        filen = len(cmplist)
        count = filen
        for x in cmplist:
            self.ent2.delete(0,END)
            df = nse.historydata(x,self.collectdate())
            if df.empty:
                pass
            else:
                if theroy == 'Swing_20_days':
                    sw = Trading(df,profit)
                    swval = sw.swing_20days()
                    stocklist.append(x)
                    buylist.append(swval[0])
                    tergetlist.append(swval[1])
                    closepricelist.append(swval[2])
                elif theroy == 'Darvasbox_trading':
                    db = Trading(df,profit)
                    dbval = db.Darvasbox()
                    stocklist.append(x)
                    buylist.append(dbval[0])
                    tergetlist.append(dbval[1])
                    closepricelist.append(dbval[2])
                    pass
                elif theroy == 'Turtle_trading':
                    pass
                else:
                    pass
            count-=1
            self.ent2.insert(0,str(round((((filen-count)+1)*(100/filen))))+'%')
            self.progress['value']=round((((filen-count)+1)*(100/filen)),2)
            self.frm5.update_idletasks()
        data = {'Company':stocklist,'Close_price':closepricelist,'Buy_position':buylist,'Terget_position':tergetlist}
        newdf = pd.DataFrame(data)
        today = str(datetime.date.today())
        c_dir = os.getcwd()
        f_path = os.path.join(c_dir,'Delivery')
        try:
            os.mkdir(f_path)
        except:
            pass
        f_name = f_path+'\\'+title+'_'+theroy+'_'+today+'.csv'
        newdf.to_csv(f_name,index=False)    
    def collectdate(self):
        # collect date one year before
        dt = datetime.datetime.now()
        yr = str((int(dt.strftime("%Y")))-1) # 1 == one year
        mo = str(dt.strftime("%m"))
        dy = str(dt.strftime("%d"))
        newdate = str(dy+','+mo+','+yr)
        return newdate
    def combo(self):
        nse = Nse.NseData()
        tt = self.cmvar1.get()
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
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock technical analysis")
        self.geometry('250x93')
        self.resizable(False,False)

if __name__=="__main__":
    app = App()
    MainFrame(app)
    app.mainloop()