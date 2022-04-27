import pymongo


client = pymongo.MongoClient('mongodb+srv://king20:kingshastri20@cluster0.ut1m1.mongodb.net/users?retryWrites=true&w=majority')

db = client.get_database('users')
col1 = db.get_collection('data')
col2 = db.get_collection('books')


def insert_user(name,passwd):
    data={
        'name':name,
        'password':passwd
    }

    col1.insert_one(data)

def insert_book(img,url):
    data={
         'img':img,
         'url':url
    }

    col2.insert_one(data)

def get_user():

    return col1.find()

def delete_user(name):
    col1.delete_one({'name':name})

def update_user(name,passw):
    old={
        'name':name
    }
    new={
        'password': passw
    }
    col1.update_one(old,{'$set':new})

def get_book():
    row = col2.find()
    imgs,urls = [],[]

    return row


def delete_book(img):
    col2.delete_one({'img':img})

