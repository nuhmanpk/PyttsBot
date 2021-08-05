from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

DB_URI = "postgres://zrxnzwzeiypfzw:75387f4557cd36b6a036864a5927d9e128955fa9e8478fa2af8d9360d13a3941@ec2-18-211-171-122.compute-1.amazonaws.com:5432/d60du9ge6npgc2"

def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
