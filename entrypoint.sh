if [ ! -f .env ]; then
  echo ".env not found in container, creating from .env.example"
  if [ -f .env.example ]; then
    cp .env.example .env
  else
    echo ".env.example not found either! The application might fail."
  fi
else
  echo ".env exists, skipping creation"
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
