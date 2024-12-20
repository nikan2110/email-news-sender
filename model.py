from sqlalchemy import Column, Integer, String, Boolean, Date
from config import Base


class News(Base):
    """
    Represents a news block in the email newsletter system.

    Attributes:
        news_id (int): Primary key for the news block.
        title (str): The title of the news block.
        description (str): The description of the news block.
        is_send (bool): Whether the news block has been sent. Default is False.
        news_link (str): A link related to the news block.
    """

    __tablename__ = 'news_block'

    news_id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String)
    description = Column(String)
    is_send = Column(Boolean, default=False)
    news_link = Column(String)
    sort_order = Column(Integer)
    strategy_image_path = Column(String)
    strategy_name = Column(String)

    def __repr__(self):
        return f"<News(" \
               f"title={self.title}, " \
               f"description={self.description}, " \
               f"sent={self.is_send}, " \
               f")>"

class NewsStrategy(Base):
    """
    Represents a news strategy.

    Attributes:
        strategy_name (str): Strategy name.
        strategy_path (str): Strategy image path.
    """

    __tablename__ = 'news_strategies'

    strategy_name = Column(String, primary_key=True)
    strategy_path = Column(String)
    strategy_name_en = Column(String)

    def __repr__(self):
        return (f"<NewsStrategy(strategy_name={self.strategy_name}, strategy_path={self.strategy_path}, "
                f"self.strategy_name_en={self.strategy_name_en})>")


class NewsMainPage(Base):
    """
    Represents the main page of the email newsletter.

    Attributes:
        main_page_news_id (int): Primary key for the main page.
        news_date (Date): The date of the newsletter.
        title (str): The title of the main page.
        description (str): The description of the main page.
        is_send (bool): Whether the main page has been sent. Default is False.
    """

    __tablename__ = 'news_main_page'

    main_page_news_id = Column(Integer, primary_key=True, autoincrement=False)
    news_date = Column(Date)
    title = Column(String)
    description = Column(String)
    is_send = Column(Boolean, default=False)
    history_link = Column(String)

    def __repr__(self):
        return f"<News(" \
               f"title={self.title}, " \
               f"description={self.description}, " \
               f"sent={self.is_send}, " \
               f"news_date={self.news_date}, " \
               f")>"


class Recipients(Base):
    """
    Represents the recipients of the email newsletter.

    Attributes:
        recipient (str): The email address of the recipient. This is the primary key.
    """

    __tablename__ = 'news_recipients'

    recipient = Column(String, primary_key=True)

    def __repr__(self):
        return f"<Recipient(Recipient={self.recipient})"
