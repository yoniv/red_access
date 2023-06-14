# red_access

run the docker compose
```bash
docker compose up
```

if the http://0.0.0.0:8000/docs#/ don't work please run the command below
```bash
docker compose restart --no-deps configuration
```

## test the api
the api build on fastApi, so you could check the EP in
http://0.0.0.0:8001/docs#/
