from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey
from datetime import datetime
from app.database import Base

class Article(Base):

    '''
    The DB store for Articles
    TODO : Add relationship for easy article.source.name
    '''
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    #source: Mapped[str] = mapped_column(String, nullable=False)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="RESTRICT"),index=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    published: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    guid: Mapped[str | None] = mapped_column(String, nullable=True)



class Source(Base):

    '''
    The DB store for sources
    '''
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    
