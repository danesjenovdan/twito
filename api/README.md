# How to run this in dev?

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

## Useful commands
### Get tweets
Fetches tweets for all days in the given date range from `start_date` to `end_date` (both included).

Date format: `%Y-%m-%d`

`[docker-compose exec flask] flask get_tweets start_date end_date`

### Calculate daily summaries
Calculates daily summaries for all days in the given date range from `start_date` to `end_date` (both included).

Date format: `%Y-%m-%d`

! Summaries are calculated on existing tweets in the database, so run `get_tweets` command first.

`[docker-compose exec flask] flask calculate_daily_summaries start_date end_date`