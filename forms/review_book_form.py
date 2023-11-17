from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import Length

class ReviewBookForm(FlaskForm):
    rating = SelectField(
        u'Rating the book',
        choices = [(1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Average'), (4, '4 - Good'), (5, '5 - Excellent')]
    )
    review = TextAreaField(u'Review', validators=[Length(max=1000)])