import web
import json
import random
import time
import shelve
import string

def make_text(string):
	return string

urls = ('/', 'tutorial')
render = web.template.render('templates/')
app = web.application(urls, globals())


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

"""Assumption: vocabulary text file uses the format KR = EN = JP"""
VOCAB_FILE = "vocab.txt"
WHITE_FILE = "white.shv"
KR = "KR"
EN = "EN"
JP = "JP"
SHELVEKEY = "art history"

whiteList = None

SHELVE = shelve.open(WHITE_FILE)
try: 
	print SHELVE[SHELVEKEY]
	whiteList = SHELVE[SHELVEKEY]
except KeyError:
	SHELVE[SHELVEKEY] = whiteList = {}
	print "Whitelist is empty."

#vocabList = None

def convertFileToArray():

	convertedList = {}
	lineNumber = 0

	with open(VOCAB_FILE) as f:
		for line in f:
			line = line.strip()
			lineNumber = lineNumber + 1
			if (line != "" and not line.startswith("#")):
				originalLine = line
				try: 
					line = line.strip().split("=")
					krContent = line[0].strip()
					enContent = line[1].strip()
					jpContent = line[2].strip()
					convertedList[enContent] = {KR: krContent,JP: jpContent}
					#card = {KR: krContent, EN: enContent, JP: jpContent}
				except:
					print "Error in line " + str(lineNumber) + ": ", 
					print originalLine
					raise

	return convertedList


def getRandomCard(cards):
	randomEntry = random.choice(cards.keys())
	return {KR: cards[randomEntry][KR], JP: cards[randomEntry][JP], EN: randomEntry}

vocabList = convertFileToArray()


def whiteListCard(card):
	for cardEN, cardKRJP in card.iteritems():
		vocabList.pop(cardEN,None)
		whiteList[cardEN] = cardKRJP
	SHELVE[SHELVEKEY] = whiteList
	return

def convertWhiteListCards():
	convertedList = []
	for cardEN,cardKRJP in whiteList.iteritems():
		newEntry = {EN: cardEN, KR: cardKRJP[KR], JP: cardKRJP[JP]}
		convertedList.append(newEntry)
	return convertedList

def removeWhiteListCard(card):
	print card
	for cardEN,cardKRJP in card.iteritems():
		vocabList[cardEN] = cardKRJP
		whiteList.pop(cardEN,None)
	SHELVE[SHELVEKEY] = whiteList
	return


class tutorial:
	def GET(self):
		return render.tutorial()

	def POST(self):
		print "Received POST"
		time.sleep(2)
		web.header('Content-Type', 'application/json')
		cmd = web.input()["cmd"]
		if cmd:
			if cmd == "nextcard":
				result = json.dumps(getRandomCard(vocabList))
				data = { 'dateTime':'asdf', 'random':'fdsa'} 
				print result
				return result
			elif cmd == "getBlackList":
				data = { 'dateTime':'asdf', 'random':'fdsa'} 
				result = json.dumps(convertWhiteListCards());
				return result
			elif cmd == "addBL":
				cardConverted = {web.input()["BLcard[EN]"]: {KR: web.input()["BLcard[KR]"], JP: web.input()["BLcard[JP]"]}}
				#cardConverted = {EN: web.input()["BLcard[EN]"], KR: web.input()["BLcard[KR]"], JP: web.input()["BLcard[JP]"]}
				whiteListCard(cardConverted)
				return json.dumps("success");
			elif cmd == "removeBL":
				cardConverted = {web.input()["BLcard[EN]"]: {KR: web.input()["BLcard[KR]"], JP: web.input()["BLcard[JP]"]}}
				removeWhiteListCard(cardConverted)
				return json.dumps("success");


		#print getAjaxArg("cmd")
		return make_text({"a":"b"})


if __name__ == '__main__':
	app.run()