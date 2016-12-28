# -*- coding: utf-8 -*-
import json
import time
from twython import Twython
from twython import TwythonStreamer
from pyv4l2.frame import Frame

class MyStreamer(TwythonStreamer):
	def initialize(self, handler):
		print "initialize stremmer"
		self.text = None
		self.error = None
		self.last_update = 0
		self.handler = handler
		self.config = handler.config

	def on_success(self, data):
		print "ON SUCCESS"
		diff = int(time.time()) - self.last_update
		if 'text' in data and diff > self.config["interval"]:
			print "DATA", data
			text = data['text'].encode('utf-8')
			data = text.lower().split()
			self.handler.dispatcher(data)

	def on_error(self, status_code, data):
		self.error = str(status_code)




class Cambot(object):
	def __init__(self):
		self.config = json.loads(open("config.json").read())
		self.stream = None
		self.twitter = Twython(self.config["app_key"],
							   self.config["app_secret"],
							   self.config["oauth_token"], 
							   self.config["oauth_secret"])

	def start_streamming(self):
		self.stream = MyStreamer(self.config["app_key"],
								 self.config["app_secret"],
								 self.config["oauth_token"], 
								 self.config["oauth_secret"])
		self.stream.initialize(self)
		self.stream.statuses.filter(track=self.config["filter"])	

	def dispatcher(self, data):
		if "ver" in data:
			data.pop(data.index("ver"))
			for d in data:
				if d.find("cam") > -1:
					idx = d.replace("cam","")
					try:
						idx = int(idx)
					except:
						pass
			if idx:
				self.get_picture(idx)

	def get_picture(self, idx):
		frame = Frame('/dev/video%d' % idx)
		frame_data = frame.get_frame()
		print frame_data


def main():
	cambot= Cambot()
	cambot.start_streamming
	while True:
		time.sleep(5)


if __name__ == '__main__':
	main()
