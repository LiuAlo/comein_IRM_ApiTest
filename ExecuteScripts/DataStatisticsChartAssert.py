from DatabaseQuery.KeyDataOverview.DataOverviewSinglePeriod import DataOverviewSinglePeriod
from api_requests.KeyDataOverviewApi.Api_SharesContrast import Api_SharesContrast
from common.my_assert import my_assert


class DataStatisticsChartAssert(object):

    def __init__(self, company_id, accountPassword):
        self.company_id = company_id
        self.accountPassword = accountPassword

    def run(self):
        api_resulf = Api_SharesContrast(self.accountPassword)

        for d in api_resulf:
            record_date = d['currentTime']
            data_query = DataOverviewSinglePeriod(self.company_id, record_date).overview_of_roster_data()

            my_assert(int(data_query["gdzs"]) == int(d['shareholderNum']), "总户数对比错误")
            my_assert(int(data_query["jggdzs"]) == int(d['mechanismNum']), "机构户数对比错误")
            my_assert(int(data_query["grgdzs"]) == int(d['personalNum']), "个人户数对比错误")
            my_assert(int(data_query["xygdzs"]) == int(d['creditNum']), "信用股东户数对比错误")
            my_assert(int(data_query["gdzgs"]) == int(d['shareholdingNum']), "总股数对比错误")
            my_assert(int(data_query["jggdzgs"]) == int(d['mechanismShareholdingNum']), "机构股数对比错误")
            my_assert(int(data_query["jggdzgs_proportion"]) == int(d['mechanismShareholdingRatio']), "机构比例对比错误")
            my_assert(int(data_query["grzgs"]) == int(d['personalShareholdingNum']), "个人股数对比错误")
            my_assert(int(data_query["grzgs_proportion"]) == int(d['personalShareholdingRatio']), "个人比例对比错误")
            my_assert(int(data_query["xygdzgs"]) == int(d['creditNumShareholdingNum']), "信用股数对比错误")
            my_assert(int(data_query["xygdzgs_proportion"]) == int(d['creditNumShareholdingRatio']), "信用比例对比错误")
            my_assert(int(data_query["ltgdzs"]) == int(d['circulationNum']), "流通户数对比错误")
            my_assert(int(data_query["ltgdzgs"]) == int(d['circulationShareholdingNum']), "流通股数对比错误")
            my_assert(int(data_query["ltgdzgs_proportion"]) == int(d['circulationShareholdingRatio']), "流通比例对比错误")

            print("{}, 对比完成".format(str(record_date)))


if __name__ == '__main__':
    d = DataStatisticsChartAssert(774, [])
    d.run()
