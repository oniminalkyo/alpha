import tushare as ts


class StockTransaction(object):
    def __init__(self):
        self.base_dir = "./trans_data/"
        self.hist_data_file = self.base_dir + "hist_data.csv"
        self.today_all_file = self.base_dir + "today_all.csv"

    def init_hist_data(self):
        df = ts.get_hist_data("000001")
        df.to_csv(self.hist_data_file)

    def init_last_day_data(self):
        df = ts.get_today_all()
        df.to_csv(self.today_all_file)


if __name__ == "__main__":
    st = StockTransaction()
    st.init_hist_data()
    st.init_last_day_data()
