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
			actual_schedule = schedules[1]
		elif now > dt.time(12,25,0) and now <= dt.time(14,40,0):
			actual_schedule = schedules[2]
		elif now > dt.time(14,40,0) and now <= dt.time(16,55,0):
			actual_schedule = schedules[3]
		elif now > dt.time(16,55,0) and now <= dt.time(18,50,0):
			actual_schedule = schedules[4]
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

	# CUSTOM
	def get_UPBroute_url(self, location):
		if location == "Biblioteca":
			return "http://i.imgur.com/ycAdrw1.gif"
		elif location == "Parqueo":
			return "http://i.imgur.com/5rXCoSw.gif"
		else:
			return "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=roadmap&format=png" % location

	# CUSTOM
	def get_schedule_url(self, prof):
		if prof == u"Marcel Barrero":
			return "http://i.imgur.com/Vqm4nOR.png"
		elif prof == u"Alex Villazón":
			return "http://i.imgur.com/fBo0k7w.png"
		else:
			return "http://i.imgur.com/fBo0k7w.png"

	# CUSTOM
	def get_sc_url(self, career):
		if career == u'Comunicación':
			return "http://i.imgur.com/4ODAbxh.png"
		elif career == u'Ingeniería Civil':
			return "http://i.imgur.com/wHJ6NYX.png"
		elif career == u'Economía':
			return "http://i.imgur.com/724G39v.png"
		elif career == u'Ingeniería de la Producción':
			return "http://i.imgur.com/87lSurk.png"
		elif career == u'Derecho':
			return "http://i.imgur.com/dkb3Z3v.png"
		elif career == u'Diseno Gráfico':
			return "http://i.imgur.com/lQ69mpl.png"
		elif career == u'Ingeniería de Sistemas Computacionales':
			return "http://i.imgur.com/Hg2uqsg.png"
		elif career == u'Ingeniería Electromecánica':
			return "http://i.imgur.com/olUqRPR.png"
		elif career == u'Ingeniería Electrónica y Telecomunicaciones':
			return "http://i.imgur.com/39fd6il.png"
		elif career == u'Ingeniería Petrolera y Gas Natural':
			return "http://i.imgur.com/frfdXtv.png"
		elif career == u'Ingeniería Industrial y de Sistemas':
			return "http://i.imgur.com/rb0tp3g.png"
		elif career == u'Ingeniería Financiera':
			return "http://i.imgur.com/yyG8GLY.png"
		elif career == u'Marketing y Logística':
			return "http://i.imgur.com/m15JNsw.png"
		elif career == u'Arquitectura':
			return "http://i.imgur.com/x06IbD4.png"
		elif career == u'Ingeniería Comercial':
			return "http://i.imgur.com/oKz9hhl.png"
		elif career == u'Administración de Empresas':
			return "http://i.imgur.com/eV5f01b.png"
		else:
			return ""
