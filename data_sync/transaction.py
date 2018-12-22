import tushare as ts
import pandas as pd


class Transaction(object):
    def __init__(self):
        self.base_dir = "./"
        self.his_data_dir = "./hist_data/"
        self.hist_data_file = self.his_data_dir + "hist_data.csv"
        self.today_all_file = self.base_dir + "today_all.csv"

    def init_hist_data(self, code):
        df = ts.get_hist_data(code)
        df.to_csv(self.his_data_dir + code + ".csv")

    def init_last_day_data(self):
        df = ts.get_today_all()
        df.to_csv(self.today_all_file)

    def init_all_hist_data(self):
        df = pd.read_csv(self.today_all_file)
        stock_codes = list(df["code"].values)
        stock_codes = [str(code) for code in stock_codes]

        for code in stock_codes:
            print(code)
            self.init_hist_data(code)


if __name__ == "__main__":
    st = Transaction()
    #st.init_hist_data()
    #st.init_last_day_data()
    st.init_all_hist_data()
