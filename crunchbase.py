# Crunchbase API Tests

import requests
import json
import wget

class crunchbase:
	def __init__(self):
		with open("crunchbase.key") as f:
			self.api_key = f.read()

	def loadJSON(self, query):

		api_key = "zbehy2ahumjcscdjum5u9gtv"
		baseURL = "http://api.crunchbase.com/v/1"
		qURL = baseURL+query+".js?api_key="+api_key

		r = requests.get(qURL)
		if r.status_code == 200:
			return r.json()
		else:
			s = "HTTP code " + str(r.status_code)
			raise NetworkError(s)

	def getImageURL(self, json):
		baseImageURL = "http://crunchbase.com/"
		imageURL = baseImageURL + json['image']['available_sizes'][-1][-1]
		return imageURL

	def getImage(self, imageURL):
		image = wget.download(imageURL)	
		return image

