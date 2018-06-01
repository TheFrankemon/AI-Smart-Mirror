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

launch_phrase = "hola"
use_launch_phrase = True
debugger_enabled = True
camera = 0
conf = None

class Bot(object):
	def __init__(self):
		global conf
		self.debugger_enabled = debugger_enabled
		with open('config.json') as data_file:
			conf = json.load(data_file)
		self.nlg = NLG()
		self.speech = Speech(launch_phrase=launch_phrase, debugger_enabled=debugger_enabled)
		self.vision = Vision(camera=camera)
		self.firebase = Firebase()

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
					self.__debugger_recognition(enable=True)
					if self.speech.is_call_to_action(recognizer, audio, str(conf["tokens"]["wit_ai_token"])):
						self.__debugger_recognition(enable=False)
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
		self.__debugger_recognition(enable=True)
		speech = self.speech.wit_speech_recognition(recognizer, audio, str(conf["tokens"]["wit_ai_token"]))

		if speech is None:
			self.__debugger_recognition(enable=False)
			self.__text_action("Perdón, no te oí bien. Déjame reconocerte de nuevo...")
		else:
			entities = None
			intent = None
			try:
				#speech = "something" ##Hardcoded Speech
				print('Requesting WIT.AI: ' + speech)
				r = requests.get('https://api.wit.ai/message?v=20180301&q=%s' % speech, headers={'Authorization': str(conf["tokens"]["wit_ai_token"])})
				self.__debugger_recognition(enable=False)
				print('Recognized text: ' + r.text)
				json_resp = json.loads(r.text)
				if 'entities' in json_resp and 'Intent' in json_resp['entities']:
					entities = json_resp['entities']
					intent = json_resp['entities']['Intent'][0]["value"]

			except Exception as e:
				print("Failed wit! " + e)
				traceback.print_exc()
				self.__text_action("Perdón, algo anda mal con el servicio de reconocimiento")
				return

			print(intent)
			#CUSTOM>
			if intent == 'hods':
				self.__hods_action(entities)
			elif intent == 'upblocations':
				self.__upblocations_action(entities)
			elif intent == 'buses':
				self.__text_action(self.nlg.buses())
			elif intent == 'career_semesterclasses':
				self.__career_sc_action(entities)
			elif intent == 'courses':
				self.__courses_action(entities)
			#<CUSTOM
			elif intent == 'maps':
				self.__maps_action(entities)
			elif intent == 'appreciation':
				self.__text_action(self.nlg.appreciation())
				return
			else: # No recognized intent
				self.__text_action("Perdón, no entendí el asunto")

			self.decide_action()

	# CUSTOM
	def __info_action(self, phrase):
		info = self.nlg.info(phrase)
		self.__text_action(info)

	def __acknowledge_action(self):
		self.__text_action(self.nlg.acknowledge())

	# CUSTOM
	def __hods_action(self, nlu_entities=None):
		career_name = None		
		if nlu_entities is not None and 'Career_Names' in nlu_entities:
			career_name = nlu_entities['Career_Names'][0]['value']
			print(career_name)
		
		if career_name is not None:
			career_data = self.firebase.get_DB_career(career_name)
			if career_data is None:
				self.__text_action("Perdón, no encuentro al jefe de carrera")
				return
			hod = career_data['HOD_name']
			hod_hours = career_data['HOD_available_hours']
			self.__text_action(("El jefe de carrera de {} es {}, sus horarios de atención son de {}").format(career_name, hod, hod_hours))
		else:
			self.__text_action("Perdón, no encuentro al jefe de carrera")

	# CUSTOM
	def __upblocations_action(self, nlu_entities=None):
		upblocation_name = None		
		if nlu_entities is not None and 'UPB_Location_Names' in nlu_entities:
			upblocation_name = nlu_entities['UPB_Location_Names'][0]['value']
			print(upblocation_name)

		if upblocation_name is not None:
			upblocation_url = self.firebase.get_DB_upblocationurl(upblocation_name)
			if upblocation_url is None:
				self.__text_action("Perdón, no encontré una ruta para la ubicación")
				return
			body = {'url': upblocation_url}
			requests.post("http://localhost:8888/image", data=json.dumps(body))
			
			self.speech.synthesize_text(("{} se encuentra aqui.").format(upblocation_name))
		else:
			self.__text_action("Perdón, no encontré la ubicación que buscabas")

	# CUSTOM
	def __career_sc_action(self, nlu_entities=None):
		career_name = None
		if nlu_entities is not None and 'Career_Names' in nlu_entities:
			career_name = nlu_entities['Career_Names'][0]['value']
			print(career_name)
		
		if career_name is not None:
			career_data = self.firebase.get_DB_career(career_name)
			if career_data is None:
				self.__text_action("Perdón, no encontré la carrera que buscas")
				return
			sc_url = career_data['cs_url']
			body = {'url': sc_url}
			requests.post("http://localhost:8888/image", data=json.dumps(body))
			
			self.speech.synthesize_text(("Ten el detalle de Semestres y Materias de {}.").format(career_name))
		else:
			self.__text_action("Perdón, no encontré la carrera que buscas")

	# CUSTOM
	def __courses_action(self, nlu_entities=None):
		course = None
		professor = None
		if nlu_entities is not None:
			if 'Course_Names' in nlu_entities:
				course = nlu_entities['Course_Names'][0]['value']
				print(course)
			if 'Professor_Names' in nlu_entities:
				professor = nlu_entities['Professor_Names'][0]['value']
				print(professor)

		if course is not None:
			if professor is None:
				parallels = self.firebase.get_DB_course_parallels(course)
				if parallels is None:
					self.__text_action("Perdón, no encontré la materia que buscas")
					return
				if len(parallels) == 1:
					self.__text_action(("Existe 1 paralelo de {}...").format(course))
				else:
					self.__text_action(("Existen {} paralelos de {}...").format(len(parallels), course))

				for parallel in parallels:
					professor = parallel['professor']
					if professor == "":
						professor = "Docente por definir"
					classroom = parallel['classroom']
					if classroom == "":
						classroom = "un aula por definir"
					period = parallel['period']
					self.__text_action(("{}. Las clases son en horario {} en {}").format(professor, period, classroom))
			else:
				parallels = self.firebase.get_DB_course_parallels(course, professor)
				if parallels is None:
					self.__text_action("Perdón, no encontré la materia que buscas")
					return
				if len(parallels) == 1:
					self.__text_action(("Existe 1 paralelo de {} con {}...").format(course, professor))
				else:
					self.__text_action(("Existen {} paralelos de {} con {}...").format(len(parallels), course, professor))
				index = 1

				for parallel in parallels:
					classroom = parallel['classroom']
					if classroom == "":
						classroom = "un aula por definir"
					period = parallel['period']
					self.__text_action(("Paralelo {}. Las clases son en {} en horario {}").format(index, classroom, period))
					index += 1

		else:
			self.__text_action("Perdón, no encontré la materia que buscas")

	def __maps_action(self, nlu_entities=None):
		location = None
		map_type = None
		if nlu_entities is not None:
			if 'location' in nlu_entities:
				location = nlu_entities['location'][0]["value"]
			if "Map_Type" in nlu_entities:
				map_type = nlu_entities['Map_Type'][0]["value"]

		if location is not None:
			maps_url = self.nlg.get_map_url(location, map_type)
			maps_action = "Ten un mapa de %s." % location
			body = {'url': maps_url}
			requests.post("http://localhost:8888/image", data=json.dumps(body))
			self.speech.synthesize_text(maps_action)
		else:
			self.__text_action("Perdón, no encontré el lugar que buscas")

	def __text_action(self, text=None):
		if text is not None:
			requests.get("http://localhost:8888/statement?text=%s" % text)
			self.speech.synthesize_text(text)

	def __debugger_recognition(self, enable=True):
		if self.debugger_enabled:
			print("...Loading...")
			try:
				r = requests.get("http://localhost:8888/recognition?enabled=%s" % str(enable))
				if r.status_code != 200:
					print("Used wrong endpoint for recognition debugging")
			except Exception as e:
				print(e)

if __name__ == "__main__":
	bot = Bot()
	bot.start()
