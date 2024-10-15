import os
from constant import IMAGE_FOLDER_NEWS

def get_image_path(news_id):
    """
    Constructs the file path for a news image based on the given news ID.

    :param news_id: The ID of the news item.
    :return: The full path to the image file as a string.
    """
    return os.path.join(IMAGE_FOLDER_NEWS, f"{news_id}.png")