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
			"Este es un prototipo del UPB Smart Booth.",
			"Me presento, soy UPB Smart Booth.",
			"Hola! Soy UPB Smart Booth y aun estoy sprendiendo."
		]
		
		intros2 = [
			"Digita tu nombre y apellido por favor",
			"Escribe tu nombre y apellido por favor"
		]

		return random.choice(intros) + " " + random.choice(intros2)

	def user_name(self, user_name):
		phrases = [
			"Así que tu nombre es %s" % user_name,
			"Cómo estás %s" % user_name,
			"Qué tal %s" % user_name,
			"Hola %s" % user_name,
			"%s %s" % (self.time_of_day(dt.datetime.now()), user_name)
		]

		return random.choice(phrases)

	def acknowledge(self, user_name):
		if user_name is None:
			user_name = ""

		simple_acknoledgement = [
			"Sí?",
			"Qué puedo hacer por vos?"
		]

		personal_acknowledgement = [
			"Qué necesitas de mí, %s?" % user_name,
			"Cómo puedo ayudarte, %s?" % user_name,
			"Qué puedo hacer por vos, %s?" % user_name
		]

		choice = 0
		if user_name is not None:
			choice = random.randint(0, 2)
		else:
			choice = random.randint(0,1)

		ret_phrase = ""

		if choice == 0:
			ret_phrase = random.choice(simple_acknoledgement)
		elif choice == 1:
			date = dt.datetime.now()
			ret_phrase = "%s. Qué puedo hacer por vos?" % self.time_of_day(date)
		else:
			ret_phrase = random.choice(personal_acknowledgement)

		return ret_phrase

	"""
	def searching(self):
		searching_phrases = [
			"I'll see what I can find"
		]

		return random.choice(searching_phrases)
	"""

	def insult(self):
		return "That's not very nice. Talk to me again when you have fixed your attitude"

	def appreciation(self):
		phrases = [
			"No hay problema!",
			"No, gracias a ti",
			"De nada",
			"No, por favor",
			"Ni lo menciones"
		]

		return random.choice(phrases)

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
