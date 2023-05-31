from DatabaseQuery.KeyDataOverview.TopTenShareholdersHoldingShares import TopTenShareholdersHoldingShares
from api_requests.Api_StockLedgerList import Api_StockLedgerList
from api_requests.KeyDataOverviewApi.Api_TopTenShareholdings import Api_TopTenShareholdings
from common.PeriodCombination import PeriodCombination
from common.my_assert import my_assert


class TopTenShareholdingsAssert(object):
    """
    前十大持股排名 对比
    """

    def __init__(self, company_id, accountPassword):
        self.company_id = company_id
        self.accountPassword = accountPassword
        self.params = self.periods_params()

    def periods_params(self):
        datetime, timestamp = Api_StockLedgerList(self.accountPassword)
        return PeriodCombination(timestamp)

    def assert_run(self):
        for param in self.params:
            ttshs = TopTenShareholdersHoldingShares(self.company_id, param[0], param[1])
            # 全部股东
            api_all = Api_TopTenShareholdings(param[0], param[1], 0, self.accountPassword)['wholes']
            database_all = ttshs.all_shareholder_dimensions_top_ten()
            for i in range(len(database_all)):
                my_assert(database_all[i]['zqzhmc'] == api_all[i]['name'], "股东名称对比错误")
                my_assert(int(database_all[i]['t1_cgsl']) == int(api_all[i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_all[i]['t2_cgsl']) == int(api_all[i]['shareholdingNum']), "对比期持股数对比错误")
                my_assert(int(database_all[i]['t1_cgbl']) == int(api_all[i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_all[i]['t2_cgbl']) == int(api_all[i]['shareholdingRatio']), "对比期持股比例对比错误")
                my_assert(int(database_all[i]['diff_cgsl']) == int(api_all[i]['shareholdingChangeNum']), "变动持股数对比错误")
                my_assert(int(database_all[i]['diff_cgbl']) == int(api_all[i]['shareholdingChangeRatio']), "变动持股比例对比错误")

            # 机构股东
            api_institution = Api_TopTenShareholdings(param[0], param[1], 1, self.accountPassword)['mechanisms']
            database_institution = ttshs.institution_shareholder_dimensions_top_ten()
            for i in range(len(database_institution)):
                my_assert(database_institution[i]['party_full_name'] == api_institution[i]['mechanismName'], "机构名称对比错误")
                my_assert(int(database_institution[i]['product_cnt']) == int(api_institution[i]['productNum']), "产品数对比错误")
                my_assert(int(database_institution[i]['t1_cgsl']) == int(api_institution[i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_institution[i]['t2_cgsl']) == int(api_institution[i]['shareholdingNum']), "对比期持股数对比错误")
                my_assert(int(database_institution[i]['t1_cgbl']) == int(api_institution[i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_institution[i]['t2_cgbl']) == int(api_institution[i]['shareholdingRatio']), "对比期持股比例对比错误")
                my_assert(int(database_institution[i]['diff_cgsl']) == int(api_institution[i]['shareholdingChangeNum']), "变动持股数对比错误")
                my_assert(int(database_institution[i]['diff_cgbl']) == int(api_institution[i]['shareholdingChangeRatio']), "变动持股比例对比错误")

            # 产品维度
            api_product = Api_TopTenShareholdings(param[0], param[1], 2, self.accountPassword)['products']
            database_product = ttshs.product_dimensions_top_ten()
            for i in range(len(database_product)):
                my_assert(database_product[i]['fund_full_name'] == api_product[i]['productName'], "产品名称对比错误")
                my_assert(int(database_product[i]['t1_cgsl']) == int(api_product[i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_product[i]['t2_cgsl']) == int(api_product[i]['shareholdingNum']), "对比期持股数对比错误")
                my_assert(int(database_product[i]['t1_cgbl']) == int(api_product[i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_product[i]['t2_cgbl']) == int(api_product[i]['shareholdingRatio']), "对比期持股比例对比错误")
                my_assert(int(database_product[i]['diff_cgsl']) == int(api_product[i]['shareholdingChangeNum']), "变动持股数对比错误")
                my_assert(int(database_product[i]['diff_cgbl']) == int(api_product[i]['shareholdingChangeRatio']), "变动持股比例对比错误")

            # 个人股东
            api_individual = Api_TopTenShareholdings(param[0], param[1], 3, self.accountPassword)['wholes']
            database_individual = ttshs.individual_shareholder_dimensions_top_ten()
            for i in range(len(database_individual)):
                my_assert(database_individual[i]['zqzhmc'] == api_individual[i]['name'], "股东名称对比错误")
                my_assert(int(database_individual[i]['t1_cgsl']) == int(api_individual[i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_individual[i]['t2_cgsl']) == int(api_individual[i]['shareholdingNum']), "对比期持股数对比错误")
                my_assert(int(database_individual[i]['t1_cgbl']) == int(api_individual[i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_individual[i]['t2_cgbl']) == int(api_individual[i]['shareholdingRatio']), "对比期持股比例对比错误")
                my_assert(int(database_individual[i]['diff_cgsl']) == int(api_individual[i]['shareholdingChangeNum']), "变动持股数对比错误")
                my_assert(int(database_individual[i]['diff_cgbl']) == int(api_individual[i]['shareholdingChangeRatio']), "变动持股比例对比错误")

            # 基金经理
            # TODO

            print("{}-{},对比完成".format(str(param[0]), str(param[1])))


if __name__ == '__main__':
    d = TopTenShareholdingsAssert(774, [])
    d.assert_run()
