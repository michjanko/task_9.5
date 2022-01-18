from turtle import title
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired

class CoinForm(FlaskForm):
    full_name = StringField('Nazwa', validators=[DataRequired()])
    short_name = StringField('Skrót', validators=[DataRequired()])
    price = FloatField('Cena', validators=[DataRequired()])
    amount = FloatField('Ilość', validators=[DataRequired()])
    description = TextAreaField('Opis')
    logo = TextAreaField('Link do logo')
    # id = TextAreaField('Opis', 5) najlepiej tu dodać automatyczne ID, ale nie wiem jak

