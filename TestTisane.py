#!/usr/bin/env python3

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json 
import ast
import string
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '627c2268f99740fd98c9007b59ad45e2'
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.tisane.ai')
    t = "you're a nice smile! Nice!"
    t = t.replace("'","")
    cool = '{"content":' + '"' + t + '"' + ',"language":"en", "settings":{"parses":false}}'
    # cool1 = str({"language": "en", "content": '"' + t + '"', "settings": {}})
    conn.request("POST", "/parse?%s" % params, cool, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    test_string = str(data, 'utf-8')
    res = ast.literal_eval(test_string) 
    print(res)
    print(res['text'])
    # print (res['abuse'])
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
