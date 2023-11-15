from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class EditBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=710)])
    series = StringField('Series', validators=[Length(min=1, max=710)])
    author = StringField('Author', validators=[DataRequired(), Length(min=1, max=710)])
    description = StringField('Description', validators=[Length(min=1, max=710)])
    language_1 = StringField('Available book language', validators=[Length(min=1, max=710)])
    language_2 = StringField('Available book language', validators=[Length(min=1, max=710)])
    language_3 = StringField('Available book language', validators=[Length(min=1, max=710)])
    language_4 = StringField('Available book language', validators=[Length(min=1, max=710)])
    language_5 = StringField('Available book language', validators=[Length(min=1, max=710)])
    pages = IntegerField('Pages')
    publisher = StringField('Publisher', validators=[Length(min=1, max=710)])
    publishDate = StringField('Publish Date', validators=[Length(min=1, max=710)])
    coverImg = StringField('Cover Image', validators=[Length(min=1, max=710)])
    price = FloatField('Price', validators=[DataRequired(), Length(min=1, max=710)])
