import numpy


# noinspection PyGlobalUndefined
class Indicator:
    def __init__(self, DataFrame):
        self.df = DataFrame.iloc[::-1].reset_index(drop=True)
        cpl = self.df["Close"]
        self.close_price_list = list(reversed(list(cpl)))

    # noinspection PyBroadException
    def lenthlist(self, n):
        temp = []
        count = 0
        for x in self.close_price_list:
            try:
                temp.append(float(x.replace(',', '')))
            except AttributeError:
                temp.append(x)
            if count == n:
                break
            count += 1
        return temp

    def rsi(self, num):
        cpl = list(reversed(self.lenthlist(num)))
        tmp = [0]
        change = [0]
        gain = [0]
        lose = [0]
        for x in cpl:
            tmp.append(x)
            if len(tmp) == 3:
                ch = float(tmp[1]) - float(tmp[2])
                change.append(ch)
                tmp.pop(1)
                if (change[1]) < 0:
                    lose.append(abs(change[1]))
                    change.pop(1)
                else:
                    gain.append(change[1])
                    change.pop(1)
        average_gain = sum(gain) / 14
        average_lose = sum(lose) / 14
        rs = average_lose / average_gain 
        rsi_ = 100 - (100 / (1 + rs))
        rsi = round(rsi_, 2)
        return rsi

    def sma(self, no):
        cplis = self.lenthlist(no)
        cplenth = len(cplis)
        sma = round((sum(cplis) / cplenth), 2)
        return round(sma, 2)

    def ema(self, days):
        sma = self.sma(days)
        k = 2 / (days + 1)
        clpric = (self.lenthlist(0))[0]
        ema = clpric * k + sma * (1 - k)
        return round(ema, 2)

    def macd(self):
        global condition
        macd_line = self.ema(12)
        signal_line = self.ema(26)
        zero_line = self.ema(9)

        bull = macd_line > signal_line
        bear = macd_line < signal_line
        bulst1 = macd_line > zero_line
        bulst2 = signal_line > zero_line
        barst1 = macd_line < zero_line
        barst2 = signal_line < zero_line

        if bull and barst1 and barst2:
            condition = 'Bullish_crossover'
        elif bear and bulst1 and bulst2:
            condition = 'Bearish_crossover'
        elif bull and bulst1 and bulst2:
            condition = 'Strong_bullish_trend'
        elif bear and barst1 and barst2:
            condition = 'Strong_bearish_trend'
        elif bull and bulst1 and barst2:
            condition = 'Wipshaw'
        elif bear and bulst2 and barst1:
            condition = 'Wipshaw'

        return condition
    
    def bollinger_bands(self):
        stdlist = self.lenthlist(20)
        bbstd = numpy.std(stdlist)
        bbsma = self.sma(20)
        upper = round((bbsma + (bbstd * 2)),2)
        lower = round((bbsma - (bbstd*2)),2)
        bbresult = dict(Upper_Band=upper, Middle_Band=bbsma, Lower_Band=lower)
        return bbresult
