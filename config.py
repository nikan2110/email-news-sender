from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import smtplib

from constant import smtp_server, smtp_port

DATABASE_URL = "postgresql://postgres:411652@localhost:5432/postgres"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

server = smtplib.SMTP(smtp_server, smtp_port)


