from fastapi import FastAPI
from . import database

app = FastAPI(title="The Blog Project")

@app.on_event("startup")
async def on_startup():
    database.create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)