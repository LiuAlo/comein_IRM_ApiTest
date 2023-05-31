from DatabaseQuery.KeyDataOverview.DataOverviewSinglePeriod import DataOverviewSinglePeriod
from api_requests.KeyDataOverviewApi.Api_DataStatistics import Api_DataStatistics
from common.PeriodCombination import PeriodCombination
from api_requests.Api_StockLedgerList import Api_StockLedgerList
from common.my_assert import my_assert


class DataStatisticsAssert(object):
    """
    数据统计 对比
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
            api_resulf = Api_DataStatistics(param[0], param[1], self.accountPassword)
            databasequery_resulf = DataOverviewSinglePeriod(self.company_id, param[0]).overview_of_roster_data()
            my_assert(int(databasequery_resulf['gdzs']) == int(api_resulf['shareholderNum']), "总户数对比错误")
            my_assert(int(databasequery_resulf['jggdzs']) == int(api_resulf['mechanismNum']), "机构户数对比错误")
            my_assert(int(databasequery_resulf['grgdzs']) == int(api_resulf['personalNum']), "个人户数对比错误")
            my_assert(int(databasequery_resulf['ltgdzs']) == int(api_resulf['circulationNum']), "流通户数对比错误")
            my_assert(int(databasequery_resulf['xygdzs']) == int(api_resulf['creditNum']), "信用股东户数对比错误")
            my_assert(int(databasequery_resulf['gdzgs']) == int(api_resulf['shareholdingNum']), "总股数对比错误")
            my_assert(int(databasequery_resulf['jggdzgs']) == int(api_resulf['mechanismShareholdingNum']), "机构股数对比错误")
            my_assert(int(databasequery_resulf['grzgs']) == int(api_resulf['personalShareholdingNum']), "个人股数对比错误")
            my_assert(int(databasequery_resulf['ltgdzgs']) == int(api_resulf['circulationShareholdingNum']), "流通股数对比错误")
            my_assert(int(databasequery_resulf['xygdzgs']) == int(api_resulf['creditNumShareholdingNum']), "信用股数对比错误")
            print(str(param[0]) + "对比完成")


if __name__ == '__main__':
    d = DataStatisticsAssert(774, [])
    d.assert_run()
