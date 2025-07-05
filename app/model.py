from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="true", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()", nullable=False)
    ovener_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    votes = relationship("Vote", back_populates="post")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()", nullable=False)
    votes = relationship("Vote", back_populates="user")

class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)

    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")