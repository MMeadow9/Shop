from flask_wtf import FlaskForm
from wtforms import IntegerField ,StringField, SubmitField


class ReviewForm(FlaskForm):
    comment = StringField("Комментарий")
    mark = IntegerField("Оценка товара (1 - 5)")
    submit = SubmitField("Отправить")
