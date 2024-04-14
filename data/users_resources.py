from flask_restful import reqparse, abort, Resource
from flask import abort, jsonify
from data.db_session import create_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('email', required=True)
parser.add_argument('phone_number', required=True)
parser.add_argument('password', required=True)
parser.add_argument('products', required=True)
parser.add_argument('sold_products', required=True)
parser.add_argument('card', required=True, type=int)


USERS_CHARACTERISTICS: list[str] = "id name surname email phone_number hashed_password products sold_products card".split()


def abort_if_user_not_found(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=tuple(USERS_CHARACTERISTICS))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        data = parser.parse_args()
        session = create_session()
        user = session.query(User).get(user_id)
        user.name = data["name"]
        user.surname = data["surname"]
        user.email = data["email"]
        user.phone_number = data["phone_number"]
        user.products = data["products"]
        user.sold_products = data["sold_products"]
        user.card = data["card"]
        user.set_password(data["password"])
        session.commit()
        return jsonify({'id': user.id})


class UserListResource(Resource):
    def get(self):
        session = create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(only=tuple(USERS_CHARACTERISTICS)) for item in user]})

    def post(self):
        data = parser.parse_args()
        session = create_session()
        user = User()
        user.name = data["name"]
        user.surname = data["surname"]
        user.email = data["email"]
        user.phone_number = data["phone_number"]
        user.products = data["products"]
        user.sold_products = data["sold_products"]
        user.card = data["card"]
        user.set_password(data["password"])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})
