import decimal
import json

def validPrice(price):
	try:
		float(price)
	except ValueError:
		print 'Price is not a number'
		return False
	if float(price) < 0:
		print 'Negative price not allowed'
		return False
	return True

def remove_item():
	print "REMOVE ITEM\n"
	email = raw_input('What is your email? ')

	#Get dictionary
	with open('data.json') as datafile:    
		data = json.load(datafile)
	if email in data:
		curr = data[email]
		items = [i[0] for i in curr]
		item = raw_input("What item would you like removed? ").lower()
		if item in items:
			index = items.index(item)
			del curr[index]
			data[email] = curr
		
			#Save dictionary
			with open('data.json', 'w') as savefile:
				json.dump(data, savefile, indent=4, separators=(',', ':'))
			print "Item removed!"

		else:
			print "Item not found"
			return
	else:
		print "Email not found"

def add_item():
	item = raw_input('What item are you searching for? ').lower()
	price = raw_input('Max price? Write 0 if you do not have one. ')
	if not validPrice(price):
		print 'Price not valid'
		return
	email = raw_input('What is your email address? ')

	#Get dictionary
	with open('data.json') as datafile:    
		data = json.load(datafile)

	request = (item, price)
	if not email in data:
		data[email] = []
	curr = data[email]
	if not item in curr:
		curr.append(request)
		data[email] = curr

	#Save dictionary
	with open('data.json', 'w') as savefile:
		json.dump(data, savefile, indent=4, separators=(',', ':'))
	print "Item added!"

def main():
	add_item();
	add_item();
if __name__ == "__main__":
	main()
