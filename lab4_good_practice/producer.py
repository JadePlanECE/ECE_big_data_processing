import os
import time
from confluent_kafka import Producer

bootstrap = os.getenv('BOOTSTRAP_SERVERS', 'localhost:9092')

conf = {'bootstrap.servers': bootstrap}
producer = Producer(conf)

topic = 'book'
book_path = os.getenv('BOOK_PATH', '/data/book.txt')

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")

with open(book_path, 'r', encoding='utf-8') as f:
    for line in f:
        producer.produce(
            topic=topic,
            value=line.rstrip('\n'),
            callback=delivery_report,
        )
        producer.poll(0)          # traite les callbacks de delivery
        time.sleep(0.01)          # léger débit pour la démo

# flush avec timeout : renvoie le nb de messages non acquittés
remaining = producer.flush(30)
if remaining:
    print(f"ATTENTION : {remaining} messages non flushés")
print("Producer terminé.")
# PAS de producer.close() : ça n'existe pas pour confluent_kafka.Producer