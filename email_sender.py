import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import logging
from constants import SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, EMAIL_HISTORY_PATH
import psycopg2
from db import fetch_all_recipients, update_news_main_page_status, update_news_block_status, \
    add_email_html_link_to_main_page
from html_builder_email_main import make_html_for_email
from html_builder_email_preview import make_html_for_preview


def add_header_and_news_images_to_news_block(msg):
    """
    Attaches header and news images to the email message.

    :param msg: MIMEMultipart message object.
    :return: List of news IDs whose images were added to the email.
    """
    logging.info("Attaching header and news images to the email")
    news_ids = []

    try:
        with open("static/basic_images/header.jpg", 'rb') as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header('Content-ID', '<header_image>')
            mime_img.add_header('Content-Disposition', 'inline', filename="header")
            msg.attach(mime_img)

        with open("static/basic_images/arrow.png", 'rb') as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header('Content-ID', '<arrow_image>')
            mime_img.add_header('Content-Disposition', 'inline', filename="header")
            msg.attach(mime_img)

        with open("static/basic_images/icon.png", 'rb') as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header('Content-ID', '<icon>')
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
                logging.info(f"Attached image {image_name} for news ID {image_id}")

    except Exception as e:
        logging.exception("Error while attaching images to news block")
        raise e

    return news_ids


def add_header_and_footer_images_to_main_page(msg):
    """
    Attaches header and footer images to the main page of the email.

    :param msg: MIMEMultipart message object.
    """
    logging.info("Attaching header and footer images to the main page")

    try:
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

    except Exception as e:
        logging.exception("Error while attaching images to main page")
        raise e


def send_email(main_page_html, html_content):
    """
    Sends an email with the main page and news block content.

    Parameters:
    - main_page_html (str): HTML content of the main page to be included in the email.
    - html_content (str): HTML content of the news block to be included in the email.

    Returns:
    - list: A list of news IDs (news_ids) included in the email.

    Exceptions:
    - Raises an exception if there is an error while sending the email.

    Description:
    This function creates the full HTML content of the email by combining the main page and news block.
    It also attaches header and footer images to the main page and images for each news block.
    The function connects to the SMTP server, sends the email, and then closes the connection.
    In case of a disconnection, it attempts to reconnect and resend the email.
    """
    logging.info("Preparing to send email")

    full_email_html = f"""{main_page_html}{html_content}"""
    html_content_attachment = MIMEText(full_email_html, 'html')

    msg = MIMEMultipart()
    msg['Subject'] = "Week news"
    msg['From'] = SMTP_USER
    msg['To'] = get_recipients_list()

    msg.attach(html_content_attachment)

    logging.info("Attaching main page and news block images")
    add_header_and_footer_images_to_main_page(msg)
    news_ids = add_header_and_news_images_to_news_block(msg)

    try:
        logging.info("Starting email server and sending email")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

        logging.info("Email sent successfully")
    except smtplib.SMTPServerDisconnected:
        logging.exception("SMTP server disconnected, trying to reconnect")

        server.connect(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    except Exception as e:
        logging.exception("Error while sending email")
        raise e
    finally:
        server.quit()
        return news_ids

def get_recipients_list():
    """
    Fetches the list of email recipients from the database and returns them as a string.

    :return: A string of recipient email addresses separated by commas.
    """
    logging.info("Fetching recipients from database")
    recipients = fetch_all_recipients()
    recipient_emails = [recipient.recipient for recipient in recipients]
    recipients_string = ', '.join(recipient_emails)
    logging.info(f"Recipients: {recipients_string}")
    return recipients_string


def save_email_history(main_page_id, main_page_date):

    history_folder = 'static/email_history'
    html_for_saving = make_html_for_preview()

    file_name = f"email_{main_page_date}.html"
    file_path = os.path.join(history_folder, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_for_saving)

    email_history_link = f"{EMAIL_HISTORY_PATH}/{file_name}"

    add_email_html_link_to_main_page(main_page_id,email_history_link)

def send_news():
    """
    Generates the main page and news block HTML content, then sends the email.

    Logs any exceptions that occur during the process.
    """
    logging.info("Sending news email")
    try:
        main_page_content, main_page_html, news_block_html = make_html_for_email()

        news_ids = send_email(main_page_html, news_block_html)

        # update_news_main_page_status(main_page_content.main_page_news_id)
        # update_news_block_status(news_ids)

        save_email_history(main_page_content.main_page_news_id,main_page_content.news_date)


        logging.info("Email sent and status updated successfully")
    except Exception as error:
        logging.exception("Error occurred while sending news")