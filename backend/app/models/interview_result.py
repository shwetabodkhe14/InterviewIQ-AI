from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database.base import Base


class InterviewResult(Base):
    __tablename__ = "interview_results"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    technical_score = Column(Integer)
    communication_score = Column(Integer)
    confidence_score = Column(Integer)
    grammar_score = Column(Integer)
    overall_score = Column(Integer)

    strengths = Column(Text)
    weaknesses = Column(Text)
    feedback = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="interview_results"
    )