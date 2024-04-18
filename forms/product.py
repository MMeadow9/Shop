from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class ProductCreate(FlaskForm):
    title = StringField("Название товара")
    description = StringField("Описание товара")
    price = IntegerField("Цена товара")
    count = IntegerField("Кол-во товара")
    is_limited = BooleanField("Ограничено ли кол-во товара")
    submit = SubmitField('Войти')


class ProductEdit(FlaskForm):
    title = StringField("Название товара")
    description = StringField("Описание товара")
    price = IntegerField("Цена товара")
    count = IntegerField("Кол-во товара")
    is_limited = BooleanField("Ограничено ли кол-во товара")
    submit = SubmitField('Изменить')
