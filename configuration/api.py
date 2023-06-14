import logging
from typing import Set

import uvicorn
from asyncpg import UniqueViolationError
from fastapi import FastAPI, Depends, status, Response, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, get_session
from schema import malicious_words

logger = logging.getLogger("api")
app = FastAPI(title="configuration.", version='1.0.0', description="FastAPI and postgres configuration.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/ping")
async def ping():
    logger.debug("ping")
    return Response(status_code=status.HTTP_200_OK)


@app.get("/words", response_model=Set[str])
async def list_words(session=Depends(get_session)):
    query = malicious_words.select()
    result = await session.execute(query)
    words = set([i[0] for i in result.all()])
    return words


@app.post("/words", status_code=status.HTTP_201_CREATED)
async def add_word(session=Depends(get_session),
                   word: str = Query(alias='word')):
    try:
        query = malicious_words.insert().values(word=word)
        await session.execute(query)
    except UniqueViolationError as exc:
        await session.roolback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from exc


if __name__ == '__main__':
    uvicorn.run("api:app",
                host="0.0.0.0",
                port=8000,
                log_level=logging.DEBUG)
