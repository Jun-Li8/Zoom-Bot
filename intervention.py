# You need to install pyaudio to run this example
# pip install pyaudio

# When using a microphone, the AudioSource `input` parameter would be
# initialised as a queue. The pyaudio stream would be continuosly adding
# recordings to the queue, and the websocket client would be sending the
# recordings to the speech to text service

import pyaudio
import joblib
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3
import http.client, urllib.request, urllib.parse, urllib.error, base64
from email_setup import sent_email
from mute import controlKeyboard
from get_window import warn
import ast
from threading import Timer

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# USER = Jun
###############################################
#### Initalize queue to store the recordings ##
###############################################
CHUNK = 1024
# Note: It will discard if the websocket client can't consumme fast enough
# So, increase the max size as per your choice
BUF_MAX_SIZE = CHUNK * 10
# Buffer to store audio
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

# Create an instance of AudioSource
audio_source = AudioSource(q, True, True)

###############################################
#### Prepare Speech to Text Service ########
###############################################

# initialize speech to text service
authenticator = IAMAuthenticator('437LbRpZ4UVpoQ1BqsTmGKgOW4KIEn6lcGCzCA5jXkUH')
authenticator1 = IAMAuthenticator('Rwqm8kJI4m23ErDDUETNmrfLIQYQk1mEZQdk3bJ2yGgP')
speech_to_text = SpeechToTextV1(authenticator=authenticator)
ta = ToneAnalyzerV3(version='2017-09-21', authenticator=authenticator1)
ta.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/da1b4bd0-109f-496a-a543-6b734fcca3b7')
speech_to_text.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/a4e313e3-3bc3-40a2-8f1e-7eb1d478d62a')

model = joblib.load('bully_model.sav')

def get_data(text):
    t = '{"content":' + '"' + text + '"' + ',"language":"en", "settings":{"parses":false}}'
    conn.request("POST", "/parse?%s" % params, t, headers)
    response = conn.getresponse()
    data = response.read()
    test_string = str(data, 'utf-8')
    res = ast.literal_eval(test_string)
    data = [None, None, None]
    if 'abuse' in res: 
        data[0] = res['abuse'][0]['type']
        data[1] = res['abuse'][0]['severity']
    try:
        res1 = ta.tone_chat([{'text': text}]).get_result()
        data[2] = res1['utterances_tone'][0]['tones'][0]['tone_id']
    except:
        pass
    return data

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '627c2268f99740fd98c9007b59ad45e2'
}
params = urllib.parse.urlencode({
})

conn = http.client.HTTPSConnection('api.tisane.ai')

# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.speech = []
        self.offense = {'personal_attack': 0, 'bigotry':0, 'profanity':0, 'sexual_advances':0, 'criminal_activity':0, 'external_contact':0, 'adult_only':0, 'mental_issues':0 , 'spam':0, 'generic':0}
        self.total = 0
        self.bully_count = 0

    def on_transcription(self, transcript):
        t = transcript[0]['transcript']
        print(t)
        data = get_data(t)
        if data[1] != None:
            print('Severity: ' + data[1])
            print('Offense: ' + data[0])
            self.offense[data[0]] += 1
            if  data[1] != 'low':
                print('BULLY DETECTED')
            if 2 in self.offense.values():
                w = Timer(5.0,warn, (data[0],"lol"))
                w.start()
                self.offense[data[0]] = 0
    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        pass
        # print(hypothesis)

    def on_data(self, data):
        pass
        # print(data)

    def on_close(self):
        # sorted_dict = sorted(self.offense.items(), key=lambda x: x[1], reverse=True)
        # email_data = {'speech': self.speech, 'count': self.bully_count, 'offenses': sorted_dict[0:3], 'email':'convoztesting@gmail.com'}
        # print(email_data)
        # sent_email(email_data)
        print("Connection closed")

# this function will initiate the recognize service and pass in the AudioSource
def recognize_using_weboscket(*args):
    mycallback = MyRecognizeCallback()
    speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mycallback,
                                             interim_results=True,profanity_filter=False)

###############################################
#### Prepare the for recording using Pyaudio ##
###############################################

# Variables for recording the speech
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# define callback for pyaudio to store the recording in queue
def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass # discard
    return (None, pyaudio.paContinue)

# instantiate pyaudio
audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
    dev = audio.get_device_info_by_index(i)
    if(dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
        dev_index = dev['index']
        # print('dev_index:',dev_index)

# open stream using callback
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=pyaudio_callback,
    start=False,
    input_device_index = dev_index
    )

#########################################################################
#### Start the recording and start service to recognize the stream ######
#########################################################################

print("Enter CTRL+C to end recording...")
stream.start_stream()
# start_server(8080)

try:
    recognize_thread = Thread(target=recognize_using_weboscket, args=())
    recognize_thread.start()

    while True:
        pass
except KeyboardInterrupt:
    # stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_source.completed_recording()