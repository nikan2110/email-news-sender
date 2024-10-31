from sqlalchemy import func
from config import Session, logging
from model import News, NewsMainPage, Recipients


def add_news(news):
    """
    Adds a new news item to the database.

    :param news: News object to add.
    """
    session = Session()
    try:
        logging.info(f"Adding news: {news}")
        session.add(news)
        session.commit()
        logging.info("News added successfully")
    except Exception as e:
        session.rollback()
        logging.exception("Failed to add news")
        raise e
    finally:
        session.close()


def add_main_page(main_page):
    """
    Adds a new main page entry to the database.

    :param main_page: NewsMainPage object to add.
    """
    session = Session()
    try:
        logging.info(f"Adding main page: {main_page}")
        session.add(main_page)
        session.commit()
        logging.info("Main page added successfully")
    except Exception as e:
        session.rollback()
        logging.exception("Failed to add main page")
        raise e
    finally:
        session.close()


def fetch_pending_news():
    """
    Fetches all news that have not been sent yet.

    :return: List of pending News objects.
    """
    session = Session()
    try:
        logging.info("Fetching pending news")
        return session.query(News).filter_by(is_send=False).all()
    except Exception as e:
        logging.exception("Failed to fetch pending news")
    finally:
        session.close()


def fetch_main_page():
    """
    Fetches the main page that has not been sent yet.

    :return: List of pending NewsMainPage objects.
    """
    session = Session()
    try:
        logging.info("Fetching main page")
        return session.query(NewsMainPage).filter_by(is_send=False).all()
    finally:
        session.close()


def update_news_block_status(news_ids):
    """
    Updates the 'is_send' status for the given list of news IDs.

    :param news_ids: List of news IDs to mark as sent.
    """
    session = Session()
    try:
        logging.info(f"Updating status for news IDs: {news_ids}")
        session.query(News).filter(News.news_id.in_(news_ids)).update({"is_send": True})
        session.commit()
        logging.info("News status updated successfully")
    except Exception as e:
        session.rollback()
        logging.exception("Failed to update news block status")
        raise e
    finally:
        session.close()


def update_news_main_page_status(main_page_news_id):
    """
    Updates the 'is_send' status for the main page.

    :param main_page_news_id: ID of the main page to mark as sent.
    """
    session = Session()
    try:
        logging.info(f"Updating status for main page ID: {main_page_news_id}")
        session.query(NewsMainPage).filter(NewsMainPage.main_page_news_id == main_page_news_id).update(
            {"is_send": True})
        session.commit()
        logging.info("Main page status updated successfully")
    except Exception as e:
        session.rollback()
        logging.exception("Failed to update main page status")
        raise e
    finally:
        session.close()


def remove_news_block(news_block):
    """
    Removes a news block from the database.

    :param news_block: News object to remove.
    """
    session = Session()
    try:
        logging.info(f"Removing news block: {news_block}")
        session.delete(news_block)
        session.commit()
        logging.info("News block removed successfully")
    except Exception as e:
        session.rollback()
        logging.exception("Failed to remove news block")
        raise e
    finally:
        session.close()


def remove_main_page(main_page):
    """
    Removes a main page from the database.

    :param main_page: NewsMainPage object to remove.
    """
    session = Session()
    try:
        logging.info(f"Removing main page: {main_page}")
        session.delete(main_page)
        session.commit()
        logging.info("Main page removed successfully")
    except Exception as e:
        session.rollback()
        logging.exception("Failed to remove main page")
        raise e
    finally:
        session.close()


def get_next_id(model_type):
    """
    Retrieves the next ID for either the news block or the main page.

    :param model_type: Type of the model ('news_block' or 'main_page').
    :return: The next available ID.
    """
    session = Session()
    max_id = None
    if model_type == 'news_block':
        max_id = session.query(func.max(News.news_id)).scalar()
    elif model_type == 'main_page':
        max_id = session.query(func.max(NewsMainPage.main_page_news_id)).scalar()

    try:
        logging.debug(f"Received max ID: {max_id} for model type: {model_type}")
        if max_id is None:
            return 1
        else:
            return max_id + 1
    except Exception as e:
        logging.exception("Failed to get next ID")
    finally:
        session.close()


def update_news(news_id, updated_title, updated_description, updated_link):
    """
    Updates the news block with the given information.

    :param news_id: ID of the news to update.
    :param updated_title: New title for the news.
    :param updated_description: New description for the news.
    :param updated_link: New link for the news.
    """
    session = Session()
    try:
        logging.info(f"Updating news ID: {news_id}")
        news = session.query(News).filter_by(news_id=news_id).first()

        if news:
            news.title = updated_title
            news.description = updated_description
            news.news_link = updated_link

            session.commit()
            logging.info(f"News ID {news_id} updated successfully")
        else:
            raise ValueError(f"News with ID {news_id} not found.")
    except Exception as e:
        session.rollback()
        logging.exception(f"Failed to update news ID {news_id}")
        raise e
    finally:
        session.close()


def update_main_page(main_page_id, updated_title, updated_description, updated_date):
    """
    Updates the main page with the given information.

    :param main_page_id: ID of the main page to update.
    :param updated_title: New title for the main page.
    :param updated_description: New description for the main page.
    :param updated_date: New date for the main page.
    """
    session = Session()
    try:
        logging.info(f"Updating main page ID: {main_page_id}")
        main_page = session.query(NewsMainPage).filter_by(main_page_news_id=main_page_id).first()

        if main_page:
            main_page.title = updated_title
            main_page.description = updated_description
            main_page.news_date = updated_date

            session.commit()
            logging.info(f"Main page ID {main_page_id} updated successfully")
        else:
            raise ValueError(f"Main page with ID {main_page_id} not found.")
    except Exception as e:
        session.rollback()
        logging.exception(f"Failed to update main page ID {main_page_id}")
        raise e
    finally:
        session.close()


def fetch_all_recipients():
    """
    Fetches all email recipients from the database.

    :return: List of Recipients objects.
    """
    session = Session()
    try:
        logging.info("Fetching all recipients")
        recipients = session.query(Recipients).all()
        return recipients
    except Exception as e:
        logging.exception("Failed to fetch recipients")
    finally:
        session.close()