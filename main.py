from flask import Flask, render_template, redirect, abort, request
from requests import get, post, delete, put
from authors_secrets import SECRET_KEY, LOAD_DATA  # Файл доступ к которому имеет только создатель проекта
from random import choices, randint, choice, uniform
from flask_restful import Api
from data.users import *
from data.products import *
from data.cards import *
from data.users_resources import *
from data.products_resources import *
from data.cards_resources import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)

api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

api.add_resource(CardListResource, '/api/v2/cards')
api.add_resource(CardResource, '/api/cards/<int:card_id>')

api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:product_id>')


@app.route("/")
def load_data():
    """
    Функция которая создаёт базу данных <db/base.db> если её не существует.
    :return: Переводит пользователя на страницу [/main/]
    """
    LOAD_DATA()
    return redirect("/main/")


app.run(port=5000, host='127.0.0.1')
