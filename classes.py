from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SubmitField

class CreateDog(FlaskForm):
    fur_color = TextField('Fur Color')
    name = TextField('Name')
    gender = TextField('Gender')
    breed = TextField('Breed')
    create = SubmitField('Create')