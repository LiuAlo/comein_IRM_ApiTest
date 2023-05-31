import json
from common.Request_api import Request_api
from common.timeFormat import timeFormat


def Api_TopTenShareholdings(currentTime, contrastTime, top_type, accountPassword):
    """
    股东分析: 性质分析
    股东变化：分组变化
    :param currentTime:
    :param contrastTime:
    :param top_type: 0：全部股东，1：机构股东，2：产品维度，3：个人股东，4：基金经理
    :param accountPassword:
    :return:
    """
    url = "https://testserver.comein.cn/comein/irmcenter/irm/shareholder/home/top"
    currentTime = timeFormat(currentTime)
    contrastTime = timeFormat(contrastTime)
    body = json.dumps(
        {
            "currentTime": currentTime,
            "contrastTime": contrastTime,
            "type": top_type}
    )
    result = Request_api(url=url, data=body, accountPassword=accountPassword)
    return result['data']


if __name__ == '__main__':
    list_data = Api_TopTenShareholdings("1701100800000", "1700409600000", 0, [])
    print(list_data)
