import tushare as ts
import pandas as pd
import numpy as np

from config.configuration import Configuration
from data_source.data_server import DataSourceServer


class DistributionEarnRate(object):
    def __init__(self):
        self.config = Configuration()
        self.dss = DataSourceServer()

    def calculate_distribution_earning(self):
        report_df = self.dss.get_basic_reports()
        report_df.drop_duplicates(subset=["code", "distrib", "report_date", "year_quarter"], inplace=True)
        report_df = report_df[~report_df.distrib.isna()]
        report_df = report_df[report_df.distrib.str.contains("派")]
        report_df = report_df[["code", "distrib", "report_date", "year_quarter"]]

        report_group_df = report_df.groupby(["code"])
        distribute_df = report_group_df.size()
        distribute_df.columns = ["code", "distib_num"]
        print(distribute_df)
        distribute_df.to_csv("./distribution.csv", header=True)
        #for code, group in report_group_df:
            #print(code)
            #print(group)

        return report_group_df


if __name__ == "__main__":
    st = DistributionEarnRate()
    st.calculate_distribution_earning()
