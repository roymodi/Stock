"creator BIDYUT PRAJAPATI"
'pyinstaller --onefile gui.py'
import os
from os import terminal_size
import tkinter as tk
from tkinter import StringVar, Toplevel, ttk
from tkinter.constants import BOTTOM, DISABLED, FLAT, HORIZONTAL, INSERT, LEFT, RAISED, RIGHT
import stock_indicator
import darvasbox
import stock_range_predction
import Nse
from YFindia import YahooIndia
import datetime
import Pivot_point
from Swing_20days import Swing_20days
import Turtle_trading
import SuperBreakout

window_0 = tk.Tk()
window_0.title('Stock technical analysis')
window_0.geometry('350x120')


def radiobtn():
    num = rdb.get()
    return num

def bokerage(closeprice):
    position = int(rdb1.get())
    if position == 1:
        rate = round((float((closeprice/100)*0.24)),2)
        bok = 'Delivery_Bokerage_of_stock: '+(str(rate))+"  DP charges 21 rupees per share"
    else:
        bok = 'Intraday_Bokerage_of_stock: '+(str(round((float((closeprice/100)*0.16)),2)))
    return bok

def create_path():
    folder_name = 'Temp_file'  # this is folder name
    current_dir = os.getcwd()  # this is path
    path = os.path.join(current_dir, folder_name)  # create folder path
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    return path

def trading(df,fname,data):
    filename = create_path()+"\\"+fname
    name = create_path()+"\\"+"Swing_trading___"+fname
    name_ = create_path()+"\\"+"Turtle_trading__"+fname
    name_sb = create_path()+"\\"+"Super_Breakout"+fname
    ls_cp = float((str(df['Close'].iloc[-1])).replace(',',''))
    sw = Swing_20days(df)
    sw_val = sw.swing(ls_cp)
    position = int(rdb1.get())
    tt = Turtle_trading.Turtle(df)
    tutd = tt.turtle(ls_cp)
    sb = SuperBreakout.SuperBreakout(df)
    if position == 1:
        if sw_val != False:
            with open(name,'a')as f:
                f.write(data)
        else:
            pass
        if tutd != False:
            with open(name_,'a')as fi:
                fi.write(data)
        else:
            pass
        if sb != False:
            with open(name_,'a')as fi:
                fi.write(data)
        else:
            pass
    else:
        with open(filename,'a')as ni:
            ni.write(data)
    

def getdata(df,preday=0, totalday=3): # preday=0 means twomorrow prediction
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

def hisdata(x):
    dt = datetime.datetime.now()
    yr = str((int(dt.strftime("%Y")))-1)
    mo = str(dt.strftime("%m"))
    dy = str(dt.strftime("%d"))
    newdate = str(dy+','+mo+','+yr)

    yf = YahooIndia()
    ns = Nse.NSE()
    try:
        df = ns.historydata(x,newdate)
    except ValueError:
        df = yf.historydata(x,newdate)
    return df


def suggestion(df):
    db = darvasbox.DarvasBox(df)
    days = db.days()
    fst = days[0]
    sec = days[1]
    if (fst > sec):
        re = fst + sec
    else:
        re = fst
    return re
def tigger(val,df):
    if val < 3:
        re = suggestion(df)
    else :
        re = val
    return re

# main funtion
def main(file,nsclp,tt):
    st = str(tt)
    today = datetime.datetime.now()  
    thetime = str(today.strftime("%c"))
    rmv = str(thetime[11:20])
    now = thetime.replace(rmv,'')
    preday = int(rdb.get())
    spinbox = int(spbox_1.get())
    maximum = float(ent_2vr.get())
    if maximum == 0:
        rnpv = 1000000000000000
    else:
        rnpv = maximum
    minmum = float(ent_1vr.get())
    filen = len(file)
    count = filen
    for x in file:
        barlabl.delete(0,'end')
        try:
            clp = float((str(nsclp.iloc[filen-count])).replace(',',''))
            bok = bokerage(clp)
            if rnpv >= clp and clp >= minmum:
                df = hisdata(x)
                if df.empty:
                    continue
                else:
                    try:
                        total_day = tigger(spinbox,df)
                        rang = " Range= "+str(total_day)
                        data = '\n\n'+str(filen-count)+'. '+'NSE:'+x+'             '+bok+'\n\n'+str(getdata(df,preday,total_day))+'\n\n\n'
                        filename = str(now)+' '+st+rang+" .txt"
                        trading(df,filename,data)
                    except:
                        pass
            else:
                pass
        except AttributeError:
            df = hisdata(x)
            if df.empty:
                    continue
            else:
                lcp = float((str(df['Close'].iloc[-1])).replace(',',''))
                bok = bokerage(lcp)
                if rnpv >= lcp and lcp >= minmum:
                    try:
                        total_day = tigger(spinbox,df)
                        rang = " Range= "+str(total_day)
                        data = '\n\n'+str(filen-count)+'. '+'NSE:'+x+'           '+bok+'\n\n'+str(getdata(df,preday,total_day))+'\n\n\n'
                        filename = str(now)+' '+st+rang+" .txt"
                        trading(df,filename,data)
                    except :
                        pass
                else:
                    pass
        count-=1
        barlabl.insert(0,str(round((((filen-count)+1)*(100/filen))))+'%')
        progress['value']=round((((filen-count)+1)*(100/filen)),2)
        window_0.update_idletasks()

# button funtion
def button():
    nse = Nse.NseData()
    tt = cmbovr.get()
    if tt == 'Nifty_50_stock_list':
        n50 = nse.nifty_50()
        n50clp = n50['Adj Close'].iloc[1:51]
        n50list = n50['SYMBOL'].iloc[1:51]
        main(n50list,n50clp,tt)
    elif tt == 'Top_gainers_stock_list':
        tg = nse.gainers()
        tgclp = tg['Prev. Close'].iloc[0:20]
        tglist = tg['Symbol'].iloc[0:20]
        main(tglist,tgclp,tt)
    elif tt == 'Top_losers_stock_list':
        tl = nse.losers()
        tlclp = tl['Prev. Close'].iloc[0:15]
        tllist = tl['Symbol'].iloc[0:15]
        main(tllist,tlclp,tt)
    elif tt == 'Volume_gainers_stock_list':
        tvg = nse.volume_gainers()
        tvgclp = None
        tvglist = tvg['SYMBOL'].iloc[0:25]
        main(tvglist,tvgclp,tt)
    elif tt == 'Most_active_stock_volume_list':
        masvol = nse.most_active_stock_volume()
        masvolcpl = masvol['Adj Close'].iloc[0:20]
        masvollist = masvol['SYMBOL'].iloc[0:20]
        main(masvollist,masvolcpl,tt)
    elif tt == 'Most_active_stock_value_list':
        masval = nse.most_active_stock_value()
        masvalclp = masval['Adj Close'].iloc[0:20]
        masvallist = masval['SYMBOL'].iloc[0:20]
        main(masvallist,masvalclp,tt)
    elif tt == 'Nifty_100_Company_stock_list':
        n100 = nse.nifty_100()
        n100.dropna(subset=['SYMBOL','Adj Close'])
        n100ls = n100['SYMBOL'].iloc[0:101]
        n100clp = n100['Adj Close'].iloc[0:101]
        main(n100ls,n100clp,tt)
    elif tt == 'Nifty_200_Company_stock_list':
        n200 = nse.nifty_200()
        n200.dropna(subset=['SYMBOL','Adj Close'])
        n200ls = n200['SYMBOL'].iloc[0:201]
        n200clp = n200['Adj Close'].iloc[0:201]
        main(n200ls,n200clp,tt)
    elif tt == 'Nifty_500_Company_stock_list':
        n500 = nse.nifty_500()
        n500ls = n500['Symbol'].iloc[0:501]
        clp = None
        main(n500ls,clp,tt)
    elif tt == 'Nse_listed_all_Company_list':
        nallc = nse.nse_listed_company()
        nallcls = nallc['SYMBOL']
        clp = None
        main(nallcls,clp,tt)
    else:
        pass


# frame 1
window_1 = tk.Frame(window_0)
window_1.pack()

lb_1 = tk.Label(window_1,text='Nse Stock list :')
lb_1.pack(side= LEFT)
cmbovr = tk.StringVar()
cmbo_1 = ttk.Combobox(window_1, width= 24, textvariable= cmbovr)
cmbo_1['values'] = (
    'Nifty_50_stock_list',
    'Top_gainers_stock_list',
    'Top_losers_stock_list',
    'Volume_gainers_stock_list',
    'Most_active_stock_volume_list',
    'Most_active_stock_value_list',
    'Nifty_100_Company_stock_list',
    'Nifty_200_Company_stock_list',
    'Nifty_500_Company_stock_list',
    'Nse_listed_all_Company_list'
    )
cmbo_1.current(0)
cmbo_1.pack(side=LEFT)

# label and spinbox
lb_2 = tk.Label(window_1, text= 'Range :')
lb_2.pack(side= LEFT)
spbox_1 = tk.IntVar()
spbox_1 = tk.Spinbox(window_1, from_= 0, to=9)
spbox_1.pack(side= LEFT)


# frame 2
window_2 = tk.Frame(window_0)
window_2.pack()

#radiobutton
rdb = tk.IntVar()
rbb_1 = tk.Radiobutton(window_2, text= 'Today', variable= rdb, value= 1, command= radiobtn)
rbb_1.pack(side= LEFT)
rbb_2 = tk.Radiobutton(window_2, text= 'Twomorrow', variable= rdb, value= 0, command= radiobtn)
rbb_2.pack(side= LEFT)

#radiobutton_2
rdb1 = tk.IntVar()
rbb_3 = tk.Radiobutton(window_2, text= 'Swing_Delivery', variable= rdb1, value= 1, command= radiobtn)
rbb_3.pack(side= LEFT)
rbb_4 = tk.Radiobutton(window_2, text= 'Intraday', variable= rdb1, value= 0, command= radiobtn)
rbb_4.pack(side= RIGHT)


# frame 3
window_3 = tk.Frame(window_0)
window_3.pack()

# label
lb_3 = tk.Label(window_3, text= '...................................Enter stock price range value..................................')
lb_3.pack()

# label and entry
lb_3 = tk.Label(window_3, text= '         Minmum value :')
lb_3.pack(side= LEFT)
ent_1vr = tk.IntVar()
ent_1 = tk.Entry(window_3, width= 5, bd= 2,textvariable=ent_1vr)
ent_1.pack(side= LEFT)

lb_3 = tk.Label(window_3, text= '               Maximum value :')
lb_3.pack(side= LEFT)
ent_2vr = tk.IntVar()
ent_2 = tk.Entry(window_3, width= 5,bd= 2,textvariable=ent_2vr)
ent_2.pack(side= LEFT)


# frame 4
window_4 = tk.Frame(window_0)
window_4.pack()

# progress bar
progress=ttk.Progressbar(window_4,orient= HORIZONTAL,length=240,mode='determinate')
progress.pack(side= LEFT)

# progress bar percentage
lb_5 = tk.Label(window_4,text='')
lb_5.pack(side= LEFT)
barlabl = tk.Entry(window_4, width= 5,relief = FLAT)
barlabl.pack(side= LEFT)

# label for space
lb_4 = tk.Label(window_4,text='')
lb_4.pack(side= LEFT)

# button
btn_1 = tk.Button(window_4, text= 'OK', command= button, width= 7)
btn_1.pack(side= RIGHT)


window_0.mainloop()