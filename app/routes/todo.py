from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import model
from ..schemas import todo
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from typing import  List, Optional

router = APIRouter(
    prefix="/todos",
    tags=['Todos']
)

@router.get("/", response_model=List[todo.TodoOut])
def get_todos(db: Session = Depends(get_db), 
              current_user: int = Depends(get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    

    todos = db.query(model.Todo).limit(limit).offset(skip).all()

    return todos


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=todo.Todo)
def create_todo(todo: todo.TodoCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    new_todo = model.Todo(owner_id=current_user.id, **todo.dict())
    # add todos to our database
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get("/{id}", response_model=todo.TodoOut)
def get_todo(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    todo = db.query(model.Todo).group_by(
            model.Todo.id).filter(model.Todo.id == id).first()

    # Validation
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    return todo


@router.put("/{id}", response_model=todo.Todo, status_code=status.HTTP_200_OK)
def update_todo(id: int, updated_post: todo.TodoCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    todo_query = db.query(model.Todo).filter(model.Todo.id == id)

    todo = todo_query.first()

    # Validation
    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"todo with id: {id} does not exist")
    
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    todo_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return todo_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    todo_query  = db.query(model.Todo).filter(model.Todo.id == id)

    todo = todo_query.first()

    # Validation
    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"todo with id: {id} does not exists")
    
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    todo_query .delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
