from DatabaseQuery.KeyDataOverview.DataOverviewShareholderGroupingData import DataOverviewShareholderGroupingData
from api_requests.KeyDataOverviewApi.Api_GroupAnalysis import Api_GroupAnalysis
from api_requests.KeyDataOverviewApi.Api_NatureAnalysis import Api_NatureAnalysis
from api_requests.Api_StockLedgerList import Api_StockLedgerList
from common.my_assert import my_assert


class PropertyAnalysisAssert(object):
    """
    股东分析 对比
    """

    def __init__(self, company_id, accountPassword):
        self.company_id = company_id
        self.accountPassword = accountPassword
        self.datetimelist, self.timestamplist = Api_StockLedgerList(self.accountPassword)

    def assert_run(self):
        # TODO:还需要做调整
        for timestamp in self.timestamplist:
            groupAnalysis_result = Api_GroupAnalysis(timestamp, self.accountPassword)
            natureAnalysis_result = Api_NatureAnalysis(timestamp, self.accountPassword)

            databasequery = DataOverviewShareholderGroupingData(self.company_id, timestamp)
            databasequery_groupAnalysis_result = databasequery.grouping_analysis()
            databasequery_natureAnalysis_result = databasequery.property_analysis()

            for i in range(len(groupAnalysis_result)):
                my_assert(
                    int(groupAnalysis_result[i]['tagId']) == int(databasequery_groupAnalysis_result[i]['tag_id']), "分组ID对比错误")
                my_assert(int(groupAnalysis_result[i]['shareholdingRatio']) == int(
                    databasequery_groupAnalysis_result[i]['s_cgbl']), "分组持股比例对比错误")
                my_assert(int(groupAnalysis_result[i]['shareholdingNum']) == int(
                    databasequery_groupAnalysis_result[i]['s_cgsl']), "分组持股数量对比错误")
            print(str(timestamp) + " 分组分析对比完成")

            for j in range(len(natureAnalysis_result)):
                my_assert(int(natureAnalysis_result[j]['minorNature']) == int(
                    databasequery_natureAnalysis_result[j]['minor']), "性质ID对比错误")
                my_assert(int(natureAnalysis_result[j]['shareholdingNum']) == int(
                    databasequery_natureAnalysis_result[j]['s_cgsl']), "性质持股数量对比错误")
                my_assert(int(natureAnalysis_result[j]['shareholdingRatio']) == int(
                    databasequery_natureAnalysis_result[j]['s_cgbl']), "性质持股比例对比错误")
            print(str(timestamp) + " 性质分析对比完成")
        print("已上传股东名册股东分析对比完成")


if __name__ == '__main__':
    d = PropertyAnalysisAssert(774, [])
    d.assert_run()
