from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import POSTGRES_PASSWORD
import logging as log

DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

logging = log.getLogger("email_sender")

if not logging.hasHandlers():
    logging.setLevel(log.INFO)

    handler_console = log.StreamHandler()
    handler_file = log.FileHandler("logs.txt", 'w')

    formatter = log.Formatter('%(levelname)s : %(asctime)s : %(message)s')

    handler_console.setFormatter(formatter)
    handler_file.setFormatter(formatter)

    logging.addHandler(handler_console)
    logging.addHandler(handler_file)
