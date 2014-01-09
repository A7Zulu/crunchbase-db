# Crunchbase API Tests
from crunchbase import crunchbase
import redis
import Image
import io


def flushdb():
	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)
	r.flushdb()
	print "Database flushed"

# Downloads the image for all companies in companies.csv and stores them in Redis
def download():
	cb = crunchbase()
	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)
	count = 0
	
	with open("data/companies.csv", 'r') as f:
		next(f) #skips header row
		for line in f:
			company = line.split(',')[0]		
			json = cb.loadJSON(company)
			imageURL = cb.getImageURL(json)
			print imageURL
			image = cb.getImage(imageURL)
			print "Downloaded %s" % (company)
			r.hset(company, "image", image.getvalue())
			print "Stored %s" % (company)
			count += 1

	f.close()
	print "%s companies downloaded and stored" % (count)


def main():
	flushdb()
	download()


if __name__ == '__main__':
	main()
