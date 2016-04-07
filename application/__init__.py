from flask import Flask
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
        item['goto'] = obj.full_text_url
        item['articalid'] = obj.artical_id
        articals.append(item)
    return articals

def convert_artical(src):
    ret = dict()
    ret['header'] = src.artical_title
    ret['picture_src'] = src.artical_important_pic
    ret['content'] = src.artical_main_content
    ret['date'] = src.artical_date
    ret['editor'] = src.artical_editor
    ret['source'] = src.artical_src
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
    articals = convert(Item.objects[start: end])
    return dumps(articals)


@app.route("/arsenal/artical/<string:id>/")
def artical(id):
    from models import Artical
    artical = Artical.objects(artical_id=id).get()
    return dumps(convert_artical(artical))
