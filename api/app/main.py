from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers import food_security


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(food_security.router)


# @app.get("/")
# def root():
#     return {"message": "Hello World!"}
