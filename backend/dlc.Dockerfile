ARG BUILD_FROM=deeplabcut/deeplabcut:latest-gui
FROM $BUILD_FROM

ENV API_KEY="mysupersecretpassword"
ENV DLC_PROJECTS="/projects"

EXPOSE 8000

COPY pyproject.toml .
COPY pyinstaller.spec .
COPY requirements*.txt .
COPY setup.* ./

RUN pip install --no-cache-dir .[dlc]

COPY ./tests/testdata /projects
COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
