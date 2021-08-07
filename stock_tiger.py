import os
from tkinter.constants import FLAT, LEFT, RIGHT
import pandas as pd
import Nse
import tkinter as tk

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
        self.button = tk.Button(self.wd2,text= 'Click',command=self.main,width=5)
        self.button.pack(side= LEFT)
         

    def main(self):
        try:
            c_dir = os.getcwd()
            f_list = os.listdir(c_dir)
            def find_csv(f_list):
                for x in f_list:
                    if x.endswith('.csv'):
                        return x
                    else:
                        pass
            f_csv = find_csv(f_list=f_list)
            f_path = os.path.abspath(f_csv)
            l_file = pd.read_csv(f_path)
            df = pd.DataFrame(l_file)

            nse = Nse.NSE()
            data = {}
            count = 0
            for x in df['Company']:
                self.label.config(text=' ')
                si = nse.stock_info(x)
                h_value = ((si['Price_Info'])['intraDayHighLow'])['max']
                bp_value = df['Buy_position'].iloc[count]
                if bp_value <= h_value:
                    data[x]= h_value
                self.label.config(text=str(count))
                print(count)
                count +=1

            df['Tiger']= ""
            df['T_value']=""

            count = 0
            for x in df['Company']:
                if x in data:
                    df.loc[count,'Tiger'] = 'Done'
                    df.loc[count,'T_value'] = data[x]
                count+=1

            df.to_csv(f_csv)
        except:
            self.label.config(text='File not found')
            print('File not found')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock tiger 20Days")
        self.geometry('100x45')
        self.resizable(False,False)


if __name__=="__main__":
    app = App()
    MainFrame(app)
    app.mainloop()
# pyinstaller stock_tiger.py -w --onefile