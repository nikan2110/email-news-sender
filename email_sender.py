import logging
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import server
from constant import smtp_user, smtp_password
from db import *
import psycopg2

from html_builder_email_main import generate_main_page, generate_news_block_html, make_html_for_email


def add_header_and_news_images_to_news_block(msg):
    news_ids = []
    with open("static/basic_images/header.jpg", 'rb') as img:
        mime_img = MIMEImage(img.read())
        mime_img.add_header('Content-ID', '<header_image>')
        mime_img.add_header('Content-Disposition', 'inline', filename="header")
        msg.attach(mime_img)

    for image_name in os.listdir("static/news_images"):
        if image_name.endswith('.png'):
            image_path = os.path.join("static/news_images", image_name)
            image_id = image_name.split('.')[0]

            news_ids.append(image_id)

            with open(image_path, 'rb') as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header('Content-ID', f'<news_image_{image_id}>')
                mime_img.add_header('Content-Disposition', 'inline', filename=image_name)
                msg.attach(mime_img)

    return news_ids


def add_header_and_footer_images_to_main_page(msg):
    with open("static/basic_images/header_main_page.jpg", 'rb') as img:
        mime_img = MIMEImage(img.read())
        mime_img.add_header('Content-ID', '<main_page_header_image>')
        mime_img.add_header('Content-Disposition', 'inline', filename="main_page_header_image")
        msg.attach(mime_img)

    with open("static/basic_images/footer_main_page.png", 'rb') as img:
        mime_img = MIMEImage(img.read())
        mime_img.add_header('Content-ID', '<main_page_footer_image>')
        mime_img.add_header('Content-Disposition', 'inline', filename="main_page_footer_image")
        msg.attach(mime_img)


def send_email(main_page_html, html_content):
    full_email_html = f"""{main_page_html}{html_content}"""

    html_content_attachment = MIMEText(full_email_html, 'html')

    msg = MIMEMultipart()
    msg['Subject'] = "Week news"
    msg['From'] = smtp_user
    msg['To'] = "nikita.d@meuhedet.co.il"

    msg.attach(html_content_attachment)

    add_header_and_footer_images_to_main_page(msg)
    news_ids = add_header_and_news_images_to_news_block(msg)

    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
    server.quit()

    return news_ids



def send_news():
    try:
        main_page_content, main_page_html, news_block_html = make_html_for_email()

        news_ids = send_email(main_page_html,news_block_html)

        print(f"Main page id: {main_page_content.main_page_news_id}")
        print(f"News ids: {news_ids}")

        # update_news_main_page_status(main_page_content.main_page_news_id)
        # update_news_block_status(news_ids)

    except Exception as error:
        logging.exception("ERRORS: ")



