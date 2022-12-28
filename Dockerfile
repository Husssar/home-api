FROM python:3.10-slim-buster
COPY src/requirements.txt requirements.txt
WORKDIR /src

COPY . .
RUN pip install --no-cache-dir -r src/requirements.txt
RUN pip install cryptography
CMD [ "python", "src/server.py"]
