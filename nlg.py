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

	def acknowledge(self, user_name = ""):
		simple_acknoledgement = [
			"Sí?",
			"Qué puedo hacer por vos?",
			"Qué querés?"
		]

		personal_acknowledgement = [
			"Qué necesitas de mí, %s?" % user_name,
			"Cómo puedo ayudarte, %s?" % user_name,
			"Qué puedo hacer por vos, %s?" % user_name,
			"Hola %s, qué puedo hacer por vos?" % user_name,
			"Hey %s, qué puedo hacer por vos?" % user_name
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

	def searching(self):
		searching_phrases = [
			"I'll see what I can find"
		]

		return random.choice(searching_phrases)

	def personal_status(self, status_type=None):
		positive_status=[
			"I'm doing well",
			"Great, thanks for asking",
			"I'm doing great"
		]

		negative_status = [
			"I'm not doing well",
			"I'm feeling terrible",
			"I'm not doing well today",
			"I could be much better"
		]

		moderate_status = [
			"I'm doing alright",
			"I'm okay",
			"I could be better",
			"I'm alright"
		]

		if status_type == 'negative':
			return random.choice(negative_status)
		elif status_type == 'moderate':
			return random.choice(moderate_status)

		return random.choice(positive_status)

	# CUSTOM
	def chiefs(self, career=None):
		chiefs = [
			"Ph.D. Mariana Lacunza",
			"Ph.D. Francisco Aguirre",
			"Ph.D.c. Ricardo Nogales",
			"Ph.D. Elizabeth Torres",
			"Mgr. Laura García",
			"Mgr. Marcelo Canedo",
			"Mgr. Marcel Barrero",
			"Ph.D. Cecilia Tapia",
			"Ph.D. Omar Ormachea",
			"Ing. Lourdes Oropeza",
			"Mgr. Agatha Da Silva",
			"Ph.D.c. Juan José Jordán",
			"Mgr. Martín Arandia",
			"Arq. Bernardo Cabrerizo",
			"Mgr. Rommel Rojas",
			"Ph.D. Juan Carlos Jordán"
		]
		
		if career == u'Comunicación':
			return chiefs[0]
		elif career == u'Ingeniería Civil':
			return chiefs[1]
		elif career == u'Economía':
			return chiefs[2]
		elif career == u'Ingeniería de la Producción':
			return chiefs[3]
		elif career == u'Derecho':
			return chiefs[4]
		elif career == u'Diseño Gráfico':
			return chiefs[5]
		elif career == u'Ingeniería de Sistemas Computacionales':
			return chiefs[6]
		elif career == u'Ingeniería Electromecánica':
			return chiefs[7]
		elif career == u'Ingeniería Electrónica y Telecomunicaciones':
			return chiefs[8]
		elif career == u'Ingeniería Petrolera y Gas Natural':
			return chiefs[9]
		elif career == u'Ingeniería Industrial y de Sistemas':
			return chiefs[10]
		elif career == u'Ingeniería Financiera':
			return chiefs[11]
		elif career == u'Marketing y Logística':
			return chiefs[12]
		elif career == u'Arquitectura':
			return chiefs[13]
		elif career == u'Ingeniería Comercial':
			return chiefs[14]
		elif career == u'Administración de Empresas':
			return chiefs[15]

		return None

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
		if now > dt.time(0,0,0) and now <= dt.time(10,10,0):
			actual_schedule = "El próximo bus debería salir a las " + schedules[0]
		elif now > dt.time(10,10,0) and now <= dt.time(12,25,0):
			actual_schedule = schedules[2]
		elif now > dt.time(12,25,0) and now <= dt.time(14,40,0):
			actual_schedule = schedules[3]
		elif now > dt.time(14,40,0) and now <= dt.time(16,55,0):
			actual_schedule = schedules[4]
		elif now > dt.time(16,55,0) and now <= dt.time(18,50,0):
			actual_schedule = schedules[5]
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

	def name(self):
		return self.user_name
