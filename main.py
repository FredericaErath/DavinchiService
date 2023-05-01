from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import file_management


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

app.include_router(file_management.upload, prefix="")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host="192.168.43.7", port=9001, reload=True)
