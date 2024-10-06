from config import Session
from model import News, NewsMainPage

session = Session()

def fetch_pending_news():
    return session.query(News).filter_by(is_news_send=False).all()


def fetch_main_page():
    return session.query(NewsMainPage).filter_by(is_send=False).all()

def update_news_block_status(news_ids):
    session.query(News).filter(News.news_id.in_(news_ids)).update({"is_news_send": True})
    session.commit()


def update_news_main_page_status(main_page_news_id):
    (session.query(NewsMainPage).filter(NewsMainPage.main_page_news_id == main_page_news_id)
     .update({"is_send": True}))
    session.commit()

def session_close():
    session.close()