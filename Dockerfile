FROM python:3.13

# Set environment variables
ENV POETRY_VERSION=2.1.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install Poetry
RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /bookpython

# Copy only dependency files first for caching
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the rest of your application
COPY . .

# Command to run your app (example)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]