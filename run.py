from flask import Flask, render_template, redirect
from pymongo import MongoClient
from classes import *

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='Practica2Team1'))
client = MongoClient("mongodb://mgcoello:Tovjip-wekqyx-xefbu3@advanceddatabases-shard-00-00-xn5qi.azure.mongodb.net:27017,advanceddatabases-shard-00-01-xn5qi.azure.mongodb.net:27017,advanceddatabases-shard-00-02-xn5qi.azure.mongodb.net:27017/test?ssl=true&replicaSet=AdvancedDatabases-shard-0&authSource=admin&retryWrites=true")
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
    docs = db.Dogs.find().limit(10)
    data = []
    for i in docs:
        data.append(i)

    return render_template('home.html', cform = cform, \
            data = data)

if __name__=='__main__':
    app.run(debug=True)
