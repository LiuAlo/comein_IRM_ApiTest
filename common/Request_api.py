import requests
from common.IRM_login import IRM_login


def Request_api(url, data, accountPassword):
    accountPassword = list(accountPassword)
    token, uuid = IRM_login(accountPassword)

    headers = {"uid": uuid, "token": token}
    res = requests.post(url=url, headers=headers, data=data)
    return res.json()
