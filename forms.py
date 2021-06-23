from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


# WTForm
class GenerateQrForm(FlaskForm):
    data_entry = StringField("data", validators=[DataRequired(message=u'Enter some text to encode.')])
    submit = SubmitField("Generate QR")

