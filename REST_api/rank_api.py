from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop 

import re
import requests



"""
ranking service for input department and course numbers
e.g.:
localhost:7777/rank/?rank=COMS+W4111+w1004+w4995
"""

class RankHandler(RequestHandler):
	def set_default_headers(self):
		self.set_header('Access-Control-Allow-Credentials', 'true')
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "content-type, Authorization, Accept, X-Requested-With")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
	
	def get(self):
	    #take department + course_number input 
	    #e.g.: 'COMS w4111 w4995 w4170'
	    input = self.get_argument('rank','none')
	    self.write(rank_course(input))
	    
	
	def options(self):
		self.set_status(204)
		self.finish()

	def post(self):
		input = self.get_argument('ex','none')
		self.write(input)

def rank_course(inputstr):
	inputstr = re.findall(r'\w+', inputstr.upper())
	depart = inputstr[0]
	cnums = inputstr[1:]
	sDict = {}
	for cnum in cnums:
		score = requests.post(url = 'http://localhost:7778/evalue/', data = {'depart':depart, 'cnum':cnum})
		sDict.update({cnum:float(score.text)})


	top5 = sorted(sDict, key=sDict.get, reverse=True)[:5]	
	
	rankinfo = requests.post(url = 'http://localhost:7778/getinfo/', data = {'depart':depart, 'cnums':' '.join(top5)})

	return rankinfo.text



if __name__ == "__main__":
		handler_mapping = [
							(r'/rank/', RankHandler),
							]
		application = Application(handler_mapping)
		application.listen(7777)
		IOLoop.current().start()