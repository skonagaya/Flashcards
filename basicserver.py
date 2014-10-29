import web
import json
import random


def make_text(string):
	return string

urls = ('/', 'tutorial')
render = web.template.render('templates/')

app = web.application(urls, globals())

"""Assumption: vocabulary text file uses the format KR = EN = JP"""
VOCAB_FILE = "vocab.txt"
KR = "KR"
EN = "EN"
JP = "JP"



#vocabList = None

def convertFileToArray():

	convertedList = []

	with open(VOCAB_FILE) as f:
		for line in f:
			if (line != ""):
				line = line.strip().split("=")
				krContent = line[0].strip()
				enContent = line[1].strip()
				jpContent = line[2].strip()
				card = {KR: krContent, EN: enContent, JP: jpContent}
				convertedList.append(card)

	return convertedList

def getRandomCard(cards):
	return random.choice(cards)


vocabList = convertFileToArray()

class tutorial:
	def GET(self):
		return render.tutorial()

	def POST(self):
		print "Received POST"
		web.header('Content-Type', 'application/json')
		cmd = web.input()["cmd"]
		if cmd:
			if cmd == "nextcard":
				result = json.dumps(getRandomCard(vocabList))
				data = { 'dateTime':'asdf', 'random':'fdsa'} 
				print result
				return result
		#print getAjaxArg("cmd")
		return make_text({"a":"b"})


if __name__ == '__main__':
	app.run()