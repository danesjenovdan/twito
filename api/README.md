# How to initialize the db?

```bash
# If you want to execute from container
sudo docker-compose exec flask python
```

```python
from app import init_db
init_db()
```

# How to run this in dev?

```bash
# Create .env file from template
cp .env.EXAMPLE .env

# Edit it and provide credentials
vi .env

# Start Docker container
docker-compose up
```

