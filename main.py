from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from models import ToDo, User
from schemas import ToDoCreate, ToDoUpdate, ToDoResponse, UserCreate, UserResponse 
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils import create_access_token, get_password_hash, verify_password


app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Приложение работает!"}

# Эндпоинт для регистрации
@app.post("/users/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли уже пользователь
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username уже занят")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Эндпоинт для логина (возвращает токен)
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Создать задачу
@app.post("/todos/", response_model=ToDoResponse)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_todo = ToDo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# Получить список задач
@app.get("/todos/", response_model=list[ToDoResponse])
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(ToDo).all()
    return todos

# Обновить задачу
@app.put("/todos/{todo_id}", response_model=ToDoResponse)
async def update_todo(todo_id: int, todo: ToDoUpdate, db: Session = Depends(get_db)):
    existing_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(existing_todo, key, value)
    db.commit()
    db.refresh(existing_todo)
    return existing_todo

# Удалить задачу
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    existing_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    db.delete(existing_todo)
    db.commit()
    return {"detail": "Задача удалена"}

