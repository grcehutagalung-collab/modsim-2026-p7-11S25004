from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    request_id = Column(Integer, ForeignKey("story_requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
