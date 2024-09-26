from sqlalchemy import Column, Integer, String, Boolean
from config import Base


class News(Base):
    __tablename__ = 'news'

    news_id = Column(Integer, primary_key=True)
    news_title = Column(String)
    news_description = Column(String)
    is_news_send = Column(Boolean, default=False)
    news_link = Column(String)

    def __repr__(self):
        return f"<News(" \
               f"title={self.news_title}, " \
               f"description={self.news_description}, " \
               f"sent={self.is_news_send}, " \
               f")>"
