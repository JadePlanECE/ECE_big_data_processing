FROM python:3.12
WORKDIR /lab4_good_practice
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY admin.py producer.py consumer.py ./