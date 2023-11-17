from fastapi import FastAPI
from .models import model
from .db.config import engine
from .routes import user, todo, auth
from .environment.config import Settings

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routes
app.include_router(user.router)
app.include_router(todo.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
