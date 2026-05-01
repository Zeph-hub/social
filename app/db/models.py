from sqlalchemy import Column, DateTime, Integer, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SocialPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    sentiment = Column(Text, nullable=True)
    language = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
