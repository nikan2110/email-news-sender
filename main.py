import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Session, server
from constant import smtp_user, smtp_password, main_page_content, main_page_html_template_begin, \
    main_page_html_template_end
from model import News
import psycopg2
from constant import news_html_template
from tools import generate_news_block

session = Session()


def fetch_pending_news():
    return session.query(News).filter_by(is_news_send=False).all()


def generate_news_block_html(news_items, html_template):
    for news_item in news_items:
        news_block = generate_news_block(news_item)
        html_template += news_block

    html_template += """
        </table>
        </body>
        </html>
    """

    return html_template


def add_header_and_news_images_to_news_block(msg):
    news_ids = []
    with open("basic_images/header.jpg", 'rb') as img:
        mime_img = MIMEImage(img.read())
        mime_img.add_header('Content-ID', '<header_image>')
        mime_img.add_header('Content-Disposition', 'inline', filename="header")
        msg.attach(mime_img)

    for image_name in os.listdir("news_images"):
        if image_name.endswith('.png'):
            image_path = os.path.join("news_images", image_name)
            image_id = image_name.split('.')[0]

            news_ids.append(image_id)

            with open(image_path, 'rb') as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header('Content-ID', f'<news_image_{image_id}>')
                mime_img.add_header('Content-Disposition', 'inline', filename=image_name)
                msg.attach(mime_img)

    return news_ids


def add_header_and_footer_images_to_main_page(msg):
    with open("basic_images/header_main_page.jpg", 'rb') as img:
        mime_img = MIMEImage(img.read())
        mime_img.add_header('Content-ID', '<main_page_header_image>')
        mime_img.add_header('Content-Disposition', 'inline', filename="main_page_header_image")
        msg.attach(mime_img)

    with open("basic_images/footer_main_page.png", 'rb') as img:
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


def update_news_status(news_ids):
    session.query(News).filter(News.news_id.in_(news_ids)).update({"is_news_send": True})
    session.commit()


def generate_main_page_html(main_page_html_template_begin, main_page_html_template_end, main_page_content):
    main_page_html = ""
    main_page_html += main_page_html_template_begin
    main_page_html += f"""
    <tr>
        <td style="padding: 20px; text-align: right; direction: rtl; background-color: #ffffff; color: #000000; 
        font-size: 16px; line-height: 1.5;">
            "{main_page_content}"
        </td>
    </tr>"""
    
    main_page_html += main_page_html_template_end

    return main_page_html


if __name__ == '__main__':
    pending_news = fetch_pending_news()

    if pending_news:
        main_page_html = generate_main_page_html(main_page_html_template_begin,
                                                 main_page_html_template_end,
                                                 main_page_content)

        news_block_html = generate_news_block_html(pending_news, news_html_template)

        news_ids = send_email(main_page_html,news_block_html)

        # update_news_status(news_ids)

        session.close()



