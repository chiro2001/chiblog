import requests
import json

api_home = "http://127.0.0.1:8192/api/v1/"


def test_main():
    # 注册账户
    resp = requests.post(api_home + 'user', headers={
        'Content-Type': 'application/json'
    }, data=json.dumps({
        'username': 'lance',
        'password': '1352040930lxr'
    })).json()
    print(resp)
    if 'uid' not in resp['data']:
        uid = 1
    else:
        uid = resp['data']['uid']
    resp = requests.post(api_home + 'session', headers={
        'Content-Type': 'application/json'
    }, data=json.dumps({
        'username': 'lance',
        'password': '1352040930lxr'
    })).json()
    print(resp)
    ac, rf = resp['data']['access_token'], resp['data']['refresh_token']
    print(ac, rf)
    # 发布文章
    cid = 1
    for _ in range(3):
        resp = requests.post(api_home + 'content', headers={
            'Content-Type': 'application/json',
            'Authorization': ac
        }, data=json.dumps({
            'title': "TestTitle",
            'content': "This is Test Content!",
            'password': 'passwd'
        })).json()
        print(resp)
        cid = resp['data']['cid']
    # 检索文章
    resp = requests.get(api_home + 'content', headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        "limit": 1,
        'offset': 3
    })).json()
    print(resp)
    resp = requests.get(api_home + f'content/{cid}', headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        "password": 'passwd'
    })).json()
    print(resp)


if __name__ == '__main__':
    test_main()
