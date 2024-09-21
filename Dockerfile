FROM python:3.10

ARG STENOGRAPHER_ENV

ENV STENOGRAPHER_ENV=${STENOGRAPHER_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.8.3

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy files:
WORKDIR /app
COPY . /app/

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install $(test "$STENOGRAPHER_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

CMD ["stenographer", "start"]
