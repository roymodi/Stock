import stock_indicator
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

    def percent(self,per_val,value):
        per_val = per_val
        percent = per_val/100
        result = percent*value
        return result

    # def swing(self,Close_price):
    #     si = stock_indicator.Indicator(self.df)
    #     dma_200 = si.sma(200)
    #     low = list(self.value(self.newdf["Close"]))
    #     high = list(self.value(self.newdf["Close"]))
    #     low_min = min(low)
    #     high_max = max(high)
    #     if Close_price >= high_max and Close_price >= dma_200:
    #         rt = dict(High_20_days= high_max,Stop_loss_20_days_low= low_min,DMA_200=dma_200,Last_Close_price=Close_price)
    #     else:
    #         rt = None
    #     return rt

    def swing(self,Close_price):
        si = stock_indicator.Indicator(self.df)
        dma_200 = si.sma(200)
        low = list(self.value(self.newdf["Close"]))
        high = list(self.value(self.newdf["Close"]))
        low_min = min(low)
        high_max = max(high)
        per_5 = self.percent(5,high_max)
        if (Close_price >= per_5 and Close_price <= high_max)and Close_price >= dma_200:
            rt = dict(High_20_days= high_max,Stop_loss_20_days_low= low_min,DMA_200=dma_200,Last_Close_price=Close_price)
        else:
            rt = None
        return rt