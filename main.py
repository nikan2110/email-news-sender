import logging
import os
import time

import streamlit as st
from PIL import Image

from constants import MAIN_PAGE_MODEL, NEWS_BLOCK_MODEL
from db import fetch_pending_news, remove_news_block, add_news, update_news, get_next_id, fetch_main_page, \
    update_main_page, remove_main_page
from email_sender import send_news
from html_builder_email_preview import make_html_for_preview
from model import News, NewsMainPage
from tools import get_image_path

st.set_page_config(page_title="Email Sender", layout="wide")

(news_block_tab, main_page_tab,
 preview_tab, send_mail_tab) = st.tabs(["News block", "Main page", "Preview", "Send email"])

def save_image_as_png(image, news_id):
    """
    Saves the uploaded image as a PNG with the name of the news ID.
    """
    output_path = get_image_path(news_id)
    output_path = os.path.splitext(output_path)[0] + '.png'
    img = Image.open(image)
    img.save(output_path, format='PNG')
    logging.info(f"Image saved as {output_path}")


def delete_image(news_id):
    """
    Deletes the image associated with a specific news ID.
    """
    image_path = get_image_path(news_id)
    image_path_png = os.path.splitext(image_path)[0] + '.png'
    if os.path.exists(image_path_png):
        os.remove(image_path_png)
        logging.info(f"Image {image_path_png} deleted successfully")
        st.success(f"Image for news ID {news_id} was successfully deleted.")
    else:
        st.warning(f"Image {image_path_png} not found, cannot delete")
        logging.warning(f"Image {image_path_png} not found, skipping deletion")

def render_preview_tab():
    """
    Renders the preview tab for displaying a preview of the email.
    """
    with preview_tab:
        logging.info("Rendering Preview Tab")
        html_for_preview = make_html_for_preview()

        html_with_scroll = f"""
        <div style="height: 100vh; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">
            {html_for_preview}
        </div>
        """

        st.markdown("### Email Preview:")
        st.components.v1.html(html_with_scroll, height=700)


def render_send_email_tab():
    """
    Renders the tab for sending the email. This includes a button to trigger the email sending function.
    """
    with send_mail_tab:
        logging.info("Rendering Send Email Tab")
        st.title("Mailing List Control Panel")

        if st.button("🔴 Send Email"):
            logging.info("Send Email button clicked")
            send_news()
            st.success("Email was sent successfully")
            logging.info("Email sent successfully")


def render_news_block_tab():
    """
    Renders the tab for adding, updating, and deleting news blocks.
    """

    with news_block_tab:
        logging.info("Rendering News Block Tab")
        st.header("Add new news")

        new_news_id = get_next_id(NEWS_BLOCK_MODEL)
        logging.info(f"Generated new news ID: {new_news_id}")

        new_news_title = st.text_input("News title", key="new_news_title")
        new_news_description = st.text_area("News description", key="new_news_description")
        news_link = st.text_input("News link", key="new_news_link")

        if st.button("Add new news", key="add_news"):
            logging.info(f"Adding news with ID: {new_news_id}")
            new_news = News(news_id=new_news_id, title=new_news_title, description=new_news_description,
                            news_link=news_link, is_send=False)
            add_news(new_news)
            st.success("News added successfully")
            logging.info(f"News with ID: {new_news_id} added successfully")

        news_blocks = fetch_pending_news()
        logging.info(f"Fetched {len(news_blocks)} pending news blocks")
        news_blocks.sort(key=lambda x: x.news_id)

        if not news_blocks:
            st.write("There are no news for sending")
        else:
            for news in news_blocks:
                st.subheader(f"News ID: {news.news_id}")

                image_column, title_description_link_column = st.columns([1, 2])

                with title_description_link_column:
                    title = st.text_input(f"News title ID {news.news_id}", news.title, key=f"title_{news.news_id}")
                    description = st.text_area(f"News description ID {news.news_id}", news.description,
                                               key=f"description_{news.news_id}")
                    link = st.text_input(f"News link ID {news.news_id}", news.news_link, key=f"link_{news.news_id}")

                with image_column:
                    image_path = get_image_path(news.news_id)
                    image_path_png = os.path.splitext(image_path)[0] + '.png'

                    if os.path.exists(image_path_png):
                        st.image(image_path_png, caption=f"News image ID {news.news_id}", use_column_width=True)

                        # Добавляем кнопку для удаления изображения
                        if st.button(f"Delete image for news ID {news.news_id}", key=f"delete_image_{news.news_id}"):
                            delete_image(news.news_id)
                    else:
                        st.warning(f"News image {news.news_id} does not exist")
                        logging.warning(f"Image not found for news ID {news.news_id}")
                        uploaded_image = st.file_uploader(f"Upload image for news ID {news.news_id}",
                                                          type=["jpg", "jpeg", "png"], key=f"upload_{news.news_id}")

                        if uploaded_image is not None:
                            save_image_as_png(uploaded_image, news.news_id)
                            st.success(f"Image for news ID {news.news_id} uploaded successfully")
                            st.cache_data.clear()

                save_button_col, delete_button_col = st.columns(2)

                with save_button_col:
                    if st.button(f"Save changes for news ID {news.news_id}", key=f"save_{news.news_id}"):
                        logging.info(f"Saving changes for news ID: {news.news_id}")
                        update_news(news.news_id, title, description, link)
                        st.success(f"Changes for news ID {news.news_id} were successfully saved.")
                        logging.info(f"Changes for news ID {news.news_id} saved successfully")

                with delete_button_col:
                    if st.button(f"Delete news ID {news.news_id}", key=f"delete_{news.news_id}", type='primary'):
                        logging.info(f"Deleting news ID: {news.news_id}")
                        remove_news_block(news)
                        delete_image(news.news_id)  # Удаляем картинку вместе с новостью
                        st.success(f"News ID {news.news_id} was successfully deleted.")
                        logging.info(f"News ID {news.news_id} deleted successfully")

def render_main_page_tab():
    """
    Renders the tab for adding, updating, and deleting the main page information.
    """
    with main_page_tab:
        logging.info("Rendering Main Page Tab")
        st.header("Add main page")

        new_main_page_id = get_next_id(MAIN_PAGE_MODEL)
        logging.info(f"Generated new main page ID: {new_main_page_id}")

        new_main_page_title = st.text_input("Main page title", key="new_main_page_title")
        new_main_page_date = st.date_input("Main page date", key="new_main_page_date")
        new_main_page_description = st.text_area("Main page description", key="new_main_page_description")

        if st.button("Add new main page", key="add_main_page"):
            logging.info(f"Adding new main page with ID: {new_main_page_id}")
            new_main_page = NewsMainPage(main_page_news_id=new_main_page_id, news_date=new_main_page_date,
                                         title=new_main_page_title, description=new_main_page_description)
            add_news(new_main_page)
            st.success("Main page added successfully")
            logging.info(f"Main page with ID {new_main_page_id} added successfully")

        main_pages = fetch_main_page()

        if not main_pages:
            st.write("There are no main page for sending")
        else:
            main_page = main_pages[0]
            st.subheader(f"Main page ID: {main_page.main_page_news_id}")

            title = st.text_input(f"Main page title ID {main_page.main_page_news_id}",
                                  main_page.title, key=f"title_main_page{main_page.main_page_news_id}")

            description = st.text_area(f"Main page description ID {main_page.main_page_news_id}",
                                       main_page.description,
                                       key=f"description_main_page{main_page.main_page_news_id}")

            date = st.date_input(f"Main page date ID {main_page.main_page_news_id}",
                                 main_page.news_date, key=f"date_{main_page.main_page_news_id}")

            save_button_col, delete_button_col = st.columns(2)

            with save_button_col:
                if st.button(f"Save changes for main page ID {main_page.main_page_news_id}",
                             key=f"save_main_page{main_page.main_page_news_id}"):
                    logging.info(f"Saving changes for main page ID: {main_page.main_page_news_id}")
                    update_main_page(main_page.main_page_news_id, title, description, date)
                    st.success(f"Changes for main page ID {main_page.main_page_news_id} were successfully saved.")
                    logging.info(f"Changes for main page ID {main_page.main_page_news_id} saved successfully")

            with delete_button_col:
                if st.button(f"Delete main page ID {main_page.main_page_news_id}",
                             key=f"delete_main_page{main_page.main_page_news_id}"):
                    logging.info(f"Deleting main page ID: {main_page.main_page_news_id}")
                    remove_main_page(main_page)
                    st.success(f"Main page ID {main_page.main_page_news_id} was successfully deleted.")
                    logging.info(f"Main page ID {main_page.main_page_news_id} deleted successfully")


if __name__ == '__main__':
    logging.info("Starting Email Sender Application")
    render_news_block_tab()
    render_main_page_tab()
    render_preview_tab()
    render_send_email_tab()
    logging.info("Email Sender Application rendered successfully")