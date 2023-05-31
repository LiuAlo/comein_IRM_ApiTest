from common.timeFormat import timeFormat
from common.Request_api import Request_api


def Api_StockLedgerList(accountPassword):
    """
    已上传的股东名册期数列表
    :param accountPassword:
    :return:
    """
    url = "https://testserver.comein.cn/comein/irmcenter/irm/shareholder/dates"
    result = Request_api(url=url, data={}, accountPassword=accountPassword)
    original_time_list = result['data']
    format_date_list = [timeFormat(i) for i in original_time_list]
    return format_date_list, original_time_list


if __name__ == '__main__':
    list_data = Api_StockLedgerList([])
    r, o = list_data
    for i in o:
        print(i)
    print(list_data)
