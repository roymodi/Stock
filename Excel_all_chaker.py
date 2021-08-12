import os
import pandas as pd
import Nse
import tkinter as tk
from tkinter.constants import FLAT, LEFT, RIGHT

class MainFrame(tk.Frame):
    def __init__(self,window,*args,**kwargs):
        tk.Frame.__init__(self,window,*args,**kwargs)
        self.window = window
        
        self.wd1 = tk.Frame(self.window)
        self.wd1.pack()
        self.label = tk.Label(self.wd1,text='')
        self.label.pack(side=LEFT)

        self.wd2 = tk.Frame(self.window)
        self.wd2.pack()
        self.label1 = tk.Label(self.wd2,text='')
        self.label1.pack(side=LEFT)


        self.wd3 = tk.Frame(self.window)
        self.wd3.pack()
        self.button = tk.Button(self.wd3,text= 'Click',command=self.main,width=5)
        self.button.pack(side= LEFT)

    def main(self):
        try:
            c_dir = os.getcwd()
            f_list = os.listdir(c_dir)

            def find_csv(f_list):
                csv_lis = []
                for x in f_list:
                    if x.endswith('.csv'):
                        csv_lis.append(x)
                    else:
                        pass
                return csv_lis
            f_csv = find_csv(f_list=f_list)
            
            def buy_tiger(file):
                nse = Nse.NSE()
                data = {}
                count = 0
                l_file = pd.read_csv(file)
                df = pd.DataFrame(l_file)
                for x in df['Tiger']:
                    self.label1.config(text='')
                    if x == 'Done':
                        tprice = df['Terget_position'].loc[count]
                        stock = df['Company'].loc[count]
                        si = nse.stock_info(stock)
                        h_value = ((si['Price_Info'])['intraDayHighLow'])['max']
                        data = stock+' Tiger_price: '+str(tprice)+' Sell_done: '+str(h_value)
                        if h_value >= tprice:
                            with open('result.txt','a')as op:
                                op.write(data+'\n\n')
                            print(data)
                    self.label1.config(text=count)
                    print(count)         
                    count+=1
            
            if len(f_csv)==0:
                self.label.config(text='Files not found')
            else:
                no = 0
                for x in f_csv:
                    self.label.config(text='')
                    print(x)
                    buy_tiger(x)
                    self.label.config(text=no)
                    no+=1
        except:
            self.label.config(text='Error')
            print('Error')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock tiger 20Days")
        self.geometry('100x65')
        self.resizable(False,False)


if __name__=="__main__":
    app = App()
    MainFrame(app)
    app.mainloop()

# pyinstaller test_lab.py -w --onefile