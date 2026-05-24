FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
