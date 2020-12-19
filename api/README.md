# How to run this in dev?

```bash
# Create .env file from template
cp .env.EXAMPLE .env

# Edit it and provide credentials
vi .env

# Start Docker container
docker-compose up

# Generate migration
flask db migrate -m "Initial migration."

# Run migrations
flask db upgrade
```
