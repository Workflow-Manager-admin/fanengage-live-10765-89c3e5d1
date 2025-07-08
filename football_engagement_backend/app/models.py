# Models and DB session for Football Engagement App

import os
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Text, ForeignKey, TIMESTAMP
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# PUBLIC_INTERFACE
def get_database_url():
    """Get the SQLAlchemy database URL from environment variables or default."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://fanengage:fanengagepwd@football_engagement_database:5432/fanengage"
    )

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# PUBLIC_INTERFACE
def get_db():
    """Provide a database session context generator. Call next() to get session, and finally close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    created_at = Column(TIMESTAMP)

    responses = relationship("Response", back_populates="user")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    youtube_url = Column(String(512), nullable=False)
    status = Column(String(32), nullable=False)
    created_at = Column(TIMESTAMP)

    questions = relationship("Question", back_populates="match")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    question_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP)
    
    match = relationship("Match", back_populates="questions")
    responses = relationship("Response", back_populates="question")
    analysis = relationship("Analysis", back_populates="question", uselist=False)

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer = Column(Boolean, nullable=False)
    responded_at = Column(TIMESTAMP)
    
    user = relationship("User", back_populates="responses")
    question = relationship("Question", back_populates="responses")

class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    analysis_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP)
    
    question = relationship("Question", back_populates="analysis")
