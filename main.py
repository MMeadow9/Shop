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
from forms.product import ProductCreate as FormProductCreate, ProductEdit as FormProductEdit
from forms.users import RegisterForm as FormRegister, LoginForm as FormLogin


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def main():
    """
    Главная страница магазина со всеми товарами
    :return:
    """

    data = []
    for product in get("http://127.0.0.1:5000/api/products").json()["product"]:
        seller: dict = get(f"http://127.0.0.1:5000/api/users/{product['seller']}").json()["user"]
        data.append([product["id"], product["title"], product["description"], f"{seller['name']} {seller['surname']}", product["price"], product["count"], product["is_limited"]])

    db_sess = create_session()

    card = 0

    if current_user.is_authenticated:
        card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    db_sess = create_session()

    current_user_id = current_user.id
    ids_sold_products = [product.id for product in db_sess.query(Product).filter(Product.seller == current_user_id)]

    print(ids_sold_products)

    return render_template('main.html', data=data, card=card, isd=ids_sold_products)


@app.route("/reg", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def reg():
    """
    Страница с формой для регистрации
    :return:
    """
    form = FormRegister()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")

        users = get(f"http://127.0.0.1:5000/api/users").json()["user"]
        phone_numbers = [user["phone_number"] for user in users]
        emails = [user["email"] for user in users]
        if form.email.data in emails or form.phone_number.data in phone_numbers:
            return render_template('register.html', form=form, message="Пользователь с такой почтой или номером телефона уже есть.")

        db_sess = create_session()

        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        user.products = user.sold_products = ""

        user.set_password(form.password.data)

        card = Card()
        card.number = form.card_number.data
        card.term = form.card_term.data
        card.code = form.card_code.data
        card.cash = 0
        card.status = "Usual"
        card.status = "1"

        user.card = card.id

        db_sess.add(user)
        db_sess.add(card)

        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route("/log", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route('/authorization', methods=['GET', 'POST'])
def login():
    form = FormLogin()
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
    return render_template('login.html', form=form)


@app.route("/create_product", methods=["GET", "POST"])
@app.route("/product_create", methods=["GET", "POST"])
def create_product():
    form = FormProductCreate()
    if form.validate_on_submit():
        db_sess = create_session()
        product = Product()
        product.title = form.title.data
        product.description = form.description.data
        product.seller = current_user.id
        product.price = form.price.data
        product.count = form.count.data
        product.is_limited = form.is_limited.data
        db_sess.add(product)
        db_sess.commit()
        return redirect('/')
    return render_template('products_create.html', form=form)


@login_required
@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
@app.route("/product_edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    form = FormProductEdit()
    if request.method == "GET":

        db_sess = create_session()
        product = db_sess.query(Product).filter(Product.id == id, Product.seller == current_user.id).first()
        if product:
            form.title.data = product.title
            form.description.data = product.description
            form.price.data = product.price
            form.count.data = product.count
            form.is_limited.data = product.is_limited
        else:
             return "Кажется, у вас нет прав изменять этот товар..."
    if form.validate_on_submit():
        db_sess = create_session()
        product = db_sess.query(Product).filter(Product.id == id, Product.seller == current_user.id).first()
        if product:
            product.title = form.title.data
            product.description = form.description.data
            product.seller = current_user.id
            product.price = form.price.data
            product.count = form.count.data
            product.is_limited = form.is_limited.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)

    return render_template('products_edit.html', form=form)


global_init("db/base.db")

LOAD_DATA()

app.run(port=5000, host='127.0.0.1', debug=True)
