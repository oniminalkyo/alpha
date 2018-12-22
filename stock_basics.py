import tushare as ts
import pandas as pd
import datetime


class StockFinanceBasics(object):
    def __init__(self):
        self.data_dir = "./data/"
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

    def init_stock_basics(self):
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


if __name__ == "__main__":
    sb = StockFinanceBasics()
    sb.init_stock_basics()
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



