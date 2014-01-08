# Crunchbase API Tests

import requests
import json
import Image
import io
import urllib2 as urllib

class crunchbase:
	def __init__(self):
		with open("crunchbase.key") as f:
			self.api_key = f.read()

	def loadJSON(self, query):
		# Creating the base Crunchbase API URL with the API Key and Query
		api_key = "zbehy2ahumjcscdjum5u9gtv"
		baseURL = "http://api.crunchbase.com/v/1"
		qURL = baseURL+query+".js?api_key="+api_key

		# Retrieves the JSON from API
		r = requests.get(qURL)
		if r.status_code == 200:
			return r.json()
		else:
			s = "HTTP code " + str(r.status_code)
			raise NetworkError(s)

	def getImageURL(self, json):
		# Retrieves the name of the largest image from the JSON and creates an URL string for where image is located
		baseImageURL = "http://crunchbase.com/"
		imageURL = baseImageURL + json['image']['available_sizes'][-1][-1]
		return imageURL

	def getImage(self, imageURL):
		# Retreives the image at specified URL
		fd = urllib.urlopen(imageURL)
		image_file = io.BytesIO(fd.read())	
		im = Image.open(image_file)

		return im

