FROM python:3-alpine

# Add your instructions to dockerize the application
# App must run on port 8000
WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8000

CMD ["python3", "src/api.py"]



