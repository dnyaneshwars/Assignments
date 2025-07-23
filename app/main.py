from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, database, schemas, crud, auth, websocket_manager
from .genai import router as genai_router  

from app.qa.qa_router import router as qa_router
models.Base.metadata.create_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(qa_router, prefix="/qa")
app.include_router(genai_router, prefix="/genai")
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)


@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/todos", response_model=list[schemas.ToDo])
def read_todos(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return crud.get_todos(db, user_id=current_user.id)


@app.post("/todos", response_model=schemas.ToDo)
def create_todo(todo: schemas.ToDoCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_todo = crud.create_todo(db, todo, current_user.id)
    import asyncio
    asyncio.create_task(websocket_manager.manager.broadcast(f"New task added: {db_todo.title}"))
    return db_todo


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.manager.disconnect(websocket)
        
