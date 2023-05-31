from DatabaseQuery.KeyDataOverview.TopTenChangeShareholdersHoldingShares import TopTenChangeShareholdersHoldingShares
from api_requests.Api_StockLedgerList import Api_StockLedgerList
from api_requests.KeyDataOverviewApi.Api_TopTenChangeShareholdings import Api_TopTenChangeShareholdings
from common.PeriodCombination import PeriodCombination
from common.my_assert import my_assert


class TopTenChangeShareholdingsAssert(object):
    """
    前十大变动股东排名 对比
    """

    def __init__(self, company_id, accountPassword):
        self.company_id = company_id
        self.accountPassword = accountPassword
        self.params = self.periods_params()

    def periods_params(self):
        datetime, timestamp = Api_StockLedgerList(self.accountPassword)
        return PeriodCombination(timestamp)

    def all_assert_run(self):
        for param in self.params:
            ttchs = TopTenChangeShareholdersHoldingShares(self.company_id, param[0], param[1])
            # 全部股东
            api_all = Api_TopTenChangeShareholdings(param[0], param[1], 0, self.accountPassword)
            database_all = ttchs.all_shareholder_dimensions_top_ten_change()

            # 增持
            for i in range(len(database_all["increase_changelist"])):
                my_assert(database_all['increase_changelist'][i]['zqzhmc'] == api_all['upChanges'][i][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_all['increase_changelist'][i]['t1_cgsl']) == int(
                    api_all['upChanges'][i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_all['increase_changelist'][i]['t2_cgsl']) == int(
                    api_all['upChanges'][i]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_all['increase_changelist'][i]['t1_cgbl']) == int(
                    api_all['upChanges'][i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_all['increase_changelist'][i]['t2_cgbl']) == int(
                    api_all['upChanges'][i]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_all['increase_changelist'][i]['diff_cgsl']) == int(
                    api_all['upChanges'][i]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_all['increase_changelist'][i]['diff_cgbl']) == int(
                    api_all['upChanges'][i]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 全部股东-增持,对比完成".format(str(param[0]), str(param[1])))

            # 新增
            for k in range(len(database_all["new_entry_changelist"])):
                my_assert(database_all['new_entry_changelist'][k]['zqzhmc'] == api_all['inChanges'][k][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_all['new_entry_changelist'][k]['t1_cgsl']) == int(
                    api_all['inChanges'][k]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_all['new_entry_changelist'][k]['t2_cgsl']) == int(
                    api_all['inChanges'][k]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_all['new_entry_changelist'][k]['t1_cgbl']) == int(
                    api_all['inChanges'][k]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_all['new_entry_changelist'][k]['t2_cgbl']) == int(
                    api_all['inChanges'][k]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_all['new_entry_changelist'][k]['diff_cgsl']) == int(
                    api_all['inChanges'][k]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_all['new_entry_changelist'][k]['diff_cgbl']) == int(
                    api_all['inChanges'][k]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 全部股东-新增,对比完成".format(str(param[0]), str(param[1])))

            # 减持
            for j in range(len(database_all["decrease_changelist"])):
                my_assert(database_all['decrease_changelist'][j]['zqzhmc'] == api_all['downChanges'][j][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_all['decrease_changelist'][j]['t1_cgsl']) == int(
                    api_all['downChanges'][j]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_all['decrease_changelist'][j]['t2_cgsl']) == int(
                    api_all['downChanges'][j]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_all['decrease_changelist'][j]['t1_cgbl']) == int(
                    api_all['downChanges'][j]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_all['decrease_changelist'][j]['t2_cgbl']) == int(
                    api_all['downChanges'][j]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_all['decrease_changelist'][j]['diff_cgsl']) == int(
                    api_all['downChanges'][j]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_all['decrease_changelist'][j]['diff_cgbl']) == int(
                    api_all['downChanges'][j]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 全部股东-减持,对比完成".format(str(param[0]), str(param[1])))

            # 退出
            for l in range(len(database_all["exit_changelist"])):
                my_assert(database_all['exit_changelist'][l]['zqzhmc'] == api_all['outChanges'][l][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_all['exit_changelist'][l]['t1_cgsl']) == int(
                    api_all['outChanges'][l]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_all['exit_changelist'][l]['t2_cgsl']) == int(
                    api_all['outChanges'][l]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_all['exit_changelist'][l]['t1_cgbl']) == int(
                    api_all['outChanges'][l]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_all['exit_changelist'][l]['t2_cgbl']) == int(
                    api_all['outChanges'][l]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_all['exit_changelist'][l]['diff_cgsl']) == int(
                    api_all['outChanges'][l]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_all['exit_changelist'][l]['diff_cgbl']) == int(
                    api_all['outChanges'][l]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 全部股东-退出,对比完成".format(str(param[0]), str(param[1])))

    def institution_assert_run(self):
        for param in self.params:
            ttchs = TopTenChangeShareholdersHoldingShares(self.company_id, param[0], param[1])

            # 机构股东
            api_institution = Api_TopTenChangeShareholdings(param[0], param[1], 1, self.accountPassword)
            database_institution = ttchs.institution_shareholder_dimensions_top_ten_change()

            # 增持
            for i in range(len(database_institution["increase_changelist"])):
                my_assert(database_institution['increase_changelist'][i]['party_full_name'] ==
                          api_institution['upChanges'][i][
                              'mechanismName'], "机构名称对比错误")
                my_assert(int(database_institution['increase_changelist'][i]['t1_cgsl']) == int(
                    api_institution['upChanges'][i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_institution['increase_changelist'][i]['t2_cgsl']) == int(
                    api_institution['upChanges'][i]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_institution['increase_changelist'][i]['t1_cgbl']) == int(
                    api_institution['upChanges'][i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_institution['increase_changelist'][i]['t2_cgbl']) == int(
                    api_institution['upChanges'][i]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_institution['increase_changelist'][i]['diff_cgsl']) == int(
                    api_institution['upChanges'][i]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_institution['increase_changelist'][i]['diff_cgbl']) == int(
                    api_institution['upChanges'][i]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 机构股东-增持,对比完成".format(str(param[0]), str(param[1])))

            # 新增
            for k in range(len(database_institution["new_entry_changelist"])):
                my_assert(database_institution['new_entry_changelist'][k]['party_full_name'] ==
                          api_institution['inChanges'][k][
                              'mechanismName'], "机构名称对比错误")
                my_assert(int(database_institution['new_entry_changelist'][k]['t1_cgsl']) == int(
                    api_institution['inChanges'][k]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_institution['new_entry_changelist'][k]['t2_cgsl']) == int(
                    api_institution['inChanges'][k]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_institution['new_entry_changelist'][k]['t1_cgbl']) == int(
                    api_institution['inChanges'][k]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_institution['new_entry_changelist'][k]['t2_cgbl']) == int(
                    api_institution['inChanges'][k]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_institution['new_entry_changelist'][k]['diff_cgsl']) == int(
                    api_institution['inChanges'][k]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_institution['new_entry_changelist'][k]['diff_cgbl']) == int(
                    api_institution['inChanges'][k]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 机构股东-新增,对比完成".format(str(param[0]), str(param[1])))

            # 减持
            for j in range(len(database_institution["decrease_changelist"])):
                my_assert(database_institution['decrease_changelist'][j]['party_full_name'] ==
                          api_institution['downChanges'][j][
                              'mechanismName'], "机构名称对比错误")
                my_assert(int(database_institution['decrease_changelist'][j]['t1_cgsl']) == int(
                    api_institution['downChanges'][j]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_institution['decrease_changelist'][j]['t2_cgsl']) == int(
                    api_institution['downChanges'][j]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_institution['decrease_changelist'][j]['t1_cgbl']) == int(
                    api_institution['downChanges'][j]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_institution['decrease_changelist'][j]['t2_cgbl']) == int(
                    api_institution['downChanges'][j]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_institution['decrease_changelist'][j]['diff_cgsl']) == int(
                    api_institution['downChanges'][j]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_institution['decrease_changelist'][j]['diff_cgbl']) == int(
                    api_institution['downChanges'][j]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 机构股东-减持,对比完成".format(str(param[0]), str(param[1])))

            # 退出
            for l in range(len(database_institution["exit_changelist"])):
                my_assert(
                    database_institution['exit_changelist'][l]['party_full_name'] == api_institution['outChanges'][l][
                        'mechanismName'], "机构名称对比错误")
                my_assert(int(database_institution['exit_changelist'][l]['t1_cgsl']) == int(
                    api_institution['outChanges'][l]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_institution['exit_changelist'][l]['t2_cgsl']) == int(
                    api_institution['outChanges'][l]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_institution['exit_changelist'][l]['t1_cgbl']) == int(
                    api_institution['outChanges'][l]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_institution['exit_changelist'][l]['t2_cgbl']) == int(
                    api_institution['outChanges'][l]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_institution['exit_changelist'][l]['diff_cgsl']) == int(
                    api_institution['outChanges'][l]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_institution['exit_changelist'][l]['diff_cgbl']) == int(
                    api_institution['outChanges'][l]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 机构股东-退出,对比完成".format(str(param[0]), str(param[1])))

    def product_assert_run(self):
        for param in self.params:
            ttchs = TopTenChangeShareholdersHoldingShares(self.company_id, param[0], param[1])

            # 产品维度
            api_product = Api_TopTenChangeShareholdings(param[0], param[1], 2, self.accountPassword)
            database_product = ttchs.product_dimensions_top_ten_change()

            # 增持
            for i in range(len(database_product["increase_changelist"])):
                my_assert(database_product['increase_changelist'][i]['fund_full_name'] == api_product['upChanges'][i][
                    'productName'], "产品名称对比错误")
                my_assert(int(database_product['increase_changelist'][i]['t1_cgsl']) == int(
                    api_product['upChanges'][i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_product['increase_changelist'][i]['t2_cgsl']) == int(
                    api_product['upChanges'][i]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_product['increase_changelist'][i]['t1_cgbl']) == int(
                    api_product['upChanges'][i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_product['increase_changelist'][i]['t2_cgbl']) == int(
                    api_product['upChanges'][i]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_product['increase_changelist'][i]['diff_cgsl']) == int(
                    api_product['upChanges'][i]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_product['increase_changelist'][i]['diff_cgbl']) == int(
                    api_product['upChanges'][i]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 产品维度-增持,对比完成".format(str(param[0]), str(param[1])))

            # 新增
            for k in range(len(database_product["new_entry_changelist"])):
                my_assert(database_product['new_entry_changelist'][k]['fund_full_name'] == api_product['inChanges'][k][
                    'productName'], "产品名称对比错误")
                my_assert(int(database_product['new_entry_changelist'][k]['t1_cgsl']) == int(
                    api_product['inChanges'][k]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_product['new_entry_changelist'][k]['t2_cgsl']) == int(
                    api_product['inChanges'][k]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_product['new_entry_changelist'][k]['t1_cgbl']) == int(
                    api_product['inChanges'][k]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_product['new_entry_changelist'][k]['t2_cgbl']) == int(
                    api_product['inChanges'][k]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_product['new_entry_changelist'][k]['diff_cgsl']) == int(
                    api_product['inChanges'][k]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_product['new_entry_changelist'][k]['diff_cgbl']) == int(
                    api_product['inChanges'][k]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 产品维度-新增,对比完成".format(str(param[0]), str(param[1])))

            # 减持
            for j in range(len(database_product["decrease_changelist"])):
                my_assert(database_product['decrease_changelist'][j]['fund_full_name'] == api_product['downChanges'][j][
                    'productName'], "产品名称对比错误")
                my_assert(int(database_product['decrease_changelist'][j]['t1_cgsl']) == int(
                    api_product['downChanges'][j]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_product['decrease_changelist'][j]['t2_cgsl']) == int(
                    api_product['downChanges'][j]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_product['decrease_changelist'][j]['t1_cgbl']) == int(
                    api_product['downChanges'][j]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_product['decrease_changelist'][j]['t2_cgbl']) == int(
                    api_product['downChanges'][j]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_product['decrease_changelist'][j]['diff_cgsl']) == int(
                    api_product['downChanges'][j]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_product['decrease_changelist'][j]['diff_cgbl']) == int(
                    api_product['downChanges'][j]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 产品维度-减持,对比完成".format(str(param[0]), str(param[1])))

            # 退出
            for l in range(len(database_product["exit_changelist"])):
                my_assert(database_product['exit_changelist'][l]['fund_full_name'] == api_product['outChanges'][l][
                    'productName'], "产品名称对比错误")
                my_assert(int(database_product['exit_changelist'][l]['t1_cgsl']) == int(
                    api_product['outChanges'][l]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_product['exit_changelist'][l]['t2_cgsl']) == int(
                    api_product['outChanges'][l]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_product['exit_changelist'][l]['t1_cgbl']) == int(
                    api_product['outChanges'][l]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_product['exit_changelist'][l]['t2_cgbl']) == int(
                    api_product['outChanges'][l]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_product['exit_changelist'][l]['diff_cgsl']) == int(
                    api_product['outChanges'][l]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_product['exit_changelist'][l]['diff_cgbl']) == int(
                    api_product['outChanges'][l]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 产品维度-退出,对比完成".format(str(param[0]), str(param[1])))

    def individual_assert_run(self):
        for param in self.params:
            ttchs = TopTenChangeShareholdersHoldingShares(self.company_id, param[0], param[1])
            # 个人股东
            api_individual = Api_TopTenChangeShareholdings(param[0], param[1], 3, self.accountPassword)
            database_individual = ttchs.individual_shareholder_dimensions_top_ten_change()

            # 增持
            for i in range(len(database_individual["increase_changelist"])):
                my_assert(database_individual['increase_changelist'][i]['zqzhmc'] == api_individual['upChanges'][i][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_individual['increase_changelist'][i]['t1_cgsl']) == int(
                    api_individual['upChanges'][i]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_individual['increase_changelist'][i]['t2_cgsl']) == int(
                    api_individual['upChanges'][i]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_individual['increase_changelist'][i]['t1_cgbl']) == int(
                    api_individual['upChanges'][i]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_individual['increase_changelist'][i]['t2_cgbl']) == int(
                    api_individual['upChanges'][i]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_individual['increase_changelist'][i]['diff_cgsl']) == int(
                    api_individual['upChanges'][i]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_individual['increase_changelist'][i]['diff_cgbl']) == int(
                    api_individual['upChanges'][i]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 个人股东-增持,对比完成".format(str(param[0]), str(param[1])))

            # 新增
            for k in range(len(database_individual["new_entry_changelist"])):
                my_assert(database_individual['new_entry_changelist'][k]['zqzhmc'] == api_individual['inChanges'][k][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_individual['new_entry_changelist'][k]['t1_cgsl']) == int(
                    api_individual['inChanges'][k]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_individual['new_entry_changelist'][k]['t2_cgsl']) == int(
                    api_individual['inChanges'][k]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_individual['new_entry_changelist'][k]['t1_cgbl']) == int(
                    api_individual['inChanges'][k]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_individual['new_entry_changelist'][k]['t2_cgbl']) == int(
                    api_individual['inChanges'][k]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_individual['new_entry_changelist'][k]['diff_cgsl']) == int(
                    api_individual['inChanges'][k]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_individual['new_entry_changelist'][k]['diff_cgbl']) == int(
                    api_individual['inChanges'][k]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 个人股东-新增,对比完成".format(str(param[0]), str(param[1])))

            # 减持
            for j in range(len(database_individual["decrease_changelist"])):
                my_assert(database_individual['decrease_changelist'][j]['zqzhmc'] == api_individual['downChanges'][j][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_individual['decrease_changelist'][j]['t1_cgsl']) == int(
                    api_individual['downChanges'][j]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_individual['decrease_changelist'][j]['t2_cgsl']) == int(
                    api_individual['downChanges'][j]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_individual['decrease_changelist'][j]['t1_cgbl']) == int(
                    api_individual['downChanges'][j]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_individual['decrease_changelist'][j]['t2_cgbl']) == int(
                    api_individual['downChanges'][j]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_individual['decrease_changelist'][j]['diff_cgsl']) == int(
                    api_individual['downChanges'][j]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_individual['decrease_changelist'][j]['diff_cgbl']) == int(
                    api_individual['downChanges'][j]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 个人股东-减持,对比完成".format(str(param[0]), str(param[1])))

            # 退出
            for l in range(len(database_individual["exit_changelist"])):
                my_assert(database_individual['exit_changelist'][l]['zqzhmc'] == api_individual['outChanges'][l][
                    'securitiesAccountName'], "股东名称对比错误")
                my_assert(int(database_individual['exit_changelist'][l]['t1_cgsl']) == int(
                    api_individual['outChanges'][l]['shareholdingNumCurrent']), "当前期持股数对比错误")
                my_assert(int(database_individual['exit_changelist'][l]['t2_cgsl']) == int(
                    api_individual['outChanges'][l]['shareholdingNumContrast']), "对比期持股数对比错误")
                my_assert(int(database_individual['exit_changelist'][l]['t1_cgbl']) == int(
                    api_individual['outChanges'][l]['shareholdingRatioCurrent']), "当前期持股比例对比错误")
                my_assert(int(database_individual['exit_changelist'][l]['t2_cgbl']) == int(
                    api_individual['outChanges'][l]['shareholdingRatioContrast']), "对比期持股比例对比错误")
                my_assert(int(database_individual['exit_changelist'][l]['diff_cgsl']) == int(
                    api_individual['outChanges'][l]['shareholdingNum']), "变动持股数对比错误")
                my_assert(int(database_individual['exit_changelist'][l]['diff_cgbl']) == int(
                    api_individual['outChanges'][l]['shareholdingRatio']), "变动持股比例对比错误")

            print("{}-{} 个人股东-退出,对比完成".format(str(param[0]), str(param[1])))

            # 基金经理
            # TODO

            print("{}-{},对比完成".format(str(param[0]), str(param[1])))

    def assert_run(self):
        self.all_assert_run()
        self.institution_assert_run()
        self.product_assert_run()
        self.individual_assert_run()


if __name__ == '__main__':
    d = TopTenChangeShareholdingsAssert(774, [])
    d.all_assert_run()
