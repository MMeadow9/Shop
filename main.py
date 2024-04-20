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

    current_user_id = current_user.id if current_user.is_authenticated else -1
    ids_sold_products = [product.id for product in db_sess.query(Product).filter(Product.seller == current_user_id)]

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
def edit_product(id: int):
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


@login_required
@app.route("/view_advertisement")
def advertisement():
    added_cash = choice([1, 2, 3, 5, 10, 25]) * (10 ** choice([1, 1, 1, 2, 2, 3]))

    db_sess = create_session()

    if current_user.is_authenticated:
        card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    card.cash += int(added_cash * (1 + {"U": 0, "B": 0, "S": 0.05, "G": 0.15, "P": 0.3}[card.status[0]]))

    db_sess.commit()

    return redirect("/")


@login_required
@app.route("/buy_product/<int:product_id>/<int:count>")
def buy_product(product_id: int, count: int):
    """
    :param product_id: ID товара для покупки
    :param count:      Количество покупаемого товара
    :return:
    """
    db_sess = create_session()
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    price = product.price
    title = product.title

    card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    message = ""  # Сообщение для пользователя
    ok = None  # Флаг, если он принимает значение True, значит пользователь может купить товар(ы), если False - не может

    if product.seller == current_user.id:  # Если пользователь пытается купить свой же товар
        message = "Нельзя покупать свой товар."
        ok = False
    elif product.is_limited and product.count < count:  # Если кол-во товаров ограничено и пользователь хочет больше чем есть
        message = f"У нас в наличии лишь {product.count} \"{title}\"."
        ok = False
    elif price * count > card.cash:  # Если у пользователя не хватает денег на покупку
        message = "У Вас недостаточно денег на покупку всего этого."
        ok = False
    else:  # А если пользователь всё же может купить товар(ы), то спросим у него повторно хочет ли он сделать это
        message = f"Вы действительно хотите купить {count} шт.  товара \"{title}\" за {price * count}₽ ?"
        ok = True

    link = f"/buy/{product_id}/{count}"

    return render_template("buying.html", message=message, ok=ok, card=card, link=link)

@login_required
@app.route("/buy/<int:product_id>/<int:count>")
def buy(product_id: int, count: int):
    db_sess = create_session()
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    seller = product.seller
    price = product.price
    products = current_user.products
    dict_p = {int(product_.split(":")[0]): int(product_.split(":")[1]) for product_ in products.replace(" ", "").split(",") if products} # Словарь продуктов

    card.cash -= int(count * price * (1 - {"U": 0, "B": 0.03, "S": 0.08, "G": 0.13, "P": 0.2}[card.status[0]]))
    sellers_card = db_sess.query(Card).filter(Card.id == seller).first()
    sellers_card.cash += count * price

    product.count -= count

    dict_p[product_id] = dict_p.get(product_id, 0) + count

    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.products = str(dict_p)[1:][:-1]

    db_sess.commit()

    return redirect("/")


@login_required
@app.route("/card/<int:card_number>")
def card(card_number):
    db_sess = create_session()
    card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    return render_template("cards.html", card=card, card_number=card_number)


@login_required
@app.route("/use_card/<int:card_number>")
def use_card(card_number):
    db_sess = create_session()
    card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    if str(card_number) in card.statuses:
        card.status = {index + 1: type for index, type in enumerate("Usual Black Silver Gold Platinum".split())}[card_number]
        db_sess.commit()
        return redirect(f"/card/{card_number}")
    else:
        return render_template("error_other.html", message="Вы не можете использовать карту которой у Вас нет.")


@login_required
@app.route("/buy_card/<int:card_number>")
def buy_card(card_number):
    db_sess = create_session()
    card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    if card_number not in [1, 2, 3, 4, 5]:
        return render_template("error_other.html", message="Вы не можете купить несуществующую карту.")
    elif str(card_number) in card.statuses:
        return render_template("error_other.html", message="Вы не можете купить уже имеющуюся карту.")
    else:
        card_price = {1: 0, 2: 250, 3: 800, 4: 1950, 5: 3500}[card_number]

        if card_price > card.cash:
            return render_template("error_other.html", message="У Вас не хватает денег на эту карту.")
        else:
            card.statuses += str(card_number)
            card.cash -= card_price
            db_sess.commit()
            return redirect(f"/card/{card_number}")


@login_required
@app.route("/products")
def products():
    db_sess = create_session()

    card = db_sess.query(Card).filter(Card.id == current_user.card).first()

    products_ = current_user.products
    dict_p = {int(product_.split(":")[0]): int(product_.split(":")[1]) for product_ in
              products_.replace(" ", "").split(",") if products_}  # Словарь продуктов

    data = []
    for product in get("http://127.0.0.1:5000/api/products").json()["product"]:
        if product["id"] in dict_p.keys():
            seller: dict = get(f"http://127.0.0.1:5000/api/users/{product['seller']}").json()["user"]

            data.append([product["id"], product["title"], product["description"], f"{seller['name']} {seller['surname']}",
                         product["price"], dict_p[product["id"]]])

    return render_template("products.html", data=data, card=card, dict_p=dict_p)



@app.errorhandler(404)
def not_found(error):
    return render_template("error_404.html")


global_init("db/base.db")

LOAD_DATA()

app.run(port=5000, host='127.0.0.1', debug=True)
