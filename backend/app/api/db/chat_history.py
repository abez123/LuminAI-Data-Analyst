
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Conversations(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True)  # Single primary key
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200)),
    status = Column(Enum('active', 'archived', 'deleted',
                    name='conversation_status'), default='active'),
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow)


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True)  # Single primary key
    conversation_id = Column(Integer, ForeignKey("conversations.id")),
    role = Column(Enum('user', 'assistant', 'system', name='message_role')),
    content = Column(Text),  # The actual message content
    tokens_used = Column(Integer),  # Optional: track token usage
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow)
