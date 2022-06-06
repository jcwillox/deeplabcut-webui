FROM python:3.10-slim-bullseye

ENV DLC_PROJECTS="/projects"

EXPOSE 8000

RUN apt-get update && apt-get install -y ffmpeg \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY pyinstaller.spec .
COPY requirements*.txt .
COPY setup.* ./

RUN pip install --no-cache-dir .

COPY ./tests/testdata /projects
COPY ./app /app

CMD ["uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8000"]
