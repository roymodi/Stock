from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

"""x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state = 10)
As many times as you rerun the above code, you’ll get a different result every time.
This is because the train_test_split() function picks up the random rows every time,
and it’s good for our machine-learning model.
If you don’t want the train_test_split() function to pick up the random rows,
then you can do so by setting (random_state = 10)."""


class MLStockPredction:
    def __init__(self, dataframe):
        """.dropna is remove missing value in dataframe """
        dataframe.dropna(inplace=True)
        self.df = dataframe
        self.op_vol = self.df[['Open', 'Volume']]
        self.cl_vol = self.df[['Close', 'Volume']]
        self.lo = self.df['Low']
        self.hi = self.df['High']
        self.op = self.df['Open']

    @staticmethod
    def main(x, y, val_1, val_2):
        scale = StandardScaler()
        scale_x = scale.fit_transform(x)
        x_train, x_test, y_train, y_test = train_test_split(scale_x, y, test_size=0.2)
        model = LinearRegression()
        model.fit(x_train, y_train)
        model.predict(x_test)
        acc = model.score(x_test, y_test)
        scaled_value = scale.transform([[val_1, val_2]])
        predict_value = model.predict([scaled_value[0]])
        return predict_value, acc

    def open_value(self, day=0):
        rev_df = self.df[::-1].reset_index(drop=True)
        val_1 = rev_df['Close'].iloc[day]
        val_2 = rev_df['Volume'].iloc[day]
        open_val = self.main(self.cl_vol, self.op, val_1, val_2)
        return open_val

    def high_value(self, day=0):
        rev_df = self.df[::-1].reset_index(drop=True)
        val_1 = ((self.open_value(day))[0])[0]
        val_2 = rev_df['Volume'].iloc[day]
        high_val = self.main(self.op_vol, self.hi, val_1, val_2)
        return high_val

    def low_value(self, day=0):
        rev_df = self.df[::-1].reset_index(drop=True)
        val_1 = ((self.open_value(day))[0])[0]
        val_2 = rev_df['Volume'].iloc[day]
        low_val = self.main(self.op_vol, self.lo, val_1, val_2)
        return low_val

    def predction(self, day=0):
        dt = self.df[::-1].reset_index(drop=True)
        date = dt['Date'].iloc[day]
        op = self.open_value(day)
        op_val = float((op[0])[0])
        op_acc = float(op[1])
        hi = self.high_value(day)
        hi_val = float((hi[0])[0])
        hi_acc = float(hi[1])
        lo = self.low_value(day)
        lo_val = float((lo[0])[0])
        lo_acc = float(lo[1])
        total_acc = (op_acc + hi_acc + lo_acc) / 3
        alldict = dict(OPEN=round(op_val, 2), HIGH=round(hi_val, 2), LOW=round(lo_val, 2), Accourancy=total_acc, Before_Date=date)
        return alldict
