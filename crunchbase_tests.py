# Crunchbase API Tests
from crunchbase import crunchbase
import redis
import Image
import io

def main():
	cb = crunchbase()
	company = "/company/whistle"
	json = cb.loadJSON(company)
	imageURL = cb.getImageURL(json)
	image = cb.getImage(imageURL)
	output = io.BytesIO()
	image.save(output, format=image.format)

	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)

	r.set(company, output.getvalue())
	print r.get(company)


if __name__ == '__main__':
	main()
