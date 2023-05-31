import json
from common.Request_api import Request_api
from common.timeFormat import timeFormat


def Api_NatureAnalysis(currentTime, accountPassword):
    """
    股东分析: 性质分析
    :param currentTime:
    :param accountPassword:
    :return:
    """
    url = "https://testserver.comein.cn/comein/irmcenter/irm/shareholder/home/analysis/nature"
    currentTime = timeFormat(currentTime)
    body = json.dumps(
        {
            "currentTime": currentTime
        }
    )
    result = Request_api(url=url, data=body, accountPassword=accountPassword)
    return result['data']


if __name__ == '__main__':
    list_data = Api_NatureAnalysis(1701100800000, [])
    print(list_data)
