FROM python:3.10
WORKDIR /
ENV PORT=8000
EXPOSE ${PORT}
COPY configuration_requirements.txt configuration_requirements.txt
RUN pip install --no-cache-dir --upgrade -r configuration_requirements.txt
COPY configuration ./
CMD ["sh", "-c",  "uvicorn api:app --host 0.0.0.0 --port ${PORT} --reload --log-level info"]