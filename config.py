import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import smtplib

from constant import SMTP_SERVER, SMTP_PORT, POSTGRES_PASSWORD

DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@localhost:5432/postgres"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s ', level=logging.INFO,
                    handlers=[logging.StreamHandler(), logging.FileHandler("logs.txt", 'w+')])
