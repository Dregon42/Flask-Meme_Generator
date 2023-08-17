from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Meme, meme_schema, memes_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/memes', methods=['POST'])
@token_required
def create_meme(current_user_token):
    quote = request.json['quote']
    image = request.json['image']
    user = User.query.get(current_user_token.id)

    meme = Meme(quote=quote, image=image, user_id=user.id)

    db.session.add(meme)
    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route('/memes', methods = ['GET'])
@token_required
def get_meme(current_user_token):
    a_user = current_user_token.token
    memes = Meme.query.filter_by(user_token = a_user).all()
    response = memes_schema.dump(memes)
    return jsonify(response)

@api.route('/memes/<id>', methods = ['GET'])
@token_required
def get_single_meme(current_user_token, id):
    meme = Meme.query.get(id)
    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route('/memes/<id>', methods = ['POST','PUT'])
@token_required
def update_meme(current_user_token,id):
    meme = Meme.query.get(id) 
    meme.quote = request.json['quote']
    meme.image = request.json['image']
    meme.user_token = current_user_token.token

    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route('/memes/<id>', methods = ['DELETE'])
@token_required
def delete_meme(current_user_token, id):
    meme = Meme.query.get(id)
    db.session.delete(meme)
    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)