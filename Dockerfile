# Dockerfile
FROM python:3.11
COPY requirements.txt requirements.txt
RUN python3 -m venv /opt/env
RUN . /opt/env/bin/activate
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . code
WORKDIR /code
EXPOSE 8888
ENTRYPOINT ["python3", "gem/manage.py"]
CMD ["runserver", "0.0.0.0:8888"]
