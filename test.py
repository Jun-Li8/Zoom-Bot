from http import client

from oauthlib import oauth2
from oauthlib.oauth2.rfc6749 import grant_types
from zoom.get_transcript import Transcript
from zoom.new_server_py import start_server
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

# client_id = '1KaFjUkRTiYql5TLITaQg'
# client_secret = 'TD6jX17FnhOK3hugjYFjT54c5cXcPzJ7'

# client = BackendApplicationClient(client_id=client_id)
# oauth = OAuth2Session(client=client)
# token = oauth.fetch_token(token_url='https://zoom.us/oauth/token', grant_type='authorization_code', code='euWsr6JeLT_7XXbaVrzT5euLxvRs5JoXw',redirect_uri='http://localhost:8080')

# r = requests.get('https://zoom.us/oauth/authorize?client_id=1KaFjUkRTiYql5TLITaQg&response_type=code&redirect_uri=http://localhost:8080/')
# print(r.text)


#go to https://zoom.us/oauth/authorize?client_id=1KaFjUkRTiYql5TLITaQg&response_type=code&redirect_uri=http://localhost:8080/ 
#get the code in code='' from URL
token = Transcript(meeting_id=97807885687, client_key='1KaFjUkRTiYql5TLITaQg', client_secret='TD6jX17FnhOK3hugjYFjT54c5cXcPzJ7', code='z20RKdpFEl_7XXbaVrzT5euLxvRs5JoXw')
trans = token.GetTranscript()
print(trans)