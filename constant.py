import os
from dotenv import load_dotenv

load_dotenv()

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "nikan2110isr@gmail.com"
smtp_password = os.getenv('SMTP_PASSWORD')

postgres_password = os.getenv('POSTGRES_PASSWORD')

IMAGE_FOLDER = "news_images"

