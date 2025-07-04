from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)  # Здесь хэшированный пароль
    todos = relationship("ToDo", back_populates="owner")  # Связь с задачами
    

class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_completed = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с таблицей users

    user = relationship("User", back_populates="todos")  # Обратная связь



