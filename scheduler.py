import json
import getposts as gp
import decimal

def main():
	data = {}
	with open('data.json') as datafile:    
		data = json.load(datafile)
	for key in data:
		for item in data:
			posts = gp.input_filter(gp.get_posts(GROUP), item[0], decimal.Decimal(item[1]))
			#SEND EMAIL

if __name__ == "__main__":
	main()
