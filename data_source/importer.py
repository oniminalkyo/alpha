from data_source.basics import FinanceBasics
from data_source.basics import Classification
from data_source.basics import Transaction


class Importer(object):
    def __init__(self):
        self.basic_importer = FinanceBasics()
        self.classification_importer = Classification()
        self.transaction_importer = Transaction()

    def initialize_all(self):
        #self.basic_importer.initialize()
        #self.basic_importer.init_financial_reports()
        #self.classification_importer.initialize()
        self.transaction_importer.init_all_hist_data()

    def update_latest(self):
        self.transaction_importer.update()


if __name__ == "__main__":
    data_importer = Importer()
    data_importer.initialize_all()
    #data_importer.update_laterst()



