import stock_indicator
class SuperBreakout:
    def __init__(self,dataframe):
        self.si = stock_indicator.Indicator(dataframe)
        self.df = dataframe
    def filter_(self,df_value):
        try:
            value_str=df_value.str.replace(",","") # this is for remove , 
            value_float= value_str.astype(float)    # thid is for string to float value convert
            value = value_float
        except AttributeError:
            value = df_value
        return value

    def breakout(self):
        dataframe = self.filter_(self.df["Close"])
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