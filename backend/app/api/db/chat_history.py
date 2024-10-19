
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()


class Conversations(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True)  # Single primary key
    user_id = Column(Integer, ForeignKey("users.id"))
    data_source_id = Column(Integer, ForeignKey("data_sources.id"))
    title = Column(String(200), nullable=True),
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="conversation")
    message = relationship("Messages", back_populates="conversation")
    data_source = relationship("DataSources", back_populates="conversation")


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True)  # Single primary key
    conversation_id = Column(Integer, ForeignKey("conversations.id")),
    role = Column(Enum('user', 'assistant', 'system', name='message_role')),
    content = Column(JSON),  # The actual message content
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow)

    # Relationship
    conversation = relationship("Conversations", back_populates="message")
