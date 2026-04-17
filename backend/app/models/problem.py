# app/models/problem.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.db.base_class import Base

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    # Relationships
    topics = relationship("ProblemInTopic", back_populates="problem")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProblemInTopic(Base):
    __tablename__ = "problem_in_topic"
    id = Column(Integer, primary_key=True, index=True)
    
    problem_id = Column(Integer, ForeignKey("problems.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    
    # Relationships
    problem = relationship("Problem", back_populates="topics")
    topic = relationship("Topic", back_populates="problems")

    created_at = Column(DateTime, default=datetime.utcnow)
    