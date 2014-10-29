
"""Assumption: vocabulary text file uses the format KR = EN = JP"""
VOCAB_FILE = "vocab.txt"
KR = "KR"
EN = "EN"
JP = "JP"


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
