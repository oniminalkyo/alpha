import tushare as ts
import pandas as pd


class Classification(object):
    def __init__(self):
        self.base_dir = "./basic_data/"
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


if __name__ == "__main__":
    sc = Classification()
    sc.initialize()
