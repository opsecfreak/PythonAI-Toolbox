import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    agent_name = Column(String)
    prompt = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database connection
db_url = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def log_interaction(agent_name, prompt, response):
    session = Session()
    try:
        log = Log(agent_name=agent_name, prompt=prompt, response=response)
        session.add(log)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Database error: {e}")
    finally:
        session.close()