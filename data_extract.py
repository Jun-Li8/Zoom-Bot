import webvtt
from collections import defaultdict 

import http.client, urllib.request, urllib.parse, urllib.error, base64
import ast

from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import json
import time
apikey = 'insert key here'
url = 'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/da1b4bd0-109f-496a-a543-6b734fcca3b7'

authenticator = IAMAuthenticator(apikey)
ta = ToneAnalyzerV3(version='2017-09-21', authenticator=authenticator)
ta.set_service_url(url)

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'insert key here'
}
params = urllib.parse.urlencode({
})
conn = http.client.HTTPSConnection('api.tisane.ai')


def time_to_int(timestr):
    ftr = [3600,60,1]
    return sum([a*b for a,b in zip(ftr, map(float,timestr.split(':')))])

def get_data(text):
    t = '{"content":' + '"' + text + '"' + ',"language":"en", "settings":{"parses":false}}'
    conn.request("POST", "/parse?%s" % params, t, headers)
    response = conn.getresponse()
    data = response.read()
    test_string = str(data, 'utf-8')
    res = ast.literal_eval(test_string)
    data = [None, None, None]
    try: 
        data[0] = res['abuse'][0]['type']
        data[1] = res['abuse'][0]['severity']
    except:
        pass
    try:
        res = ta.tone_chat([{'text': text}]).get_result()
        data[2] = res['utterances_tone'][0]['tones'][0]['tone_id']
    except:
        pass
    return data
# person = {
#     'total': {'duration': 0, 'count':0},
#     'speech':{
#     }
# }
everyone = defaultdict(lambda:{
    'total': {'duration': 0, 'count':0},
    'speech':{
    }
})
total = 0
start = True
for caption in webvtt.read('97807885687_audio_transcript.vtt'):
    text= caption.text.split(':')
    data = get_data(text[1])
    if data[1] != 'low' and data[1] != None:
        everyone[text[0]]['total']['count'] += 1
        total += 1
        start = True
    if total%10 == 0 and start == False:
        print('Wait a minute for API')
        time.sleep(65)
    duration = time_to_int(caption.end) - time_to_int(caption.start)
    everyone[text[0]]['total']['duration'] += duration
    everyone[text[0]]['speech'][text[1]] = data
everyone = dict(everyone)
report_data = open("report_data.json","w")
json.dump(everyone,report_data)
print(everyone)
report_data.close()
