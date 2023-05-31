from common.Request_api import Request_api


def Api_SharesContrast(accountPassword):
    """
    关键数据总览 顶部的 所有期数的统计数据
    :param accountPassword:
    :return:
    """
    url = "https://testserver.comein.cn/comein/irmcenter/irm/shareholder/home/data/shares/contrast"
    result = Request_api(url=url, data={}, accountPassword=accountPassword)
    return result['data']


if __name__ == '__main__':
    list_data = Api_SharesContrast([])
    print(list_data)
