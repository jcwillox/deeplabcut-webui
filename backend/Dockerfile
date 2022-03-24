ARG BUILD_FROM=deeplabcut/deeplabcut:latest-gui
FROM $BUILD_FROM

ENV API_KEY="mysupersecretpassword"
ENV DLC_PROJECTS="/projects"

EXPOSE 8000

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
