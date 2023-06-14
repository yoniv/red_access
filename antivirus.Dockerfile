FROM python:3.10
WORKDIR /
ENV PORT=8001
EXPOSE ${PORT}
COPY antivirus_requirements.txt antivirus_requirements.txt
RUN pip install --no-cache-dir --upgrade -r antivirus_requirements.txt
COPY ./anti_virus ./
CMD ["sh", "-c",  "uvicorn api:app --host 0.0.0.0 --port ${PORT} --reload --log-level info"]