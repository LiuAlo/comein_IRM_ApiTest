from common.Request_api import Request_api


def Api_AnalysisNatureContrast(accountPassword):
    """
    股东变化--性质变化
    :param accountPassword:
    :return:
    """
    url = "https://testserver.comein.cn/comein/irmcenter/irm/shareholder/home/analysis/nature/contrast"
    result = Request_api(url=url, data={}, accountPassword=accountPassword)
    return result['data']


if __name__ == '__main__':
    list_data = Api_AnalysisNatureContrast([])
    print(list_data)
