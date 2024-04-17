from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField("Имя")
    surname = StringField("Фамилия")
    email = EmailField("Эл. почта")
    phone_number = StringField("Номер телефона")
    password = PasswordField("Пароль")
    password_again = PasswordField("Ещё раз пароль")
    card_number = StringField("Номер карты")
    card_term = StringField("Срок карты")
    card_code = StringField("Код карты")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email_phone = EmailField('Почта или Номер телефона', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
