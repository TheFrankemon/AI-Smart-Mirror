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

	def info(self, phrase):
		infos = [
			"Este es un prototipo del UPB Smart Booth.",
			"Te presento al UPB Smart Booth.",
			"Hola! Soy UPB Smart Booth y aun estoy en Beta."
		]
		
		infos2 = [
			"Di \"" + phrase.capitalize() + "\" para interactuar conmigo",
			"Di \"" + phrase.capitalize() + "\" para que pueda ayudarte",
			"Di \"" + phrase.capitalize() + "\" para darte una mano"
		]

		return random.choice(infos) + " " + random.choice(infos2)

	def acknowledge(self):
		simple_acknoledgement = [
			"Sí?",
			"Qué deseas?",
			"Qué necesitas de mí?",
			"Cómo puedo ayudarte?",
			"Qué puedo hacer por ti?"
		]

		ret_phrase = ""
		greet_with_date = random.choice([True, False])
		if greet_with_date:
			ret_phrase = random.choice(simple_acknoledgement)
		else:
			date = dt.datetime.now()
			ret_phrase = ("{}. {}").format(self.time_of_day(date), random.choice(simple_acknoledgement))

		return ret_phrase

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

	# CUSTOM
	def buses(self):
		actual_schedule = None
		schedules = [
			"10:10",
			"12:25",
			"14:40",
			"16:55",
			"18:50"
		]

		now = dt.datetime.now().time()
		actual_schedule = "El próximo bus debería salir a las "
		if now > dt.time(0,0,0) and now <= dt.time(10,10,0):
			actual_schedule += schedules[0]
		elif now > dt.time(10,10,0) and now <= dt.time(12,25,0):
			actual_schedule += schedules[1]
		elif now > dt.time(12,25,0) and now <= dt.time(14,40,0):
			actual_schedule += schedules[2]
		elif now > dt.time(14,40,0) and now <= dt.time(16,55,0):
			actual_schedule += schedules[3]
		elif now > dt.time(16,55,0) and now <= dt.time(18,50,0):
			actual_schedule += schedules[4]
		else:
			actual_schedule = "Lo siento, el último bus ya salió."
			
		return actual_schedule

	def appreciation(self):
		phrases = [
			"No hay problema!",
			"No, gracias a ti",
			"De nada",
			"No, por favor",
			"Claro, no hay problema",
			"Ni lo menciones"
		]

		return random.choice(phrases)

	def get_map_url(self, location, map_type=None):
		if map_type == "satellite":
			return "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=satellite&format=png" % location
		elif map_type == "terrain":
			return "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=terrain&format=png" % location
		elif map_type == "hybrid":
			return "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=hybrid&format=png" % location
		else:
			return "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=roadmap&format=png" % location
