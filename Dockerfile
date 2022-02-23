FROM python:3

# ARG YOUR_ENV

# ENV YOUR_ENV=${YOUR_ENV} \
#   PYTHONFAULTHANDLER=1 \
#   PYTHONUNBUFFERED=1 \
#   PYTHONHASHSEED=random \
#   PIP_NO_CACHE_DIR=off \
#   PIP_DISABLE_PIP_VERSION_CHECK=on \
#   PIP_DEFAULT_TIMEOUT=100 \
#   POETRY_VERSION=1.0.0

# # System deps:
# RUN pip install "poetry"

# System deps:
RUN pip install "poetry"

# Copy only requirements to cache them in docker layer
# WORKDIR /code
COPY poetry.lock pyproject.toml ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . .

# By default, listen on port 5000
EXPOSE 5000/tcp

CMD [ "python", "app.py"]