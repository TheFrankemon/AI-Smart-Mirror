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
from knowledge import Knowledge
from vision import Vision
from firebase import Firebase

user_name = "Franco"
launch_phrase = "hola"
use_launch_phrase = True
debugger_enabled = True
camera = 0
conf = None

class Bot(object):
	def __init__(self):
		global conf
		with open('config.json') as data_file:
			conf = json.load(data_file)
		self.nlg = NLG()
		self.speech = Speech(launch_phrase=launch_phrase, debugger_enabled=debugger_enabled)
		self.knowledge = Knowledge()
		self.vision = Vision(camera=camera)
		#self.firebase = Firebase()

	def start(self):
		"""
		Main loop. Waits for the launch phrase, then decides an action.
		:return:
		"""
		while True:
			requests.get("http://localhost:8888/clear")
			if self.vision.recognize_face():
				print("Found face")
				self.__info_action(launch_phrase)
				if use_launch_phrase:
					recognizer, audio = self.speech.listen_for_audio()
					if self.speech.is_call_to_action(recognizer, audio, str(conf["wit_ai_token"])):
						self.__acknowledge_action()
						self.decide_action()
				else:
					self.decide_action()

	def decide_action(self):
		"""
		Recursively decides an action based on the intent.
		:return:
		"""
		recognizer, audio = self.speech.listen_for_audio()

		#Recognize audio with Google Speech Recognition
		#speech = self.speech.google_speech_recognition(recognizer, audio)

		#Recognize audio with Wit Speech API
		speech = self.speech.wit_speech_recognition(recognizer, audio, str(conf["wit_ai_token"]))

		if speech is not None:
			try:
				#speech = "torta UPB" ###Hardcoded Speech
				print('Requesting WIT.AI [' + speech + ']')
				r = requests.get('https://api.wit.ai/message?v=20170403&q=%s' % speech, headers={'Authorization': str(conf["wit_ai_token"])})
				print('Text ' + r.text)
				#print(r.headers['authorization'])
				json_resp = json.loads(r.text)
				entities = None
				intent = None
				if 'entities' in json_resp and 'Intent' in json_resp['entities']:
					entities = json_resp['entities']
					intent = json_resp['entities']['Intent'][0]["value"]

				print(intent)
				if intent == 'chiefs':     #CUSTOM
					self.__chiefs_action(entities)
				elif intent == 'rooms':      #CUSTOM
					self.__rooms_action(entities)
				elif intent == 'buses':      #CUSTOM
					self.__text_action(self.nlg.buses())
				elif intent == 'schedules':  #CUSTOM
					self.__schedules_action(entities)
				elif intent == 'career_semesterclasses':  #CUSTOM
					self.__career_sc_action(entities)
				elif intent == 'maps':
					self.__maps_action(entities)
				elif intent == 'appreciation':
					self.__text_action(self.nlg.appreciation())
					return
				else: # No recognized intent
					self.__text_action("Perdón, aún estoy en kinder.")

			except Exception as e:
				print("Failed wit!")
				print(e)
				traceback.print_exc()
				self.__text_action("Perdón, no te entendí")
				return

			self.decide_action()

	# CUSTOM
	def __info_action(self, phrase):
		info = self.nlg.info(phrase)

		if info is not None:
			self.__text_action(info)
		else:
			self.__text_action("Me raye")

	def __acknowledge_action(self):
		self.__text_action(self.nlg.acknowledge())

	# CUSTOM
	def __chiefs_action(self, nlu_entities=None):

		chief = None

		if nlu_entities is not None:
			if 'Career_Type' in nlu_entities:
				career_type = nlu_entities['Career_Type'][0]['value']
				print(career_type)
				chief = self.nlg.chiefs(career_type)

		if chief is not None:
			self.__text_action(chief)
		else:
			self.__text_action("No encuentro al jefe de carrera")

	# CUSTOM
	def __rooms_action(self, nlu_entities=None):
		if nlu_entities is not None:
			if 'Room_Type' in nlu_entities:
				location = nlu_entities['Room_Type'][0]['value']
				print(location)

		if location is not None:
			room_url = self.knowledge.get_UPBroute_url(location)
			body = {'url': room_url}
			requests.post("http://localhost:8888/image", data=json.dumps(body))
			
			room_action = "%s se encuentra aqui." % location
			self.speech.synthesize_text(room_action)
		else:
			self.__text_action("Perdón, no encontré el salon que buscabas")

	# CUSTOM
	def __schedules_action(self, nlu_entities=None):
		if nlu_entities is not None:
			if 'Professor_Names' in nlu_entities:
				prof = nlu_entities['Professor_Names'][0]['value']
				print(prof)

		if prof is not None:
			prof_url = self.knowledge.get_schedule_url(prof)
			body = {'url': prof_url}
			requests.post("http://localhost:8888/image", data=json.dumps(body))
			
			prof_action = "%s tiene los siguientes horarios. Podras tambien consultar sobre las ubicaciones." % prof
			self.speech.synthesize_text(prof_action)
		else:
			self.__text_action("Perdón, no encontré a la persona que buscabas")

	# CUSTOM
	def __career_sc_action(self, nlu_entities=None):
		if nlu_entities is not None:
			if 'Career_Type' in nlu_entities:
				career = nlu_entities['Career_Type'][0]['value']
				print(career)

		if career is not None:
			career_url = self.knowledge.get_sc_url(career)
			body = {'url': career_url}
			requests.post("http://localhost:8888/image", data=json.dumps(body))
			
			career_action = "Ten el detalle de Semestres y Materias de %s." % career
			self.speech.synthesize_text(career_action)
		else:
			self.__text_action("Perdón, no encontré la carrera que buscas.")

	def __maps_action(self, nlu_entities=None):
		location = None
		map_type = None
		if nlu_entities is not None:
			if 'location' in nlu_entities:
				location = nlu_entities['location'][0]["value"]
			if "Map_Type" in nlu_entities:
				map_type = nlu_entities['Map_Type'][0]["value"]

		if location is not None:
			maps_url = self.knowledge.get_map_url(location, map_type)
			maps_action = "Ten un mapa de %s." % location
			body = {'url': maps_url}
			requests.post("http://localhost:8888/image", data=json.dumps(body))
			self.speech.synthesize_text(maps_action)
		else:
			self.__text_action("Perdón, no encontré el lugar que buscabas")

	def __text_action(self, text=None):
		if text is not None:
			requests.get("http://localhost:8888/statement?text=%s" % text)
			self.speech.synthesize_text(text)

if __name__ == "__main__":
	bot = Bot()
	bot.start()
