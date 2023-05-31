import json
from common.Request_api import Request_api
from common.timeFormat import timeFormat


def Api_ContrastGroupAnalysis(currentTime, accountPassword):
    """
    股东变化：分组变化
    :param currentTime:
    :param accountPassword:
    :return:
    """
    url = "https://testserver.comein.cn/comein/irmcenter/irm/shareholder/home/analysis/tag/contrast"
    currentTime = timeFormat(currentTime)
    body = json.dumps(
        {
            "currentTime": currentTime
        }
    )
    result = Request_api(url=url, data=body, accountPassword=accountPassword)
    return result['data']


if __name__ == '__main__':
    list_data = Api_ContrastGroupAnalysis(1690473600000, [])
    print(list_data)
