import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

IMAGE_FOLDER_NEWS = "static/news_images"

IMAGE_PREVIEW_PATH = "http://localhost:8501/app/static"

MAIN_PAGE_MODEL = "main_page"

NEWS_BLOCK_MODEL = "news_block"

