from fastapi import FastAPI
from .routers import auth_routes, user_routes
from . import database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="The Blog Project")

#Middleware and Routers

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router)
app.include_router(user_routes.router)

@app.on_event("startup")
async def on_startup():
    database.create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)