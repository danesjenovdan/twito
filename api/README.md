# How to run this in dev?

```bash
# Create .env file from template
cp .env.EXAMPLE .env

# Edit it and provide credentials
vi .env

# Option A: run in container
docker-compose up

# Option B: run on local machine
pipenv install
pipenv run bash ./run.sh
```
