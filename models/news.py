from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, Text
from datetime import datetime
from database import Base

class Article(Base):

    '''
    The DB store
    '''
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    source: Mapped[str] = mapped_column(String, nullable=False)

    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    published: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    guid: Mapped[str | None] = mapped_column(String, nullable=True)