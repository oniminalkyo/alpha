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
        df.reset_index()
        col_name = df.columns.tolist()

        col_name.insert(col_name.index("open"), "code")
        df = df.reindex(columns=col_name)
        df["code"] = str(code)
        df.to_csv(self.his_data_dir + code + ".csv")

        return df

    def init_last_day_data(self):
        df = ts.get_today_all()
        df.to_csv(self.today_all_file)

    def init_all_hist_data(self):
        df = pd.read_csv(self.today_all_file)
        stock_codes = list(df["code"].values)
        print(stock_codes)

        stock_codes = [str(code) for code in stock_codes]
        valid_stock_codes = []
        for code in stock_codes:
            if len(code) == 6:
                valid_stock_codes.append(code)
            else:
                if len(code) == 5:
                    valid_stock_codes.append("0" + code)
                elif len(code) == 4:
                    valid_stock_codes.append("00" + code)
                elif len(code) == 3:
                    valid_stock_codes.append("000" + code)
                elif len(code) == 2:
                    valid_stock_codes.append("0000" + code)
                elif len(code) == 1:
                    valid_stock_codes.append("00000" + code)
                else:
                    valid_stock_codes.append("000000")

        print(valid_stock_codes)
        print(len(valid_stock_codes))
        failed_code = []
        hist_data_df = []
        for code in valid_stock_codes:
            try:
                df = self.init_hist_data(code)
                if hist_data_df is not None and df is not None:
                    hist_data_df.append(df)

            except Exception as e:
                print(str(e))
                failed_code.append(code)

        print(len(failed_code))
        for code in failed_code:
            print(code)
            try:
                df = self.init_hist_data(code)
                if hist_data_df is not None and df is not None:
                    hist_data_df.append(df)

            except Exception as e:
                print("Failed code:" + code)

        all_hist_data_df = pd.concat(hist_data_df)
        all_hist_data_df.sort_values(by="date", inplace=True)
        all_hist_data_df.to_csv(self.hist_data_file)

    def get_all_hist_data(self):
        df = pd.read_csv(self.hist_data_file)
        return df


if __name__ == "__main__":
    st = Transaction()
    #st.init_hist_data()
    #st.init_last_day_data()
    st.init_all_hist_data()
    df = st.get_all_hist_data()
    print(df)
