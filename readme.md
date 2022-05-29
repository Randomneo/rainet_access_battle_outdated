# rainet access battle

// TODO: rules and description

# Config

At the moment no extra config required for local start

# Startup

    docker-compose up

or to run server in background mode

    docker-compose up -d

After first up:

    docker-compose python manage.py migrate

# Usage

api available at port `8000`

database interface adminer available at port `8080`
