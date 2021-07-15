import os
import pandas as pd
import Nse

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
        si = nse.stock_info(x)
        h_value = ((si['Price_Info'])['intraDayHighLow'])['max']
        bp_value = df['Buy_position'].iloc[count]
        if bp_value <= h_value:
            data[x]= bp_value
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
    print('File not find')

# pyinstaller test_lab.py --onefile