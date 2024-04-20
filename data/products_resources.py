from flask_restful import reqparse, abort, Resource
from flask import abort, jsonify
from data.db_session import create_session
from data.products import Product


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('seller', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('count', required=True, type=int)
parser.add_argument('is_limited', required=True, type=bool)
parser.add_argument('asks', required=True)
parser.add_argument('reviews', required=True)

PRODUCTS_CHARACTERISTICS: list[str] = "id title description seller price count is_limited asks reviews".split()


def abort_if_user_not_found(product_id):
    session = create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")


class ProductResource(Resource):
    def get(self, product_id):
        abort_if_user_not_found(product_id)
        session = create_session()
        product = session.query(Product).get(product_id)
        return jsonify({'product': product.to_dict(only=tuple(PRODUCTS_CHARACTERISTICS))})

    def delete(self, product_id):
        abort_if_user_not_found(product_id)
        session = create_session()
        product = session.query(Product).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, product_id):
        abort_if_user_not_found(product_id)
        data = parser.parse_args()
        session = create_session()
        product = session.query(Product).get(product_id)
        product.title = data["title"]
        product.description = data["description"]
        product.seller = data["seller"]
        product.price = data["price"]
        product.count = data["count"]
        product.is_limited = data["is_limited"]
        product.asks = data["asks"]
        product.reviews = data["reviews"]
        session.commit()
        return jsonify({'id': product.id})


class ProductListResource(Resource):
    def get(self):
        session = create_session()
        product = session.query(Product).all()
        return jsonify({'product': [item.to_dict(only=tuple(PRODUCTS_CHARACTERISTICS)) for item in product]})

    def post(self):
        data = parser.parse_args()
        session = create_session()
        product = Product()
        product.title = data["title"]
        product.description = data["description"]
        product.seller = data["seller"]
        product.price = data["price"]
        product.count = data["count"]
        product.is_limited = data["is_limited"]
        product.asks = data["asks"]
        product.reviews = data["review"]
        session.add(product)
        session.commit()
        return jsonify({'id': product.id})
