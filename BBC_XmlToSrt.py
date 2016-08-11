import re
import sys
from bs4 import BeautifulSoup


def toSrt(xml_string):
	srt = ''
	xml_string        = xml_string.replace("<br/>","\n")
	texts             = BeautifulSoup(xml_string)
	listOfTranscripts = texts.findAll("p")

	colorDict = {}

	colorInfo = texts.findAll("style")
	for i in colorInfo:
		colorDict[i['id']]=i['tts:color']

	captionNumber = 1
	for captions in listOfTranscripts:
		
		spanList = captions.findAll("span")
		for i in spanList:
			newtag = texts.new_tag("font",color=i['tts:color'])
			newtag.string = i.string
			i.replace_with(newtag)

		start = captions['begin']
		end   = captions['end']
		
		start = formatTime(start)
		end = formatTime(end)
		captionContent = captions.contents

		caption = ""
		for content in captionContent:
			caption += str(content)

		srt += str(captionNumber) + '\n'
		srt += start + ' --> ' + end + '\n'
		srt += caption + '\n\n'

		captionNumber += 1

	return srt

def formatTime(time):
	

	pieces    = time.split(".")
	pieces[1] = (pieces[1]+"0"*3)[0:3]
	formatted = "%s,%s" % (pieces[0],pieces[1])

	return formatted

def main():
	f = open(sys.argv[1],"r")
	q = f.read()
	s = toSrt(q)
	print(s)


if __name__ == "__main__":
	main()