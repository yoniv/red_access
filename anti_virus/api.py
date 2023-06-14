import logging
import os
import re

import requests
import uvicorn
from fastapi import FastAPI, status, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

logger = logging.getLogger("api")
app = FastAPI(title="Anti virus.", version='1.0.0', description="FastAPI and postgres Anti virus.")
HOST = os.environ.get('HOST', default='localhost')
PORT = os.environ.get('PORT', default='8000')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

MALICIOUS_WORDS = set()


def get_malicious_words():
    logger.info("get data from configuration")
    result = requests.get(f'http://{HOST}:{PORT}/words').json()
    for word in result:
        MALICIOUS_WORDS.add(word)


@app.on_event("startup")
@repeat_every(seconds=60)
def startup():
    get_malicious_words()


@app.get("/ping")
async def ping():
    logger.debug("ping")
    return Response(status_code=status.HTTP_200_OK)


@app.post("/check_malicious", response_model=str)
async def check_malicious(file_to_check: UploadFile = File(...)):
    words_in_file = set(re.split('[^a-zA-Z0-9]', file_to_check.file.read().decode('utf8')))
    return 'detected' if any(word in MALICIOUS_WORDS for word in words_in_file) else 'clean'


if __name__ == '__main__':
    uvicorn.run("api:app",
                host="0.0.0.0",
                port=8001,
                log_level=logging.DEBUG)
