import pandas as pd

from data_source.config import BASIC_DATA_INFORMATION_FILE
from data_source.config import BASIC_DATA_REPORTS_FILE
from data_source.config import TRANSACTION_DATA_DIR
from data_source.config import ALL_TRANSACTION_DATA_RECORDS


class DataSourceServer(object):
    def __init__(self):
        self.his_data_dir = TRANSACTION_DATA_DIR
        self.all_transaction_data_records = ALL_TRANSACTION_DATA_RECORDS
        self.basic_info_file = BASIC_DATA_INFORMATION_FILE
        self.basic_reports_file = BASIC_DATA_REPORTS_FILE

    def get_all_history_transaction_records(self):
        df = pd.read_csv(self.all_transaction_data_records)
        return df

    def get_basic_information(self):
        df = pd.read_csv(self.basic_info_file)
        return df

    def get_basic_reports(self):
        df = pd.read_csv(self.basic_reports_file)
        return df


if __name__ == "__main__":
    dss = DataSourceServer()
    #records = st.get_all_history_transaction_records()
    records = dss.get_basic_reports()

