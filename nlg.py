# nlg.py
# -*- coding: utf-8 -*-
import random
import datetime as dt

class NLG(object):
	"""
	Used to generate natural language. Most of these sections are hard coded. However, some use simpleNLG which is
	used to string together verbs and nouns.
	"""
	def __init__(self):
		# make random more random by seeding with time
		random.seed(dt.datetime.now())

	def intro(self):
		intros = [
			"Bienvenidos a la UPB, soy UPB Smart Booth.",
			"Bienvenidos a su nueva casa, soy UPB Smart Booth.",
			"Hola! Soy UPB Smart Booth.",
			"Esta es la UPB. Me presento, soy UPB Smart Booth."
		]
		
		intros2 = [
			"Digita tu nombre y apellido por favor",
			"Escribe tu nombre y apellido por favor",
			"Te pido que escribas tu nombre y apellido por favor",
			"Registra tu nombre y apellido por favor",
			"Por favor, escribe tu nombre y apellido",
			"Puedes darme tu nombre y apellido, por favor?"
		]

		return random.choice(intros) + " " + random.choice(intros2)

	def acknowledge(self, user_name):
		phrases = [
			"Muy bien, así que eres %s" % user_name,
			"Así que tu nombre es %s" % user_name,
			"Mucho gusto, %s" % user_name,
			"Cómo estás, %s" % user_name,
			"Qué tal %s" % user_name,
			"Hola %s" % user_name,
			"%s %s" % (self.time_of_day(dt.datetime.now()), user_name)
		]

		return random.choice(phrases) + ". Espera unos segundos por favor"

	def goodbye(self):
		goodbyes = [
			"Todo listo!",
			"Todo salió bien, gracias!",
			"Disculpa por la demora, ya guardé tus datos.",
			"Genial! Ya guardé tus datos."
		]
		
		goodbyes2 = [
			"Por favor pasa, toma asiento que enseguida te atenderán",
			"Pasa, toma asiento por favor",
			"Así que puedes pasar a tomar asiento",
			"Te pido por favor tomar asiento, te atenderán enseguida"
		]

		return random.choice(goodbyes) + " " + random.choice(goodbyes2)

	def time_of_day(self, date, with_adjective=False):
		ret_phrase = ""
		if date.hour < 12:
			ret_phrase = "Buenos días"
			if with_adjective:
				ret_phrase = "%s %s" % ("this", ret_phrase)
		elif (date.hour >= 12) and (date.hour < 18):
			ret_phrase = "Buenas tardes"
			if with_adjective:
				ret_phrase = "%s %s" % ("this", ret_phrase)
		elif date.hour >= 18:
			ret_phrase = "Buenas noches"
			if with_adjective:
				ret_phrase = "%s %s" % ("this", ret_phrase)

		return ret_phrase
