import json
import getposts as gp
import decimal
#import emails as e

GROUP = '266259930135554' #Berkeley Free & For Sale

def main():
	data = {}
	with open('data.json') as datafile:    
		data = json.load(datafile)
	for key in data:
		print key
		item_dict = {}
		for item in data[key]:
			message_id = []
			posts = gp.input_filter(gp.get_posts(GROUP), item[0], decimal.Decimal(item[1]))
			for post in posts:
				message_id.append(post['id'])
			item_dict[item[0]] = message_id
		print item_dict
		#e.send(key, item_dict)

if __name__ == "__main__":
	main()
