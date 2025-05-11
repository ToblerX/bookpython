
# 📚 BookPython Project

This project is a Python web application powered by [Poetry](https://python-poetry.org/) for dependency management and [Docker](https://www.docker.com/) for containerization.

## 🚀 Getting Started

You can start the project using either **Poetry** (locally) or **Docker** (containerized).

---

## 📦 Running Locally with Poetry

### 1. Install Poetry

If you don't have Poetry installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or visit the [official documentation](https://python-poetry.org/docs/#installation).

### 2. Install Dependencies

From the project root:

```bash
poetry install
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following content:

```env
DATABASE_URL=database://user:password@host:port/db_name
SECRET_KEY="YOUR_SECRET_KEY"
ADMIN_PASSWORD="YOUR_PASSWORD_FOR_ADMIN"
```

### 4. Activate the Virtual Environment

```bash
poetry shell
```

### 5. Run the Application

```bash
python your_main_script.py
```

Replace `your_main_script.py` with your actual application entry point (e.g. `main.py`).

---

## 🐳 Running with Docker

### 1. Build the Docker Image

```bash
docker build -t bookpython-app .
```

### 2. Start the Services

```bash
docker-compose up --build
```

This will start the application and any dependent services (e.g. PostgreSQL, if defined in `compose.yml`).

### 3. Shut Down

```bash
docker-compose down
```

---

## ⚙️ Project Structure

```
.
├── .dockerignore
├── .env                # Environment variables
├── .gitignore
├── alembic.ini         # DB migration tool config
├── compose.yml         # Docker Compose setup
├── Dockerfile          # Docker build instructions
├── poetry.lock         # Locked dependency versions
├── poetry.toml         # Poetry configuration
├── pyproject.toml      # Project metadata and dependencies
```

---

## 📬 Support & Contributions

Feel free to open issues or pull requests for suggestions, bugs, or improvements. Contributions are welcome!
