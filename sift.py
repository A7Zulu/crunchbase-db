import numpy as np
import cv2
import redis
from matplotlib import pyplot as plt


# Stupid function because OpenCL library is broken
def init():
	sift = cv2.SIFT()
	try:
		kp1, des1 = sift.detectAndCompute(cv2.imread('test-images/amazon-test.jpg',0))
	except Exception:
		pass



def brutesearch(img):
	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)
	sift = cv2.SIFT()
	keys = r.keys("*")
	count = 0
	
	kp1, des1 = sift.detectAndCompute(img, None) #Query image



	for key in keys:
		if r.hexists(key, "descriptors"):
			des2 = r.hget(key, "descriptors")
			if match(des1, des2):
				print "Match found for %s" % (key)
				return


# Compute Keypoints for the Database
def computeKeyPoints():
	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)
	sift = cv2.SIFT()
	keys = r.keys("*")
	count = 0

	print "Starting to compute keypoints and descriptors\n"
	for key in keys:
		if not r.hexists(key, "descriptors"):
			nparr = np.fromstring(r.hget(key, "image"), np.uint8)
			img = cv2.imdecode(nparr, 0)
			try:
				kp, des = sift.detectAndCompute(img, None)
				r.hset(key, "descriptors", des)
				print "Descriptors computed for %s" % (key)
				count += 1		
			except:
				pass

	print "%s sets of descriptors computed" % (count)



def test():
	r = redis.StrictRedis(host='192.168.1.109', port=6379, db=0)

	nparr = np.fromstring(r.hget("/company/amazon", "image"), np.uint8)
	img2 = cv2.imdecode(nparr, 0)
	#img1 = cv2.imread('test-images/workday-test.jpg',0) # queryImage
	img1 = cv2.imread('test-images/amazon-test.jpg',0) # trainImage

	# Initiate SIFT detector
	sift = cv2.SIFT()

	# find the keypoints and descriptors with SIFT
	try:
		kp1, des1 = sift.detectAndCompute(img1,None)
	except Exception:
		pass
	
	kp1, des1 = sift.detectAndCompute(img1,None)
	kp2, des2 = sift.detectAndCompute(img2,None)
	
	# FLANN parameters
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)   # or pass empty dictionary

	flann = cv2.FlannBasedMatcher(index_params,search_params)

	matches = flann.knnMatch(des1,des2,k=2)

	# Need to draw only good matches, so create a mask
	matchesMask = [[0,0] for i in xrange(len(matches))]

	# ratio test as per Lowe's paper
	for i,(m,n) in enumerate(matches):
	    if m.distance < 0.7*n.distance:
	        matchesMask[i]=[1,0]

	draw_params = dict(matchColor = (0,255,0),
	                   singlePointColor = (255,0,0),
	                   matchesMask = matchesMask,
	                   flags = 0)

	img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

	cv2.imwrite('sift_keypoints.jpg',img3)
	


def match(des1, des2):
	MIN_MATCH_COUNT = 10

	# FLANN parameters
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)   # or pass empty dictionary

	flann = cv2.FlannBasedMatcher(index_params,search_params)

	matches = flann.knnMatch(des1,des2,k=2)

	
	good = 0
	for m,n in matches:
    		if m.distance < 0.7*n.distance:
		        good += 1

	if good>MIN_MATCH_COUNT:
		return True
	else:
		return False 

	# Need to draw only good matches, so create a mask
	#matchesMask = [[0,0] for i in xrange(len(matches))]

	# ratio test as per Lowe's paper
	#for i,(m,n) in enumerate(matches):
	#    if m.distance < 0.7*n.distance:
	#        matchesMask[i]=[1,0]

	#draw_params = dict(matchColor = (0,255,0),
	#                   singlePointColor = (255,0,0),
	#                   matchesMask = matchesMask,
	#                   flags = 0)

	#img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

	#cv2.imwrite('sift_keypoints.jpg',img3)

def main():
	init()
	computeKeyPoints()
	#test()
	#compute()


if __name__ == '__main__':
	main()
