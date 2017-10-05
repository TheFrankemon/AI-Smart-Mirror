# bot.py
# -*- coding: utf-8 -*-
# speechrecognition, pyaudio, brew install portaudio
import sys
import random
sys.path.append("./")

import requests
import datetime
import dateutil.parser
import json
import traceback
from nlg import NLG
from speech import Speech
from knowledge import Knowledge
from vision import Vision
from mongo import Mongo

my_name = "Franco"
launch_phrase = "hola"
use_launch_phrase = True
with open('config.json') as data_file:    
	conf = json.load(data_file)
debugger_enabled = True
camera = 0

class Bot(object):
    def __init__(self):
        self.nlg = NLG(user_name=my_name)
        self.speech = Speech(launch_phrase=launch_phrase, debugger_enabled=debugger_enabled)
        self.knowledge = Knowledge(str(conf["weather_api_token"]))
        self.vision = Vision(camera=camera)
        self.mongo = Mongo()

    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        :return:
        """
        while True:
            requests.get("http://localhost:8888/clear")
            if self.vision.recognize_face('c1.png'):
                print "Found face"
                self.vision.recognize_face('c2.png')
                self.__info_action(launch_phrase)
                if use_launch_phrase:
                    self.mongo.add("",
                        "/home/pi/AI-Smart-Mirror-Franco/img/c1.png",
                        "/home/pi/AI-Smart-Mirror-Franco/img/c2.png")
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

        # received audio data, now we'll recognize it using Google Speech Recognition
        #speech = self.speech.google_speech_recognition(recognizer, audio)

        # received audio data, now we'll recognize it using Wit Speech API
        speech = self.speech.wit_speech_recognition(recognizer, audio, str(conf["wit_ai_token"]))

        if speech is not None:
            try:
                ## Uncomment for HARDCODED SPEECH ##
                #speech = "torta UPB"
                print 'Requesting WIT.AI [' + speech + ']'
                r = requests.get('https://api.wit.ai/message?v=20170403&q=%s' % speech, headers={'Authorization': str(conf["wit_ai_token"])})
                print 'Text ' + r.text
                #print r.headers['authorization']
                json_resp = json.loads(r.text)
                entities = None
                intent = None
                if 'entities' in json_resp and 'Intent' in json_resp['entities']:
                    entities = json_resp['entities']
                    intent = json_resp['entities']['Intent'][0]["value"]

                print intent
                if intent == 'greeting':
                    self.__text_action(self.nlg.greet())
                elif intent == 'chiefs':     #CUSTOM
                    self.__chiefs_action(entities)
                elif intent == 'rooms':      #CUSTOM
                    self.__rooms_action(entities)
                elif intent == 'buses':      #CUSTOM
                    self.__text_action(self.nlg.buses())
                elif intent == 'schedules':  #CUSTOM
                    self.__schedules_action(entities)
                elif intent == 'career_semesterclasses':  #CUSTOM
                    self.__career_sc_action(entities)
                elif intent == 'weather':
                    self.__weather_action(entities)
                elif intent == 'news':
                    self.__news_action()
                elif intent == 'maps':
                    self.__maps_action(entities)
                elif intent == 'holidays':
                    self.__holidays_action()
                elif intent == 'appearance':
                    self.__appearance_action()
                elif intent == 'user name':
                    self.__user_name_action()
                elif intent == 'personal status':
                    self.__personal_status_action()
                elif intent == 'joke':
                    self.__joke_action()
                elif intent == 'insult':
                    self.__insult_action()
                    return
                elif intent == 'appreciation':
                    self.__appreciation_action()
                    return
                else: # No recognized intent
                    self.__text_action("Perdón, aún estoy en kinder.")
                    

            except Exception as e:
                print "Failed wit!"
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

    def __joke_action(self):
        joke = self.nlg.joke()

        if joke is not None:
            self.__text_action(joke)
        else:
            self.__text_action("I couldn't find any jokes")

    def __user_name_action(self):
        if self.nlg.user_name is None:
            self.__text_action("I don't know your name. You can configure it in bot.py")

        self.__text_action(self.nlg.user_name)

    def __appearance_action(self):
        requests.get("http://localhost:8888/face")

    def __appreciation_action(self):
        self.__text_action(self.nlg.appreciation())

    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())

    def __insult_action(self):
        self.__text_action(self.nlg.insult())

    def __personal_status_action(self):
        self.__text_action(self.nlg.personal_status())

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8888/statement?text=%s" % text)
            self.speech.synthesize_text(text)

    def __news_action(self):
        headlines = self.knowledge.get_news()

        if headlines:
            requests.post("http://localhost:8888/news", data=json.dumps({"articles":headlines}))
            self.speech.synthesize_text(self.nlg.news("past"))
            interest = self.nlg.article_interest(headlines)
            if interest is not None:
                self.speech.synthesize_text(interest)
        else:
            self.__text_action("I had some trouble finding news for you")

    # CUSTOM
    def __chiefs_action(self, nlu_entities=None):

        chief = None

        if nlu_entities is not None:
            if 'Career_Type' in nlu_entities:
                career_type = nlu_entities['Career_Type'][0]['value']
                print career_type
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
                print location

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
                print prof

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
                print career

        if career is not None:
            career_url = self.knowledge.get_sc_url(career)
            body = {'url': career_url}
            requests.post("http://localhost:8888/image", data=json.dumps(body))
            
            career_action = "Ten el detalle de Semestres y Materias de %s." % career
            self.speech.synthesize_text(career_action)
        else:
            self.__text_action("Perdón, no encontré la carrera que buscas.")

    def __weather_action(self, nlu_entities=None):

        current_dtime = datetime.datetime.now()
        skip_weather = False # used if we decide that current weather is not important

        weather_obj = self.knowledge.find_weather()
        temperature = weather_obj['temperature']
        icon = weather_obj['icon']
        wind_speed = weather_obj['windSpeed']

        weather_speech = self.nlg.weather(temperature, current_dtime, "present")
        forecast_speech = None

        if nlu_entities is not None:
            if 'datetime' in nlu_entities:
                if 'grain' in nlu_entities['datetime'][0] and nlu_entities['datetime'][0]['grain'] == 'day':
                    dtime_str = nlu_entities['datetime'][0]['value'] # 2016-09-26T00:00:00.000-07:00
                    dtime = dateutil.parser.parse(dtime_str)
                    if current_dtime.date() == dtime.date(): # hourly weather
                        forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj)
                    elif current_dtime.date() < dtime.date(): # sometime in the future ... get the weekly forecast/ handle specific days
                        forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj)
                        skip_weather = True
            if 'Weather_Type' in nlu_entities:
                weather_type = nlu_entities['Weather_Type'][0]['value']
                print weather_type
                if weather_type == "current":
                    forecast_obj = {'forecast_type': 'current', 'forecast': weather_obj['current_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'today':
                    forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'tomorrow' or weather_type == '3 day' or weather_type == '7 day':
                    forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                    skip_weather = True


        weather_data = {"temperature": temperature, "icon": icon, 'windSpeed': wind_speed, "hour": datetime.datetime.now().hour}
        requests.post("http://localhost:8888/weather", data=json.dumps(weather_data))

        if not skip_weather:
            self.speech.synthesize_text(weather_speech)

        if forecast_speech is not None:
            self.speech.synthesize_text(forecast_speech)

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

    def __holidays_action(self):
        holidays = self.knowledge.get_holidays()
        next_holiday = self.__find_next_holiday(holidays)
        requests.post("http://localhost:8888/holidays", json.dumps({"holiday": next_holiday}))
        self.speech.synthesize_text(self.nlg.holiday(next_holiday['localName']))

    def __find_next_holiday(self, holidays):
        today = datetime.datetime.now()
        for holiday in holidays:
            date = holiday['date']
            if (date['day'] > today.day) and (date['month'] > today.month):
                return holiday

        # next year
        return holidays[0]

if __name__ == "__main__":
    bot = Bot()
    bot.start()
