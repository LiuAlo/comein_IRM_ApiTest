import json
from common.Request_api import Request_api
from common.timeFormat import timeFormat


def Api_DataStatistics(currentTime, contrastTime, accountPassword):
    """
    数据统计: 户数统计、股数统计
    持股变动统计：户数统计、股数统计
    :param currentTime:
    :param contrastTime:
    :param accountPassword:
    :return:
    """
    url = "https://testserver.comein.cn/comein/irmcenter/irm/shareholder/home/data"
    currentTime = timeFormat(currentTime)
    contrastTime = timeFormat(contrastTime)
    body = json.dumps(
        {
            "currentTime": currentTime,
            "contrastTime": contrastTime
        }
    )
    result = Request_api(url=url, data=body, accountPassword=accountPassword)
    return result['data']


if __name__ == '__main__':
    list_data = Api_DataStatistics(1701100800000, 1690473600000, [])
    print(list_data)
