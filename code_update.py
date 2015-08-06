from pymongo import MongoClient
# Updates a specific tweet and its retweets with a code

dbclient = MongoClient('z')

db = None
db1 = 'baltimore'
db2 = 'rumor_compression'

collection = 'purse'

# Connects to a specific db and collection in Mongo
def db_connect(db, dbase, collection):
	db = dbclient[dbase][collection]
	print 'Connection Established'
	return db

db = db_connect(db, db2, collection)

# Grabs dictionary of tweet/retweet ids and puts them in a list
dct = list(db.find({'db_id':0},{'id':1 , '_id':0}))

lst = dct[0]['id']

db = db_connect(db, db1, collection)

# Sets new code
new_code = {"codes" : 
	[
		{
			"second_code" : [],
			"first_code" : "Deny",
			"rumor" : "purse"
		}
	],
}

query = {}

# Loops through list and finds all tweets/retweets and updates them
query['$or'] = [{'id': i} for i in lst]

db.update(query, { '$set': new_code}, upsert=False, multi=True)



