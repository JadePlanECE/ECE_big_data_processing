import os
import re
import string
from confluent_kafka import Consumer, KafkaError

bootstrap = os.getenv('BOOTSTRAP_SERVERS', 'localhost:9092')
out_path = os.getenv('OUTPUT_PATH', '/data/cleaned_book.txt')

conf = {'bootstrap.servers': bootstrap,
        'group.id': 'book-cleaners',
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
topic = 'book'
consumer.subscribe([topic])

MAX_EMPTY_POLLS = 30     # fin après ~30 s de silence (lecture d'un fichier = rapide)
MAX_ERRORS = 5
empty_polls = 0
error_count = 0
lines_written = 0

with open(out_path, 'w', encoding='utf-8') as out:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            empty_polls += 1
            if empty_polls >= MAX_EMPTY_POLLS:
                print("Fermeture : plus de messages.")
                break
            continue

        if msg.error():
            # fin de partition = normal, pas une vraie erreur
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            error_count += 1
            print(f"Consumer error: {msg.error()}")
            if error_count >= MAX_ERRORS:
                print("Fermeture : trop d'erreurs consécutives.")
                break
            continue

        empty_polls = 0
        error_count = 0

        # --- nettoyage basique du texte (inspiré du word count) ---
        text = msg.value().decode('utf-8', errors='replace')
        text = text.lower()                                  # minuscules
        text = text.translate(str.maketrans('', '', string.punctuation))  # ponctuation
        text = re.sub(r'\s+', ' ', text).strip()              # espaces multiples
        text = re.sub(r'[^a-z0-9 ]', '', text)                # caractères non alphanumériques

        if text:                                              # ignorer lignes vides
            out.write(text + '\n')
            lines_written += 1

consumer.close()
print(f"Terminé : {lines_written} lignes nettoyées écrites dans {out_path}")