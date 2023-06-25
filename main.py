from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from router import user, nurse

app = FastAPI(
    title='DavinciService'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router, prefix="")
app.include_router(nurse.router, prefix="")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host="127.0.0.1", port=9001, reload=True)
