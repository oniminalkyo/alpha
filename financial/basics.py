import tushare as ts
import pandas as pd
import datetime

from financial.config import BASIC_DATA_DIR


class FinanceBasics(object):
    def __init__(self):
        self.data_dir = BASIC_DATA_DIR
        self.basics_file = self.data_dir + "basics.csv"
        self.reports_file = self.data_dir + "reports.csv"
        self.profit_file = self.data_dir + "profit.csv"
        self.operation_file = self.data_dir + "operation.csv"
        self.growth_file = self.data_dir + "growth.csv"
        self.debt_paying_file = self.data_dir + "debt_paying.csv"
        self.cash_flow_file = self.data_dir + "cash_flow.csv"

        self.report_handlers = [
            (self.reports_file, ts.get_report_data),
            (self.profit_file, ts.get_profit_data),
            (self.operation_file, ts.get_operation_data),
            (self.growth_file, ts.get_growth_data),
            (self.debt_paying_file, ts.get_debtpaying_data),
            (self.cash_flow_file, ts.get_cashflow_data),
        ]

        self._init_year_quarters()

    def _init_year_quarters(self):
        self.years = [2015, 2016, 2017, 2018]
        self.quarters = [1, 2, 3, 4]

        current_year = datetime.datetime.now()
        if current_year.year not in self.years:
            self.years.append(current_year.year)

    def initialize(self):
        df = ts.get_stock_basics()
        df.to_csv(self.basics_file)

    @staticmethod
    def _get_basics_financial_data_by_quarter(year, quarter, handler):
        try:
            financial_data = handler(year, quarter)
        except Exception as e:
            print(e)
            raise Exception("Failed to get the financial data")
        return financial_data

    def _init_year_quarter_report(self, stored_file_name, handler):
        financial_data_frames = []
        for year in self.years:
            for quarter in self.quarters:
                try:
                    financial_data = self._get_basics_financial_data_by_quarter(year, quarter, handler)
                except Exception as e:
                    print("Failed to get finance data for year: %d, quarter: %d" % (year, quarter))
                    break

                year_quarter = "%d_%d" % (year, quarter)
                financial_data["year_quarter"] = year_quarter
                financial_data_frames.append(financial_data)

        reports_df = pd.concat(financial_data_frames)
        reports_df.to_csv(stored_file_name)

    def init_financial_reports(self):
        for stored_file_name, handler in self.report_handlers:
            self._init_year_quarter_report(stored_file_name, handler)

    def get_stock_basics(self):
        df = pd.read_csv(self.basics_file)
        return df

    def get_stock_reports(self):
        df = pd.read_csv(self.reports_file)
        return df

    def get_stock_profit_reports(self):
        df = pd.read_csv(self.profit_file)
        return df

    def get_stock_operation_reports(self):
        df = pd.read_csv(self.operation_file)
        return df

    def get_stock_growth_reports(self):
        df = pd.read_csv(self.growth_file)
        return df

    def get_stock_debt_paying_reports(self):
        df = pd.read_csv(self.debt_paying_file)
        return df

    def get_stock_cash_flow_reports(self):
        df = pd.read_csv(self.cash_flow_file)
        return df


class Classification(object):
    def __init__(self):
        self.base_dir = BASIC_DATA_DIR
        self.industry_file = self.base_dir + "industry.csv"
        self.concept_class_file = self.base_dir + "concept_class.csv"
        self.area_class_file = self.base_dir + "area_class.csv"
        self.sme_class_file = self.base_dir + "sme_class.csv"
        self.gem_class_file = self.base_dir + "gem_class.csv"
        self.hs300_class_file = self.base_dir + "hs300_class.csv"
        self.sz50_class_file = self.base_dir + "sz50_class.csv"
        self.zz500_class_file = self.base_dir + "zz500_class.csv"
        self.terminated_class_file = self.base_dir + "terminated_class.csv"
        self.suspended_class_file = self.base_dir + "sus_class.csv"
        self.st_class_file = self.base_dir + "st_class.csv"
        self.basic_info = self.base_dir + "basic_info.csv"

    def initialize(self):
        industry_df = self.init_classification()
        concept_df = self.init_concept_class()
        area_df = self.init_area_class()
        sme_df = self.init_sme_class()
        st_df = self.init_st_class()
        gme_df = self.init_gem_class()
        #self.init_hs300_class()
        #self.init_sz50_class()
        #self.init_zz500s_class()
        #self.init_suspended_class()
        #self.init_terminated_class()

        class_df = pd.merge(area_df, industry_df, on="code", how="left")
        class_df.drop(["name_y"], axis=1, inplace=True)

        def _stock_class(code):
            if code[0:3] in ["600", "601", "603"]:
                return "沪市A股"

            if code[0:3] in ["000"]:
                return "深市A股"

            if code[0:3] in ["300"]:
                return "中小板"

            if code[0:3] in ["002"]:
                return "创业板"

        class_df["股票类别"] = class_df.code.apply(_stock_class)
        class_df["c_name"].fillna("其它行业", inplace=True)

        class_df.rename(
            columns={
                "code": "股票代码",
                "name_x": "股票名称",
                "area": "公司所在地",
                "c_name": "所属行业"
            },
            inplace=True
        )
        class_df.drop_duplicates(subset=["股票代码"], inplace=True)
        print(class_df)
        class_df.to_csv(self.basic_info)

    def init_classification(self):
        df = ts.get_industry_classified()
        df.to_csv(self.industry_file)
        return df

    def init_concept_class(self):
        df = ts.get_concept_classified()
        df.to_csv(self.concept_class_file)
        return df

    def init_area_class(self):
        df = ts.get_area_classified()
        df.to_csv(self.area_class_file)
        return df

    def init_sme_class(self):
        df = ts.get_sme_classified()
        df.to_csv(self.sme_class_file)
        return df

    def init_gem_class(self):
        df = ts.get_gem_classified()
        df.to_csv(self.gem_class_file)
        return df

    def init_st_class(self):
        df = ts.get_st_classified()
        df.to_csv(self.st_class_file)

    def init_hs300_class(self):
        df = ts.get_hs300s()
        df.to_csv(self.hs300_class_file)

    def init_sz50_class(self):
        df = ts.get_sz50s()
        df.to_csv(self.sz50_class_file)

    def init_zz500s_class(self):
        df = ts.get_zz500s()
        df.to_csv(self.zz500_class_file)

    def init_terminated_class(self):
        df = ts.get_terminated()
        df.to_csv(self.terminated_class_file)

    def init_suspended_class(self):
        df = ts.get_suspended()
        df.to_csv(self.suspended_class_file)


class Transaction(object):
    def __init__(self):
        self.his_data_dir = "./transaction_data/"
        self.hist_data_file = self.his_data_dir + "hist_data.csv"
        self.today_all_file = self.his_data_dir + "today_all.csv"
        self.basic_data_file = BASIC_DATA_DIR + "basic_info.csv"

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
        df = pd.read_csv(self.basic_data_file)
        stock_codes = list(df["股票代码"].values)
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
    sb = FinanceBasics()
    sb.initialize()
    stock = sb.get_stock_basics()
    print(stock)

    sb.init_financial_reports()

    reports = sb.get_stock_reports()
    print(reports)

    reports = sb.get_stock_operation_reports()
    print(reports)

    reports = sb.get_stock_growth_reports()
    print(reports)

    reports = sb.get_stock_debt_paying_reports()
    print(reports)

    reports = sb.get_stock_cash_flow_reports()
    print(reports)



