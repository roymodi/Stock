class Pivotpoint:
    def __init__(self, dataframe, day=0):
        self.df = dataframe[::-1].reset_index(drop=True)
        self.day = day
    def main(self):
        ldp = self.df.iloc[self.day]
        high = float(str(ldp['High']).replace(',',''))
        low = float(str(ldp['Low']).replace(',',''))
        close = float(str(ldp['Close']).replace(',',''))
        pp = round(((high+low+close)/3),2)
        r1 = round((2*pp-low),2)
        r2 = round((pp+(high-low)),2)
        r3 = round((pp+2*(high-low)),2)
        s1 = round((2*pp-high),2)
        s2 = round((pp-(high-low)),2)
        s3 = round((pp-2*(high-low)),2)
        rdtstr = 'Main_Pivot_level: '+str(pp)+'\n'+'Up_Resistance_level_1: '+str(r1)+'  Down_Support_lavel_1: '+str(s1)+'\n'+'Up_Resistance_level_2: '+str(r2)+'  Down_Support_lavel_2: '+str(s2)+'\n'+'Up_Resistance_level_3: '+str(r3)+ '  Down_Support_lavel_3: '+str(s3)
        rdt = dict(Main_Pivot_level=pp, Up_Resistance_level_1=r1, Down_Support_lavel_1=s1, Up_Resistance_level_2=r2, Down_Support_lavel_2=s2, Up_Resistance_level_3=r3, Down_Support_lavel_3=s3)
        
        return rdt,rdtstr