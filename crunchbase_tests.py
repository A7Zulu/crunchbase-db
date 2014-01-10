# Crunchbase API Tests
from crunchbase import crunchbase
import redis
import Image
import io


def flushdb():
	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)
	r.flushdb()
	print "Database flushed"

# For testing and troubleshooting purposes of downloading one company
def downloadOne(company):
	cb = crunchbase()
	json = cb.loadJSON(company)
	imageURL = cb.getImageURL(json)
	print imageURL
	try:
		image = cb.getImage(imageURL)
		print "Downloaded %s" % (company)
	except:
		pass


# Downloads the image for all companies in companies.csv and stores them in Redis
def download():
	cb = crunchbase()
	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)
	count = 0
	
	with open("data/companies.csv", 'r') as f:
		next(f) #skips header row
		for line in f:
			company = line.split(',')[0]		
			if r.exists(company):
				print "%s already downloaded and stored" % (company)
				continue
			try:
				json = cb.loadJSON(company)
				imageURL = cb.getImageURL(json)
				print imageURL
				image = cb.getImage(imageURL)
				print "Downloaded %s" % (company)
				r.hset(company, "image", image.getvalue())
				print "Stored %s" % (company)
				count += 1
			except:
				pass

	f.close()
	print "%s companies downloaded and stored" % (count)


def main():
	#flushdb()
	download()
	#downloadOne("/company/3gear-systems")

if __name__ == '__main__':
	main()
