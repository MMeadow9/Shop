from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AskForm(FlaskForm):
    comment = StringField("Комментарий")
    submit = SubmitField("Отправить")
