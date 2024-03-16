from flask import Flask, render_template, redirect, abort, request
from data.db_session import global_init, create_session
from data.card import *
from data.user import *
from data.product import *
from data.db_session import *
import os
from forms.user import *
from forms.product import *
from wtforms import Label
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from random import randint, choices, choice
from werkzeug.security import generate_password_hash


def get_random_number(number):
    return str(randint(0, int("9" * number))).rjust(number, "0")


cashs = [1] * 10000 + [2] * 5000 + [5] * 2000 + [10] * 1000 + [20] * 500 + [25] * 400 + [50] * 200 + [100] * 100 + [250] * 40 + [500] * 20 + [1000] * 10 + [2000] * 5 + [5000] * 2 + [10000]

users = [
    ["Марианна", "Владимирова", "Marianna_Vl@yandex.ru", "+7 (356) 772 99 54", "1", "", "", 1],
    ["Михаил", "Воронцов", "Michail_Crow@yandex.ru", "+7 (915) 129 91 63", "2", "", "", 2],
    ["Андрей", "Нечаев", "Andrey_Nechaev@yandex.ru", "+7 (384) 002 55 06", "3", "", "", 3],
    ["Александра", "Бирюкова", "Alex_Biryukova@yandex.ru", "+7 (783) 736 65 07", "4", "", "", 4],
    ["Лия", "Филиппова", "Leah_Filipp@yandex.ru", "+7 (486) 695 65 50", "5", "", "", 5]
]

products = [
    ["Смартфон Pova 5 Pro", "Диагональ экрана дюймы: 6.8, Емкость аккумулятора мАч: 5000", 1, 8000, 4, True],
    ["Спички", "Просто коробок спичек", 2, 5, 0, False],
    ["Набор линеек", "Набор прозрачных зелёных линеек, обычная линейка, 2 угольника, транспортир", 3, 600, 2, True],
    ["Глобус", "Глобус с диаметром 40см", 3, 1150, 1, True]
]

cards = [
    [get_random_number(16), get_random_number(4), get_random_number(3), 5000, "Usual"],
    [get_random_number(16), get_random_number(4), get_random_number(3), 1000, "Usual"],
    [get_random_number(16), get_random_number(4), get_random_number(3), 50000, "Silver"],
    [get_random_number(16), get_random_number(4), get_random_number(3), 50, "Usual"],
    [get_random_number(16), get_random_number(4), get_random_number(3), 450000, "Platinum"]
]

app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(choices("0123456789ABCDEFabcdef", k=randint(10, 15)))

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


def load_data():
    if os.path.isfile("db/blogs.db"):
        return
    global_init("db/blogs.db")

    db_sess = create_session()

    for data in users:
        user = User()

        user.name = data[0]
        user.surname = data[1]
        user.email = data[2]
        user.phone_number = data[3]
        user.hashed_password = generate_password_hash(data[4])
        user.products = data[5]
        user.sold_products = data[6]
        user.card = data[7]

        db_sess.add(user)

    for data in products:
        product = Product()

        product.title = data[0]
        product.description = data[1]
        product.seller = data[2]
        product.price = data[3]
        product.count = data[4]
        product.is_limited = data[5]

        db_sess.add(product)

    for data in cards:
        card = Card()

        card.number = data[0]
        card.term = data[1]
        card.code = data[2]
        card.cash = data[3]
        card.status = data[4]

        db_sess.add(card)

    db_sess.commit()


load_data()


@app.route("/")
def main():
    global_init("db/blogs.db")

    db_sess = create_session()

    data = []

    for product in db_sess.query(Product).all():
        seller = db_sess.query(User).filter(User.id == product.seller).first()
        data.append(
            [
                product.id,
                product.title,
                product.description,
                f"{seller.name} {seller.surname}",
                product.price,
                product.count,
                product.is_limited
            ]
        )

    card = 0

    if current_user.is_authenticated:
        card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    return render_template('main.html', data=data, card=card)


@app.route("/reg", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        user.card = len(db_sess.query(Card).all()) + 1
        user.products = user.sold_products = ""

        user.set_password(form.password.data)
        db_sess.add(user)

        card = Card()
        card.number = form.card_number.data
        card.term = form.card_term.data
        card.code = form.card_code.data
        card.cash = 0
        card.status = "Usual"

        db_sess.add(card)

        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
@app.route('/log', methods=['GET', 'POST'])
@app.route('/authorization', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter((User.email == form.email_phone.data) |
                                          (User.phone_number == form.email_phone.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/view_advertisement")
def view_advertisement():
    global_init("db/blogs.db")

    db_sess = create_session()

    cash = choice(cashs)
    db_sess.query(Card).filter(Card.id == current_user.card).first().cash += cash

    db_sess.commit()

    return redirect("/")


print(sum(cashs) / len(cashs))


if __name__ == '__main__':
    app.run(port=8880, host='127.0.0.1')
