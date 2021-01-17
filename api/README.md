# How to run this in dev?

## Create .env file from template
cp .env.EXAMPLE .env

## Option A: run in container
docker-compose up

## Option B: run on local machine
pipenv install
pipenv run bash ./run.sh

## Migrations

### Generate migrations
`[docker-compose exec flask] python manage.py makemigrations`

### Run migrations
`[docker-compose exec flask] python manage.py migrate`
