manage := 'poetry run python manage.py'

su:
    {{ manage }} createsuperuser --email karsten.kroesch@ag.ch --username karsten

serve:
   {{ manage }} runserver

migrate:
   {{ manage }} makemigrations
   {{ manage }} migrate

poetry:
    poetry config virtualenvs.in-project true
    poetry init
    poetry add $(cat requirements.txt)
    poetry install
    poetry lock

freeze:
    poetry export -f requirements.txt > requirements.txt

activate:
    poetry shell

import:
    {{ manage }} loaddata test/fixtures/kroesch.lan.json

rundb:
    podman volume exists pgdata || podman volume create pgdata
    podman run --name postgres-dev \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_DB=clickops \
    -p 5432:5432 \
    -v pgdata:/var/lib/postgresql/data \
    -d postgres:15
