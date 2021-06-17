# Turtle trading
import stock_indicator
class Turtle:
    def __init__(self,dataframe):
        self.df = dataframe.iloc[::-1].reset_index(drop=True)
        self.df_55 = self.df.iloc[0:55]
        self.df_20 = self.df.iloc[0:20]
        self.lst_low = float((str(dataframe["Close"].iloc[-1])).replace(',',''))
        self.si = stock_indicator.Indicator(dataframe)

    def filter_(self,df_value):
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
        low = list(self.filter_(self.df_20["Close"]))
        high = list(self.filter_(self.df_55["Close"]))
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
        