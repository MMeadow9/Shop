from flask_restful import reqparse, abort, Resource
from flask import abort, jsonify
from data.db_session import create_session
from data.cards import Card


parser = reqparse.RequestParser()
parser.add_argument('number', required=True)
parser.add_argument('term', required=True)
parser.add_argument('code', required=True)
parser.add_argument('cash', required=True, type=int)
parser.add_argument('status', required=True)
parser.add_argument('statuses', required=True)

CARDS_CHARACTERISTICS: list[str] = "id number term code cash status statuses".split()


def abort_if_user_not_found(card_id):
    session = create_session()
    card = session.query(Card).get(card_id)
    if not card:
        abort(404, message=f"Card {card_id} not found")


class CardResource(Resource):
    def get(self, card_id):
        abort_if_user_not_found(card_id)
        session = create_session()
        card = session.query(Card).get(card_id)
        return jsonify({'card': card.to_dict(only=tuple(CARDS_CHARACTERISTICS))})

    def delete(self, card_id):
        abort_if_user_not_found(card_id)
        session = create_session()
        card = session.query(Card).get(card_id)
        session.delete(card)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, card_id):
        abort_if_user_not_found(card_id)
        data = parser.parse_args()
        session = create_session()
        card = session.query(Card).get(card_id)
        card.number = data["number"]
        card.term = data["term"]
        card.code = data["code"]
        card.cash = data["cash"]
        card.status = data["status"]
        card.statuses = data["statuses"]
        session.commit()
        return jsonify({'id': card.id})


class CardListResource(Resource):
    def get(self):
        session = create_session()
        card = session.query(Card).all()
        return jsonify({'card': [item.to_dict(only=tuple(CARDS_CHARACTERISTICS)) for item in card]})

    def post(self):
        data = parser.parse_args()
        session = create_session()
        card = Card()
        card.number = data["number"]
        card.term = data["term"]
        card.code = data["code"]
        card.cash = data["cash"]
        card.status = data["status"]
        card.statuses = data["statuses"]
        session.add(card)
        session.commit()
        return jsonify({'id': card.id})
