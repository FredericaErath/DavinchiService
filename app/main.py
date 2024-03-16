from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.router import user, nurse, doctor, administrator

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
app.include_router(doctor.router, prefix="")
app.include_router(administrator.router, prefix="")

