from flask import Flask, render_template, redirect, abort, request
from requests import get, post, delete, put
from authors_secrets import SECRET_KEY, LOAD_DATA  # Файл доступ к которому имеет только создатель проекта
import authors_secrets
from random import choices, randint, choice, uniform
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import *
from data.products import *
from data.cards import *
from data.users_resources import *
from data.products_resources import *
from data.cards_resources import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

api.add_resource(CardListResource, '/api/cards')
api.add_resource(CardResource, '/api/cards/<int:card_id>')

api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:product_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def load_data():
    """
    Функция которая создаёт базу данных <db/base.db> если её не существует.
    :return: Переводит пользователя на страницу [/main/]
    """
    LOAD_DATA()
    return redirect("/main/")


@app.route("/main/")
def main():
    """
    Главная страница магазина со всеми товарами
    :return:
    """

    global_init("db/base.db")



    return render_template("main.html")


app.run(port=5000, host='127.0.0.1')
