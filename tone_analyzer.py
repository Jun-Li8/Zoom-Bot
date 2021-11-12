#Authenticate
apikey = 'insert key here'
url = 'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/da1b4bd0-109f-496a-a543-6b734fcca3b7'

from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(apikey)
ta = ToneAnalyzerV3(version='2017-09-21', authenticator=authenticator)
ta.set_service_url(url)
chat = [
    {'text': 'I am feeling amazing',
     'user': 'ABC'},
    {'text': 'You suck',
     'user': 'DEF'},
    {'text': 'You are dumb',
         'user': 'DEF'}
]
res = ta.tone_chat([{'text': 'I hate y0u.'}]).get_result()
print(res)
# output = ta.tone_chat(chat).get_result()
print(res['utterances_tone'][0]['tones'][0]['tone_id'])
# print(output)
