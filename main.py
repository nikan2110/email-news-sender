import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Session, server
from constant import smtp_user, smtp_password
from model import News
import psycopg2
from constant import html_template
from tools import generate_news_block

session = Session()


def fetch_pending_news():
    return session.query(News).filter_by(is_news_send=False).all()


def generate_email_html(news_items, html_template):
    for news_item in news_items:
        news_block = generate_news_block(news_item)
        html_template += news_block

    html_template += """
        </table>
        </body>
        </html>
    """

    return html_template


def add_header_and_news_image(msg):
    news_ids = []
    with open("header.jpg", 'rb') as img:
        mime_img = MIMEImage(img.read())
        mime_img.add_header('Content-ID', '<header_image>')
        mime_img.add_header('Content-Disposition', 'inline', filename="header")
        msg.attach(mime_img)

    for image_name in os.listdir("./news_image"):
        if image_name.endswith('.png'):
            image_path = os.path.join("./news_image", image_name)
            image_id = image_name.split('.')[0]

            news_ids.append(image_id)

            with open(image_path, 'rb') as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header('Content-ID', f'<news_image_{image_id}>')
                mime_img.add_header('Content-Disposition', 'inline', filename=image_name)
                msg.attach(mime_img)

    return news_ids


def send_email(html_content):
    html_content_attachment = MIMEText(html_content, 'html')

    msg = MIMEMultipart()
    msg['Subject'] = "Week news"
    msg['From'] = smtp_user
    msg['To'] = "nikita.d@meuhedet.co.il"

    msg.attach(html_content_attachment)

    news_ids = add_header_and_news_image(msg)

    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
    server.quit()

    return news_ids


def update_news_status(news_ids):
    session.query(News).filter(News.news_id.in_(news_ids)).update({"is_news_send": True})
    session.commit()


if __name__ == '__main__':
    pending_news = fetch_pending_news()

    if pending_news:
        email_html = generate_email_html(pending_news, html_template)

        news_ids = send_email(email_html)

        # update_news_status(news_ids)

        session.close()



