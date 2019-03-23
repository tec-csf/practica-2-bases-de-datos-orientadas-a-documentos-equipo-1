from flask import Flask, render_template, redirect
from pymongo import MongoClient
from classes import *

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='Practica2Team1'))
client = MongoClient('mongodb://mgcoello:Tovjip-wekqyx-xefbu3@advanceddatabases-shard-00-00-xn5qi.azure.mongodb.net:27017,advanceddatabases-shard-00-01-xn5qi.azure.mongodb.net:27017,advanceddatabases-shard-00-02-xn5qi.azure.mongodb.net:27017/test?ssl=true&replicaSet=AdvancedDatabases-shard-0&authSource=admin&retryWrites=true')
db = client.LostDogs

def createDog(form):
    Fur_color = form.fur_color.data
    Name = form.name.data
    Gender = form.gender.data
    Breed = form.breed.data
    
    dog = { 'fur_color':Fur_color, 'name':Name, 'gender':Gender, 'breed':Breed}

    db.Dogs.insert_one(dog)
    return redirect('/')

@app.route('/', methods=['GET','POST'])
def main():
    # create form
    cform = CreateDog(prefix='cform')

    # response
    if cform.validate_on_submit() and cform.create.data:
        return createDog(cform)

    # read all data
    #dogs = db.Dogs.find().limit(10)
    pipeline = [{'$group':{'_id':'$breed', 'total':{'$sum':1}, 'male':{'$sum':{'$cond':[{'$eq':['male', '$gender']}, 1, 0]}}, 'female':{'$sum':{'$cond':[{'$eq':['female', '$gender']}, 1, 0]}}}}]
    cursor = db.Dogs.aggregate(pipeline)
    dogs = list(cursor)
    data = []
    for i in dogs:
        data.append(i)

    pipeline1 = [{'$lookup':{'from':'owners', 'localField':'ownerID', 'foreignField':'ownerID', 'as': 'owner'}}, {'$project':{'_id':0, 'name':1, 'gender':1, 'breed':1, 'ownerName':{'$reduce':{'input':'$owner.name', 'initialValue':'', 'in':{'$concat':['$$value', '$$this']}}}, 'ownerPhone':{'$reduce':{'input':'$owner.phone', 'initialValue':'', 'in':{'$concat':['$$value', '$$this']}}},'address':{'$reduce':{'input':'$owner.address', 'initialValue':'', 'in': {'$concat':['$$value', '$$this']}}}}}]
    cursor1 = db.Dogs.aggregate(pipeline1)
    dogs1 = list(cursor1)
    data1 = []
    count = 0
    for i in dogs1:
        count = count + 1
        if(count>20):
            break
        data1.append(i)

    pipeline2 = [{'$lookup':{'from':'dogs', 'localField':'breed', 'foreignField':'breed', 'as':'possibleMatch'}}, {'$project': {'_id': 0, 'lostDogID':1, 'furColor':1, 'gender':1, 'breed':1, 'dateFound':1, 'possibleMatch':{'$filter':{'input':'$possibleMatch', 'as': 'matchD', 'cond': {'$and':[{'$eq':['$$matchD.gender', '$gender']}, {'$eq':['$$matchD.furColor', '$furColor']}]} }}}}, {'$project':{'lostDogID':1, 'furColor':1, 'gender':1, 'breed':1, 'dateFound':1, 'possibleMatch':{'$map':{'input':'$possibleMatch', 'as':'p', 'in':{'owner':'$$p.ownerID', 'dogName':'$$p.name'}}}}}]
    cursor2 = db.LostDogos.aggregate(pipeline2)
    dogs2 = list(cursor2)
    data2 = []
    count1 = 0
    for i in dogs2:
        count1 = count1 + 1
        if(count1>20):
            break
        data2.append(i)

    return render_template('home.html', cform = cform, \
            data = data, data1=data1, data2=data2)

if __name__=='__main__':
    app.run(debug=True)
