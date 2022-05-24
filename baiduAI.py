# coding=utf-8

import sys
import json
import base64
import time


# make it work in both python2 both python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# skip https auth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
API_KEY = 'tb0xGjYWPg4cKF6lgUaWbUqA'
SECRET_KEY = 'n9SetxUWcAy1WsMxunQqhA7Anz22ZoeC'
COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

"""
    get token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()
"""
    call remote http server
"""
def make_request(url, comment):
    response = request(url, json.dumps(
    {
        "text": comment,
    }))
    data = json.loads(response)
    # print(data)
    correct_query = data['item']['correct_query']
    # print(data['item']['correct_query'])
    # error = data["item"]['vec_fragment'][0]['ori_frag']
    # willcorrect = data["item"]['vec_fragment'][0]['correct_frag']
    # correct_query = data["item"]['correct_query']
    # text = data["text"]
    # print("错误短语为：" + str(error))
    # print("修改建议为：" + str(willcorrect))
    # print("原语句为：" + str(text))
    # print("最后修改为：" + str(correct_query))
    # 防止qps超限
    time.sleep(0.5)
    return correct_query

"""
    call remote http server
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

def baiducorrect(comment1):
    # get access token
    token = fetch_token()
    # concat url
    url = COMMENT_TAG_URL + "?charset=UTF-8&access_token=" + token
    correct_query = make_request(url, comment1)
    # print(correct_query)
    return correct_query



