from application import db

class Item(db.Document):
	card_content = db.StringField(max_length=255, required=True)
	card_small_photo = db.URLField()
	card_header = db.StringField(max_length=255)
	full_text_url = db.URLField()
	card_src = db.StringField(max_length=100)
	artical_id = db.StringField(max_length=20)

	def __str__(self):
		return {'header' : self.card_header,
				'data_image' : self.card_small_photo,
				'content' : self.card_content}



class Artical(db.Document):
	artical_main_content = db.StringField(max_length=255, required=True)
	artical_important_pic = db.URLField()
	artical_title = db.StringField(max_length=255)
	artical_date = db.StringField()
	artical_editor = db.StringField()
	artical_src = db.StringField(max_length=100)
	artical_id = db.StringField(max_length=20)
