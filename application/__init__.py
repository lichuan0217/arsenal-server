from flask import Flask, jsonify, abort, make_response, request
from flask.ext.mongoengine import MongoEngine
from bson.json_util import dumps
from helper import convert_artical_to_dict, convert_items_to_list
import subprocess

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "arsenal"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

PAGE_SIZE = 30
db = MongoEngine(app)


@app.route("/")
def index():
    return "This is for Arsenal Fans!!!"


@app.route("/arsenal/item/")
@app.route("/arsenal/item/<int:page>/")
def item(page=0):
    from models import Item
    start = page * PAGE_SIZE
    end = (page + 1) * PAGE_SIZE
    articals = convert_items_to_list(Item.objects.order_by('-artical_id')[
        start:end])
    return dumps(articals)


@app.route("/arsenal/artical/<string:id>/", methods=['GET'])
def artical(id):
    from models import Artical
    artical = Artical.objects(artical_id=id).get()
    return dumps(convert_artical_to_dict(artical, False))


@app.route("/arsenal/artical/<string:article_id>/", methods=['POST'])
def article_with_user(article_id):
    if not request.json:
        abort(400)
    if not 'user_id' in request.json:
        abort(400)
    user_id = request.json['user_id']
    from models import Artical, Favorite
    article = Artical.objects(artical_id=article_id).get()
    obj = Favorite.objects(user_id=user_id)
    if obj:
        favorite = obj.get()
        article_list = favorite.article_list
        if article_id in article_list:
            return dumps(convert_artical_to_dict(article, True))
    return dumps(convert_artical_to_dict(article, False))


@app.route("/arsenal/favorites/", methods=['POST'])
def post_favorite():
    if not request.json or not 'user_id' in request.json or not 'article_id' in request.json:
        abort(400)
    user_id = request.json['user_id']
    article_id = request.json['article_id']
    from models import Favorite
    obj = Favorite.objects(user_id=user_id)
    if obj:
        favorite = obj.get()
    else:
        favorite = Favorite(user_id=user_id)
    favorite.article_list.append(article_id)
    favorite.save()
    return jsonify({"response_msg": "success", "response_code": 201}), 201


@app.route("/arsenal/favorites/<string:id>/", methods=['GET'])
def get_favorite(id):
    from models import Favorite, Item
    favorite_items = []
    obj = Favorite.objects(user_id=id)
    if obj:
        favorite = obj.get()
        for article_id in favorite.article_list:
            item = Item.objects(artical_id=article_id).get()
            favorite_items.append(item)
    return dumps(convert_items_to_list(favorite_items))


@app.route("/arsenal/favorites/<string:user_id>/<string:article_id>/",
           methods=['DELETE'])
def del_favorite(user_id, article_id):
    from models import Favorite
    obj = Favorite.objects(user_id=user_id)
    if obj:
        favorite = obj.get()
        if article_id in favorite.article_list:
            obj.update_one(pull__article_list=article_id)
            return jsonify({"response_msg": "success",
                            "response_code": 200}), 200
    return jsonify({"response_msg": "Not Found", "response_code": 404}), 404


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'response_msg': 'Not Found',
                 'response_code': 404}), 404)


@app.errorhandler(400)
def error_request(error):
    return make_response(
        jsonify({'response_msg': 'Bad Request',
                 'response_code': 400}), 400)


@app.route("/arsenal/spider/")
def spider():
    rc = subprocess.call("bash application/spider.sh", shell=True)
    return str(rc)
