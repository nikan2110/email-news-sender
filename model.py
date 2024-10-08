from sqlalchemy import Column, Integer, String, Boolean, Date
from config import Base


class News(Base):
    __tablename__ = 'news_block'

    news_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_send = Column(Boolean, default=False)
    news_link = Column(String)

    def __repr__(self):
        return f"<News(" \
               f"title={self.title}, " \
               f"description={self.description}, " \
               f"sent={self.is_send}, " \
               f")>"


class NewsMainPage(Base):
    __tablename__ = 'news_main_page'

    main_page_news_id = Column(Integer, primary_key=True)
    news_date = Column(Date)
    title = Column(String)
    description = Column(String)
    is_send = Column(Boolean, default=False)

    def __repr__(self):
        return f"<News(" \
               f"title={self.title}, " \
               f"description={self.description}, " \
               f"sent={self.is_send}, " \
               f"news_date={self.news_date}, " \
               f")>"