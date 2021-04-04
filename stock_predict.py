"creator BIDYUT PRAJAPATI"

import stock_indicator
import darvasbox
import stock_range_predction
import Nse
from YFindia import YahooIndia
import datetime
import Pivot_point
import os 


"pyinstaller --onefile stock_predict.py"

def getdata(df,preday=0, totalday=3): # preday=0 means twomorrow prediction
    srp = stock_range_predction.Result(df, preday, totalday)
    srp_ = srp.first_result()['Full_value']
    m_i = srp.market_immotion()
    si = stock_indicator.Indicator(df['Close'])
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
    vol1 = df['Volume'].iloc[-1]
    date1 = ((str(df['Date'].iloc[-1])).split())[0]
    voldata1 = ', Volume: ('+date1+' = '+str(vol1)+')'
    vol2=df['Volume'].iloc[-2]
    date2=((str(df['Date'].iloc[-2])).split())[0]
    voldata2 = ', ('+date2+' = '+str(vol2)+')'
    pp = Pivot_point.Pivotpoint(df,preday)
    ppdata = (pp.main())[1]
    rt = 'Last_Open_price: '+str(round((ls_op),2))+',   Last_Close_price: '+str(round((ls_cp),2))+voldata1+voldata2+'\n\n'+'Pivot_point: '+str(ppdata)+'\n\n'+'Stock_range: '+str(srp_)+'\n\n'+'EMA(8): '+str(ema8)+',  EMA(20): '+str(ema20)+',  EMA(50): '+str(ema50)+',   RSI: '+str(rsi_)+'\n\n'+'DarvasBox: '+str(db_)+'\n\n'+'Bollinger_bands: '+str(b_bands)+'\n\n'+'Macd: '+macd_+'\n'+'Market_immotion :'+m_i
    return rt
 
def hisdata(x):
    yf = YahooIndia()
    ns = Nse.NSE()
    try:
        df = yf.historydata(x,'01,01,1990')
    except ValueError:
        df = ns.historydata(x,'01,01,1990')
    return df
        

today = datetime.datetime.now()  
thetime = str(today.strftime("%c"))
rmv = str(thetime[11:20])
now = thetime.replace(rmv,'')

title = '1 = Nifty_50'+'\n'+'2 = Top_gainers'+'\n'+'3 = Top_losers'+'\n'+'4 = Volume_gainers'+'\n'+'5 = Most_active_stock_volume'+'\n'+'6 = Most_active_stock_value'+'\n\n'+'Chose NSE list number only: '


def main(file,tt):
    global filename
    ts = title.split('\n')
    st = ((ts[int(tt)-1]).split())[-1]
    title2 = 'if twomorrow enter "0" or if today enter "1"'+'\n'+'Enter Number:  '
    title3 = 'Total avarage day count minium enter number "3" or highir number'+'\n'+'Enter number:  '
    title4 = 'Enter Stock price maximum value for FILTER'+'\n'+'Enter number:  '
    preday = int(input(title2))
    total_day = int(input(title3))
    rnpv = float(input(title4))
    rang = " Range= "+str(total_day)
    
    count = 0
    for x in file:
        df = hisdata(x)
        if df.empty:
            continue
        else:
            lcp = float((str(df['Close'].iloc[-1])).replace(',',''))
            if rnpv >= lcp :
                data = '\n\n'+str(count)+'. '+'NSE:'+x+'\n\n'+str(getdata(df,preday,total_day))+'\n\n\n'
                filename = str(now)+' '+st+rang+" .txt"
                with open(filename,'a')as ni:
                    ni.write(data)
                print(data)
            else:
                pass
        count+=1


nse = Nse.NseData()
while True:
    try:
        tt = input(title)
        if tt == '1':
            n50 = nse.nifty_50()
            n50list = n50['SYMBOL'].iloc[1:51]
            main(n50list,tt)
        elif tt == '2':
            tg = nse.gainers()
            tglist = tg['Symbol'].iloc[0:20]
            main(tglist,tt)
        elif tt == '3':
            tl = nse.losers()
            tllist = tl['Symbol'].iloc[0:15]
            main(tllist,tt)
        elif tt == '4':
            tvg = nse.volume_gainers()
            tvglist = tvg['SYMBOL'].iloc[0:25]
            main(tvglist,tt)
        elif tt == '5':
            masvol = nse.most_active_stock_volume()
            masvollist = masvol['SYMBOL'].iloc[0:20]
            main(masvollist,tt)
        elif tt == '6':
            masval = nse.most_active_stock_value()
            masvallist = masval['SYMBOL'].iloc[0:20]
            main(masvallist,tt)
        else:
            pass
    except AttributeError:
        pass