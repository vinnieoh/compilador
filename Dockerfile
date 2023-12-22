FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip

EXPOSE 5000

CMD ["python", "main.py"]
