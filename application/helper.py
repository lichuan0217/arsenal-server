

# Convert model Items to python list
def convert_items_to_list(objects):
    articals = list()
    for obj in objects:
        item = dict()
        item['header'] = obj.card_header
        item['content'] = obj.card_content
        item['thumbnail'] = obj.card_small_photo
        item['source'] = obj.card_src
        item['fullTextUrl'] = obj.full_text_url
        item['articleId'] = obj.artical_id
        articals.append(item)
    return articals


# Convert model Artical to python dict
def convert_artical_to_dict(src, isFavorite):
    article = dict()
    article['header'] = src.artical_title
    article['picture_src'] = src.artical_important_pic
    article['content'] = src.artical_main_content
    article['date'] = src.artical_date
    article['editor'] = src.artical_editor
    article['source'] = src.artical_src
    article['type'] = src.artical_type
    article['video'] = src.artical_video_play
    article['favorite'] = isFavorite
    return article
