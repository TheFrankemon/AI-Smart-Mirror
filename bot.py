# bot.py
# -*- coding: utf-8 -*-
# speechrecognition, pyaudio, brew install portaudio
import sys
import random
sys.path.append("./")

import requests
import datetime as dt
import dateutil.parser
import json
import traceback
import time
from nlg import NLG
from speech import Speech
from vision import Vision
from firebase import Firebase

# user_name = "Desconocido"
status_enabled = True
camera = 0
conf = None

class Bot(object):
	def __init__(self):
		global conf
		with open('config.json') as data_file:
			conf = json.load(data_file)
		self.nlg = NLG()
		self.speech = Speech(status_enabled=status_enabled)
		self.vision = Vision(camera=camera)
		self.firebase = Firebase()

	def start(self):
		"""
		Main loop.
		:return:
		"""
		while True:
			requests.get("http://localhost:8888/clear")
			requests.get("http://localhost:8888/keyboard?text=disable")
			if self.vision.recognize_face('c1'):
				print("Found face > Took Photo#1")
				self.__intro_action()
				requests.get("http://localhost:8888/keyboard?text=enable")

				flag = False
				sleeptime = 0
				while not flag:
					uname = requests.get('http://localhost:8888/uname').json()
					if uname[u'name'] == "":
						# must set a max of 20 secs, for example
						sleeptime += 1
						print('Total sleep time: ' + str(sleeptime))
						time.sleep(1)
					else:
						flag = not flag
						requests.get("http://localhost:8888/keyboard?text=disable")
						
				self.vision.recognize_face('c2')
				print("Found face > Took Photo#2")
				print("Username: " + uname[u'name'])
				#global user_name
				user_name = uname['name']
				requests.get('http://localhost:8888/unameclear')
				self.__acknowledge_action(user_name)
				timestamp = dt.datetime.today().strftime('%d/%m/%y %H:%M:%S')
				self.firebase.add(user_name,"img/c1.jpg","img/c2.jpg", timestamp)
				print("User saved succesfully on DB")
				self.__goodbye_action()
				time.sleep(5)

	# CUSTOM
	def __intro_action(self):
		intro_phrase = self.nlg.intro()

		if intro_phrase is None:
			self.__text_action("Me raye, contacta a un humano por favor")
		else:
			self.__text_action(intro_phrase)

	def __acknowledge_action(self, user_name=None):
		acknowledge_phrase = self.nlg.acknowledge(user_name)

		if user_name is not None:
			self.__text_action(acknowledge_phrase)
		else:
			self.__text_action("No pude guardar tu nombre, contacta a un humano por favor")

	def __goodbye_action(self):
		goodbye = self.nlg.goodbye()

		if goodbye is not None:
			self.__text_action(goodbye)
		else:
			self.__text_action("Me raye, contacta a un humano por favor")

	def __text_action(self, text=None):
		if text is not None:
			requests.get("http://localhost:8888/statement?text=%s" % text)
			self.speech.synthesize_text(text)

if __name__ == "__main__":
	bot = Bot()
	bot.start()
