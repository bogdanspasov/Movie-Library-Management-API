from fastapi import FastAPI
from routers.users import users_router
from routers.movies import movies_router


app = FastAPI()
app.include_router(movies_router)
app.include_router(users_router)