from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from database import Base


class Quiz(Base):
    """
    Database model for storing Wikipedia quiz data.
    """
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    raw_html = Column(Text)  # Store raw HTML for reference (bonus feature)
    
    # JSON fields
    key_entities = Column(JSON)  # {people: [], organizations: [], locations: []}
    sections = Column(JSON)  # List of section titles
    quiz_questions = Column(JSON)  # List of quiz questions
    related_topics = Column(JSON)  # List of related Wikipedia topics
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', url='{self.url}')>"
