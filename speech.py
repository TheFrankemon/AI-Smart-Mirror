# speech.py
# speechrecognition, pyaudio, brew install portaudio
import speech_recognition as sr
import os
import requests
import wave
import json
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

class Speech(object):
	def __init__(self, launch_phrase="mirror mirror", status_enabled=False):
		self.launch_phrase = launch_phrase
		self.status_enabled = status_enabled
		self.__microphone_status(enable=False)

	def google_speech_recognition(self, recognizer, audio):
		speech = None
		try:
			speech = recognizer.recognize_google(audio)
			print('Google Speech Recognition thinks you said: "' + speech + '"')
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

		return speech

	def wit_speech_recognition(self, recognizer, audio, token):
		speech = None
		try: 
			speech = recognizer.recognize_wit(audio, token[7:])
			print('Wit Speech API thinks you said: "' + speech + '"')            
		except sr.UnknownValueError:
			print("Wit Speech API could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Wit Speech API service; {0}".format(e))

		return speech

	def listen_for_audio(self):
		# obtain audio from the microphone
		r = sr.Recognizer()
		m = sr.Microphone()
		with m as source:
			r.adjust_for_ambient_noise(source)
			self.__microphone_status(enable=True)
			print("I'm listening...")
			audio = r.listen(source)

		self.__microphone_status(enable=False)
		print("Found audio")
		return r, audio

	def is_call_to_action(self, recognizer, audio, token):
		#speech = self.google_speech_recognition(recognizer, audio)
		speech = self.wit_speech_recognition(recognizer, audio, token)

		if speech is not None and self.launch_phrase in speech.lower():
			return True

		return False

	def synthesize_text(self, text):
		tts = gTTS(text=text, lang='es')
		tts.save("tmp.mp3")
		song = AudioSegment.from_mp3("tmp.mp3")
		play(song)
		os.remove("tmp.mp3")

	def __microphone_status(self, enable=True):
		if self.status_enabled:
			print("Listening...")
			try:
				r = requests.get("http://localhost:8888/microphone?enabled=%s" % str(enable))
				if r.status_code != 200:
					print("Used wrong endpoint for microphone status")
			except Exception as e:
				print(e)
