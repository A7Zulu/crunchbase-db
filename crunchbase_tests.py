# Crunchbase API Tests
from crunchbase import crunchbase


def main():
	cb = crunchbase()
	json = cb.loadJSON("/company/whistle")
	imageURL = cb.getImageURL(json)
	image = cb.getImage(imageURL)


if __name__ == '__main__':
	main()
