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

EMAIL_HISTORY_PATH = "http://localhost:8501/email_history"

MAIN_PAGE_MODEL = "main_page"

NEWS_BLOCK_MODEL = "news_block"

FONT_FAMILY_MAIN_PAGE = "font-family: Arial, Helvetica, sans-serif;"

LINE_HEIGHT_MAIN_PAGE = "line-height: 1.5;"

FONT_FAMILY_NEWS_BLOCK = "font-family: Arial, Helvetica, sans-serif;"

LINE_HEIGHT_NEWS_BLOCK = "line-height: 1.5;"

