from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import Length

class FilterBookForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=0, max=710)])
    author = StringField('Author', validators=[Length(min=0, max=710)])
    language_1 = StringField('Language 1 available', validators=[Length(min=0, max=710)])
    language_2 = StringField('Language 2 available', validators=[Length(min=0, max=710)])
    language_3 = StringField('Language 3 available', validators=[Length(min=0, max=710)])
    language_4 = StringField('Language 4 available', validators=[Length(min=0, max=710)])
    language_5 = StringField('Language 5 available', validators=[Length(min=0, max=710)])
    price = FloatField('Price', validators=[Length(min=0, max=710)])