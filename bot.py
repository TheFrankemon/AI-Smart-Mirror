# bot.py
# -*- coding: utf-8 -*-
# speechrecognition, pyaudio, brew install portaudio
import sys
import random
sys.path.append("./")

import requests
import datetime
import dateutil.parser
import json
import traceback
import time
from nlg import NLG
from speech import Speech
from vision import Vision
from mongo import Mongo

user_name = "Temporal bro"
debugger_enabled = True
camera = 0
conf = None

class Bot(object):
    def __init__(self):
        global conf
        with open('config.json') as data_file:
	    conf = json.load(data_file)
        self.nlg = NLG(user_name=user_name)
	self.speech = Speech(debugger_enabled=debugger_enabled)
	self.vision = Vision(camera=camera)
        self.mongo = Mongo()

    def start(self):
	"""
	Main loop.
	:return:
	"""
	global user_name
        while True:
            requests.get("http://localhost:8888/clear")
            requests.get("http://localhost:8888/keyboard?text=disable")
            if self.vision.recognize_face('c1.png'):
		print "Found face > Took Photo#1"
                self.__intro_action()
                requests.get("http://localhost:8888/keyboard?text=enable")

                time.sleep(10)
                uname = requests.get('http://localhost:8888/uname').json()
                print uname
                requests.get("http://localhost:8888/keyboard?text=disable")

		self.vision.recognize_face('c2.png')
		print "Found face > Took Photo#2"
		#ans = None
                #while True:
                    #ans = requests.get("http://localhost:8888/keyboard?text=check")
                    #print ans
                    #if ans == "OK":
                    #    return
                    #else
                #########3 here it must enable keyboard, wait for ACCEPT
                print "Username: " + uname[u'name']
                user_name = uname['name']
		self.__user_name_action()
		self.mongo.add(user_name,
                    "/home/pi/AI-Smart-Mirror-Franco/img/c1.png",
                    "/home/pi/AI-Smart-Mirror-Franco/img/c2.png")
		print "User saved succesfully on DB"
		self.__acknowledge_action()
		####### it should return Y/N...Y > decide action...N > appreciation action
		self.decide_action()

    def decide_action(self):
	"""
	Recursively decides an action based on the intent.
	:return:
	"""
	recognizer, audio = self.speech.listen_for_audio()

	# received audio data, now we'll recognize it using Google Speech Recognition
	#speech = self.speech.google_speech_recognition(recognizer, audio)

	# received audio data, now we'll recognize it using Wit Speech API
        speech = self.speech.wit_speech_recognition(recognizer, audio, str(conf["tokens"]["wit_ai_token"]))

	if speech is not None:
            try:
                ## Uncomment for HARDCODED SPEECH ##
                #speech = "torta UPB"
                print 'Requesting WIT.AI [' + speech + ']'
                r = requests.get('https://api.wit.ai/message?v=20170403&q=%s' % speech, headers={'Authorization': str(conf["tokens"]["wit_ai_token"])})
                print 'Text ' + r.text
                #print r.headers['authorization']
                json_resp = json.loads(r.text)
                entities = None
                intent = None
		if 'entities' in json_resp and 'Intent' in json_resp['entities']:
                    entities = json_resp['entities']
                    intent = json_resp['entities']['Intent'][0]["value"]

                print intent
                if intent == 'appearance':
                    self.__appearance_action()
                elif intent == 'insult':
                    self.__insult_action()
                    return
                elif intent == 'appreciation':
                    self.__appreciation_action()
                    return
                else: # No recognized intent
                    self.__text_action("Perdón, aún estoy en kinder.")

            except Exception as e:
		print "Failed wit!"
		print(e)
		traceback.print_exc()
		self.__text_action("Perdón, no te entendí")
		return

            self.decide_action()

    # CUSTOM
    def __intro_action(self):
        intro = self.nlg.intro()

        if intro is not None:
            self.__text_action(intro)
        else:
            self.__text_action("Me raye, contacta a un humano por favor")

    def __user_name_action(self):
        if self.nlg.user_name is None:
            self.__text_action("I don't know your name. You can configure it in bot.py")

        self.__text_action("Hola " + user_name)

    def __acknowledge_action(self):
        acknowledge = self.nlg.acknowledge()

        if acknowledge is not None:
            self.__text_action(acknowledge)
        else:
            self.__text_action("Me raye, contacta a un humano por favor")

    def __appreciation_action(self):
        self.__text_action(self.nlg.appreciation())

    def __insult_action(self):
        self.__text_action(self.nlg.insult())

    def __appearance_action(self):
        requests.get("http://localhost:8888/face")

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8888/statement?text=%s" % text)
            self.speech.synthesize_text(text)

if __name__ == "__main__":
	bot = Bot()
	bot.start()
