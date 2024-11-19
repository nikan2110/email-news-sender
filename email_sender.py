import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import logging
from constants import SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, EMAIL_HISTORY_PATH
import psycopg2
from db import fetch_all_recipients, update_news_main_page_status, update_news_block_status, \
    add_email_html_link_to_main_page, fetch_main_page, fetch_pending_news
from html_builder_email_main import make_html_for_email
from html_builder_email_preview import make_html_for_preview


def add_header_and_news_images_to_news_block(msg, pending_news):
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

        for news in pending_news:
            image_path = f"static/news_images/{news.news_id}.png"
            image_id = news.news_id

            news_ids.append(news.news_id)

            if os.path.exists(image_path):
                with open(image_path, 'rb') as img:
                    mime_img = MIMEImage(img.read())
                    mime_img.add_header('Content-ID', f'<news_image_{image_id}>')
                    mime_img.add_header('Content-Disposition', 'inline', filename=f"{image_id}.png")
                    msg.attach(mime_img)
                logging.info(f"Attached image for news ID {image_id}")
            else:
                logging.warning(f"Image for news ID {image_id} not found at {image_path}")


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

def add_strategy_images_to_news_block(msg, pending_news):
    """
    Attaches strategy images to the email for each news item in the `pending_news` list.

    Parameters:
        msg (MIMEMultipart): The email message object to which images will be attached.
        pending_news (list of News): A list of News objects containing information about the news items,
                                     including paths to strategy images and strategy names.

    This function iterates over the provided `pending_news` list, checks if each news item has a valid
    `strategy_image_path`, and attaches the image to the email with a unique Content-ID based on the
    strategy name. If an image file does not exist at the specified path, a warning is logged.

    Raises:
        Exception: If an error occurs while attaching images, the exception is logged and re-raised.
    """
    try:
        for news in pending_news:

            image_path = news.strategy_image_path
            strategy_name = news.strategy_name

            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img:
                    mime_img = MIMEImage(img.read())
                    mime_img.add_header('Content-ID', f'<strategy_image_{strategy_name}>')
                    mime_img.add_header('Content-Disposition', 'inline', filename=strategy_name)
                    msg.attach(mime_img)
                logging.info(f"Attached image {strategy_name} for news ID {news.news_id}")
            else:
                logging.warning(f"Image for strategy {strategy_name} not found at {image_path}")

    except Exception as e:
        logging.exception("Error while attaching images to main page")
        raise e

def send_email(main_page_html, html_content, pending_news):
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
    add_strategy_images_to_news_block(msg, pending_news)
    news_ids = add_header_and_news_images_to_news_block(msg, pending_news)

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

def save_email_history(main_page_id, main_page_date, news_main_page, pending_news):
    """
        Saves an HTML preview of the email to the history folder and adds a link to the main page in the database.

        Parameters:
            main_page_id (int): The ID of the main page to associate with the saved HTML file.
            main_page_date (str): The date of the main page, used in the file name for the saved HTML.
            news_main_page (dict): The main page content used for the email preview.
            pending_news (list of News): A list of News objects containing the news items to be included in the email.

        This function generates an HTML preview of the email using the provided main page and news items, saves the
        HTML to the `email_history` folder with a file name based on `main_page_date`, and adds a link to this
        saved file in the main page record in the database.

        Raises:
            Exception: If an error occurs while writing the file or updating the main page, it will be propagated.
        """

    history_folder = 'static/email_history'
    html_for_saving = make_html_for_preview(news_main_page, pending_news)

    file_name = f"email_{main_page_date}.html"
    file_path = os.path.join(history_folder, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_for_saving)

    email_history_link = f"{EMAIL_HISTORY_PATH}/{file_name}"

    add_email_html_link_to_main_page(main_page_id,email_history_link)

def send_news(environment):
    """
    Generates the main page and news block HTML content, then sends the email.

    Logs any exceptions that occur during the process.
    """
    logging.info("Sending news email")
    try:
        news_main_page = fetch_main_page()
        pending_news = fetch_pending_news()

        main_page_content, main_page_html, news_block_html = make_html_for_email(news_main_page, pending_news)

        news_ids = send_email(main_page_html, news_block_html, pending_news)

        if environment == "Development":
            logging.info("Sending email in Development environment...")

        elif environment == "Production":
            if 9 in news_ids:
                news_ids.remove(9)

            update_news_main_page_status(main_page_content.main_page_news_id)
            update_news_block_status(news_ids)
            logging.info("Sending email in Production environment...")


        save_email_history(main_page_content.main_page_news_id,main_page_content.news_date, news_main_page,
                           pending_news)


        logging.info("Email sent and status updated successfully")
    except Exception as error:
        logging.exception("Error occurred while sending news")