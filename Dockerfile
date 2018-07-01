FROM python:2.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get install -y libpq-dev \
    && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "server.py"]
