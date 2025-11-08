if [ ! -f .env ]; then
  echo ".env not found, creating from .env.example"
  cp .env.example .env
else
  echo ".env exists, skipping creation"
fi

exec "$@"
