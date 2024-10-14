import os

from constant import IMAGE_FOLDER


def get_image_path(news_id):
    return os.path.join(IMAGE_FOLDER, f"{news_id}.png")
