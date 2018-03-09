# -*- coding: utf-8 -*-

class Knowledge(object):
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
			return "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=roadmap&format=png" % location

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
