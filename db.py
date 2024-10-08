from sqlalchemy import func
from config import Session
from model import News, NewsMainPage

# Функция для добавления новости
def add_news(news):
    session = Session()
    try:
        session.add(news)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def fetch_pending_news():
    session = Session()
    try:
        return session.query(News).filter_by(is_send=False).all()
    finally:
        session.close()

def fetch_main_page():
    session = Session()
    try:
        return session.query(NewsMainPage).filter_by(is_send=False).all()
    finally:
        session.close()

def update_news_block_status(news_ids):
    session = Session()
    try:
        session.query(News).filter(News.news_id.in_(news_ids)).update({"is_send": True})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_news_main_page_status(main_page_news_id):
    session = Session()
    try:
        session.query(NewsMainPage).filter(NewsMainPage.main_page_news_id == main_page_news_id).update({"is_send": True})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def remove_news_block(news_block):
    session = Session()
    try:
        session.delete(news_block)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_next_news_id():
    session = Session()
    try:
        max_id = session.query(func.max(News.news_id)).scalar()
        if max_id is None:
            return 1
        else:
            return max_id + 1
    finally:
        session.close()

def update_news(news_id, updated_title, updated_description, updated_link):
    session = Session()
    try:
        news = session.query(News).filter_by(news_id=news_id).first()

        if news:
            news.title = updated_title
            news.description = updated_description
            news.news_link = updated_link

            session.commit()
        else:
            raise ValueError(f"News with ID {news_id} not found.")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()