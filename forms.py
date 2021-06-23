from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


# WTForm
class GenerateQrForm(FlaskForm):
    data_entry = StringField("Enter text to encode:", validators=[DataRequired(u'Enter text to encode'),
                                                                  Length(min=1, max=200)])
    submit = SubmitField("Generate QR")
