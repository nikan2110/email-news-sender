import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import smtplib

from constant import smtp_server, smtp_port, postgres_password

DATABASE_URL = f"postgresql://postgres:{postgres_password}@localhost:5432/postgres"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

server = smtplib.SMTP(smtp_server, smtp_port)

logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s ', level=logging.INFO,
                    handlers=[logging.StreamHandler(), logging.FileHandler("logs.txt", 'w+')])
