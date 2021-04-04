import datetime


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