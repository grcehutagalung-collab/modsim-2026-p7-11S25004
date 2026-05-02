from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.extensions import Base

class StoryRequest(Base):
    __tablename__ = "story_requests"

    id = Column(Integer, primary_key=True)
    theme = Column(String(100))
    genre = Column(String(50))   # fiksi / horor / romantis
    length = Column(String(20))  # pendek / sedang / panjang
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
