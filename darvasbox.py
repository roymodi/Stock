import calendar


# noinspection PyGlobalUndefined,PyArgumentList
class DarvasBox:
    def __init__(self, dataframe):
        dataframe.dropna(inplace=True)
        newdf = (dataframe[::-1].reset_index(drop=True)).iloc[0:100]
        reversdf = newdf[::-1].reset_index(drop=True)
        self.df = reversdf
        self.date = self.df['Date']
        self.high = self.df['High']
        self.low = self.df['Low']

    def value(self,df_value):
        try:
            value_str=df_value.str.replace(",","") # this is for remove , 
            value_float= value_str.astype(float)    # thid is for string to float value convert
            value = value_float
        except AttributeError:
            value = df_value
        return value


    def lenth(self,df_value):
        if (len(self.date)) == (len(df_value)):
            ln = len(df_value)
        else:
            ln = 0
        return ln

    @staticmethod
    def weekday(x):
        global no
        date_str = (x.split('-'))
        if date_str[1].isdigit():
            y = int(date_str[0])  # year
            m = int(date_str[1])  # month
            d = int(date_str[2])  # date
            week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            d_num = calendar.weekday(y, m, d)
            day_name = week_day[d_num]
        else:  # this is for Nse dataframe beacuse nse date are defern
            month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            count = 0
            for x in month:
                if x == (date_str[1]):
                    no = count + 1
                    break
                # else:
                #     pass
                count += 1
            d = int(date_str[0])  # year
            m = int(no)  # month
            y = int(date_str[2])
            week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            d_num = calendar.weekday(y, m, d)
            day_name = week_day[d_num]
        return day_name

    @staticmethod
    def chake_wkday(lis, day):  # get days in two list uncomon days
        wk = ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        li = []
        # li.clear()
        for x in wk:
            if x not in lis:
                li.append(x)
                if x == day:
                    break
        return li

    @staticmethod
    def wklis_clear(wklis, wkday):
        new = wklis.copy()
        if len(wklis) == 7:
            new.clear()
        elif (len(wklis) < 7) and wkday == 'Friday':
            new.clear()
        # else:
        #     pass
        return new

    @staticmethod
    def tmp_lis(plis, wklis, wday):
        rt = []
        if len(plis) == 5:
            rt.clear()
        elif len(wklis) == 0:
            rt.clear()
        elif (len(plis) < 5) and (wday == 'Friday'):
            rt.clear()
        else:
            rt.extend(plis)
        return rt

    @staticmethod
    def array(plis, wklis, wd):
        newlis = []
        if (len(wklis) == 7) and (len(plis) <= 5):
            newlis = plis.copy()
        elif (len(wklis) < 7) and (len(plis) < 5) and (wd == 'Friday'):
            newlis = plis.copy()
        # else:
        #     pass
        return newlis

    def main(self,value):
        wklis = []
        mainlis = []
        pricelis = []
        count = 0
        for x in range(self.lenth(value)):
            only_date = ((str(self.date[count])).split())[0]
            wkday = self.weekday(only_date)
            price = float((str(value[count])).replace(',', ''))
            mainlis.append((self.array(pricelis, wklis, wkday))) # array creat pricelist and add mainlis
            wklis = self.wklis_clear(wklis, wkday) # this is creat new wklis
            pricelis=self.tmp_lis(pricelis, wklis, wkday) # this is creat new pricelis 
            mainlis = list(filter(None, mainlis))  # filter [] empity list in mainlist
            if wkday == 'Friday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Monday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Tuesday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Wednesday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            elif wkday == 'Thursday':
                wklis.extend(self.chake_wkday(wklis, wkday))
                pricelis.append(price)
            else:
                pass
            count += 1
        return mainlis,pricelis
    
    def days(self):
        wkl = (self.main(self.value(self.high)))[0]
        lswkln = len(wkl[-1])
        prwkln = len((self.main(self.value(self.high)))[1])
        return lswkln,prwkln

    def box(self):
        high_tup = self.main(self.value(self.high))
        high_1st = round((max((high_tup[0])[-1])),2)
        high_2nd = round((max(high_tup[1])),2)

        low_tup = self.main(self.value(self.low))
        low_1st = round((min((low_tup[0])[-1])),2)
        low_2nd = round((min(low_tup[1])),2)
        
        main_dict = dict(Darvas_High=high_1st,Darvas_Low=low_1st)
        sub_dict = dict(Presend_week_High=high_2nd,Presend_week_Low=low_2nd)
        return main_dict,sub_dict

        