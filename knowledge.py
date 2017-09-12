# -*- coding: utf-8 -*-
import requests
import json
import feedparser
import datetime

class Knowledge(object):
    def __init__(self, weather_api_token, news_country_code='us'):
        self.news_country_code = news_country_code
        self.weather_api_token = weather_api_token

    def find_weather(self):
        loc_obj = self.get_location()

        lat = loc_obj['lat']
        lon = loc_obj['lon']

        weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s" % (self.weather_api_token, lat, lon)
        print "WILL PRINT THE FORECAST"
        print weather_req_url
        r = requests.get(weather_req_url)
        weather_json = json.loads(r.text)

        temperature = int(weather_json['currently']['temperature'])

        current_forecast = weather_json['currently']['summary']
        hourly_forecast = weather_json['hourly']['summary']
        daily_forecast = weather_json['daily']['summary']
        icon = weather_json['currently']['icon']
        wind_speed = int(weather_json['currently']['windSpeed'])

        return {'temperature': temperature, 'icon': icon, 'windSpeed': wind_speed, 'current_forecast': current_forecast, 'hourly_forecast': hourly_forecast, 'daily_forecast': daily_forecast}

    def get_location(self):
        # get location
        location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
        r = requests.get(location_req_url)
        location_obj = json.loads(r.text)

        lat = location_obj['latitude']
        lon = location_obj['longitude']

        return {'lat': lat, 'lon': lon}

    def get_ip(self):
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']

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

    def get_news(self):
        ret_headlines = []
        feed = feedparser.parse("https://news.google.com/news?ned=%s&output=rss" % self.news_country_code)

        for post in feed.entries[0:5]:
            ret_headlines.append(post.title)

        return ret_headlines

    def get_holidays(self):
        today = datetime.datetime.now()
        r = requests.get("http://kayaposoft.com/enrico/json/v1.0/?action=getPublicHolidaysForYear&year=%s&country=usa" % today.year)
        holidays = json.loads(r.text)

        return holidays

