import json
import requests


def IRM_login(accountPassword):
    host = "https://testserver.comein.cn/comein/irmcenter"
    payload = json.dumps({
        "login": accountPassword[0],
        "password": accountPassword[1]
    })
    headers = {
        'mod': 'user',
        'app': 'irm',
        'act': 'login',
        'Content-Type': 'application/json'
    }
    res = requests.post(host, payload, headers=headers)
    token = res.json()["data"]["token"]
    uuid = res.json()["data"]["uuid"]
    return token, uuid
