from DatabaseQuery.KeyDataOverview.DataOverviewChangeStatistics import DataOverviewChangeStatistics
from api_requests.KeyDataOverviewApi.Api_DataStatistics import Api_DataStatistics
from common.PeriodCombination import PeriodCombination
from api_requests.Api_StockLedgerList import Api_StockLedgerList
from common.my_assert import my_assert


class DataStatisticsAssert(object):
    """
    持股变动统计 对比
    """

    def __init__(self, company_id, accountPassword):
        self.company_id = company_id
        self.accountPassword = accountPassword
        self.params = self.periods_params()

    def periods_params(self):
        datetime, timestamp = Api_StockLedgerList(self.accountPassword)
        return PeriodCombination(timestamp)

    def assert_run(self):
        # 只做最新的
        param = self.params[0]
        api_resulf = Api_DataStatistics(param[0], param[1], self.accountPassword)
        databasequery_resulf = DataOverviewChangeStatistics(self.company_id, param[0],
                                                            param[1]).OverviewHoldingsNumber()
        my_assert(int(databasequery_resulf['IncreasedHoldingsNumber']) == int(api_resulf['upCount']),
                  "增持户数对比错误")
        my_assert(int(databasequery_resulf['ReduceHoldingsNumber']) == int(api_resulf['downCount']), "减持户数对比错误")
        my_assert(int(databasequery_resulf['NewlyAddedHoldingsNumber']) == int(api_resulf['inCount']),
                  "新进户数对比错误")
        my_assert(int(databasequery_resulf['ExitHoldingsNumber']) == int(api_resulf['outCount']), "退出户数对比错误")
        my_assert(int(databasequery_resulf['maintainHoldingsNumber']) == int(api_resulf['keepCount']),
                  "维持户数对比错误")
        my_assert(int(databasequery_resulf['IncreasedSharesNumber']) == int(api_resulf['upNum']), "增持股数对比错误")
        my_assert(int(databasequery_resulf['IncreasedSharesRatio']) == int(api_resulf['upRatio']), "增持比例对比错误")
        my_assert(int(databasequery_resulf['ReduceSharesNumber']) == int(api_resulf['downNum']), "减持股数对比错误")
        my_assert(int(databasequery_resulf['ReduceSharesRatio']) == int(api_resulf['downRatio']), "减持比例对比错误")
        my_assert(int(databasequery_resulf['NewlyAddedSharesNumber']) == int(api_resulf['inNum']), "新进股数对比错误")
        my_assert(int(databasequery_resulf['NewlyAddedSharesRatio']) == int(api_resulf['inRatio']), "新进比例对比错误")
        my_assert(int(databasequery_resulf['ExitSharesNumber']) == int(api_resulf['outNum']), "退出股数对比错误")
        my_assert(int(databasequery_resulf['ExitSharesRatio']) == int(api_resulf['outRatio']), "退出比例对比错误")

        print("{}-{},对比完成".format(str(param[0]), str(param[1])))


if __name__ == '__main__':
    d = DataStatisticsAssert(774, [])
    d.assert_run()
