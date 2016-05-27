from flask import Flask, jsonify, abort, make_response, request
from flask.ext.mongoengine import MongoEngine
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "arsenal"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

PAGE_SIZE = 30

db = MongoEngine(app)


def convert(objects):
    articals = list()
    for obj in objects:
        item = dict()
        item['header'] = obj.card_header
        item['content'] = obj.card_content
        item['thumbnail'] = obj.card_small_photo
        item['source'] = obj.card_src
        item['fullTextUrl'] = obj.full_text_url
        item['articalId'] = obj.artical_id
        articals.append(item)
    return articals


def convert_artical(src, isFavorite):
    ret = dict()
    ret['header'] = src.artical_title
    ret['picture_src'] = src.artical_important_pic
    ret['content'] = src.artical_main_content
    ret['date'] = src.artical_date
    ret['editor'] = src.artical_editor
    ret['source'] = src.artical_src
    ret['type'] = src.artical_type
    ret['video'] = src.artical_video_play
    ret['favorite'] = isFavorite
    return ret


@app.route("/")
def index():
    return "This is for Arsenal Fans!!!"


@app.route("/arsenal/item/")
@app.route("/arsenal/item/<int:page>/")
def item(page=0):
    from models import Item
    start = page * PAGE_SIZE
    end = (page + 1) * PAGE_SIZE
    articals = convert(Item.objects.order_by('-artical_id')[start:end])
    return dumps(articals)


@app.route("/arsenal/artical/<string:id>/", methods=['GET'])
def artical(id):
    from models import Artical
    artical = Artical.objects(artical_id=id).get()
    return dumps(convert_artical(artical, False))


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
            return dumps(convert_artical(article, True))
    return dumps(convert_artical(article, False))


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
    from models import Favorite
    favorite = Favorite.objects(user_id=id).get()
    return jsonify({"favorite": favorite})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(
        {'response_msg': 'Not Found', 'response_code': 404}
        ), 404)


@app.errorhandler(400)
def error_request(error):
    return make_response(jsonify(
        {'response_msg': 'Bad Request', 'response_code': 400}
        ), 400)


@app.route("/arsenal/spider/")
def spider():
    pass
