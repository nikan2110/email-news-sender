import os
import streamlit as st
from db import fetch_pending_news, remove_news_block, add_news, get_next_news_id, update_news
from email_sender import send_news
from model import News
from tools import get_image_path

st.set_page_config(page_title="Email Sender", layout="wide")

news_block_tab, main_page_tab, send_mail_tab = st.tabs(["News block", "Main page", "Send email"])

def render_send_email_tab():
    with send_mail_tab:
        st.title("Mailing List Control Panel")

        if st.button("🔴 Send Email"):
            send_news()  # Логика отправки письма
            st.success("Email was sent successfully")

def render_news_block_tab():
    with news_block_tab:
        st.header("Add new news")

        new_news_id = get_next_news_id()
        new_news_title = st.text_input("News title", key="new_news_title")
        new_news_description = st.text_area("News description", key="new_news_description")
        news_link = st.text_input("News link", key="new_news_link")

        if st.button("Add new news", key="add_news"):
            new_news = News(news_id=new_news_id, title=new_news_title, description=new_news_description, news_link=news_link, is_send=False)
            add_news(new_news)
            st.success("News added successfully")

        news_blocks = fetch_pending_news()
        news_blocks.sort(key=lambda x: x.news_id)

        if not news_blocks:
            st.write("There are no news for sending")
        else:
            for news in news_blocks:
                st.subheader(f"News ID: {news.news_id}")

                image_column, title_description_link_column = st.columns([1, 2])

                with title_description_link_column:
                    title = st.text_input(f"News title ID {news.news_id}", news.title, key=f"title_{news.news_id}")
                    description = st.text_area(f"News description ID {news.news_id}", news.description, key=f"description_{news.news_id}")
                    link = st.text_input(f"News link ID {news.news_id}", news.news_link, key=f"link_{news.news_id}")

                with image_column:
                    image_path = get_image_path(news.news_id)

                    if os.path.exists(image_path):
                        st.image(image_path, caption=f"News image ID {news.news_id}", use_column_width=True)
                    else:
                        st.warning(f"News image {news.news_id} does not exist")

                save_button_col, edit_button_col = st.columns(2)

                with save_button_col:
                    if st.button(f"Save changes for news ID {news.news_id}", key=f"save_{news.news_id}"):

                        update_news(news.news_id, title, description, link)
                        st.success(f"Changes for news ID {news.news_id} were successfully saved.")

                with edit_button_col:
                    if st.button(f"Delete news ID {news.news_id}", key=f"delete_{news.news_id}"):
                        remove_news_block(news)
                        st.success(f"News ID {news.news_id} was successfully deleted.")

if __name__ == '__main__':
    render_news_block_tab()
    render_send_email_tab()

