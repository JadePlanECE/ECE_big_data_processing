from confluent_kafka.admin import AdminClient, NewTopic

bootstrap = __import__('os').getenv('BOOTSTRAP_SERVERS', 'localhost:9092')

config = {'bootstrap.servers': bootstrap}
admin_client = AdminClient(config)

topic = 'book'

# create_topics est ASYNCHRONE : on récupère des futures et on les attend
futures = admin_client.create_topics(
    [NewTopic(topic, num_partitions=1, replication_factor=1)]
)

for t, future in futures.items():
    try:
        future.result()   # attend la création effective
        print(f"Topic '{t}' créé.")
    except Exception as e:
        if 'already exists' in str(e).lower():
            print(f"Topic '{t}' existait déjà.")
        else:
            print(f"Échec création topic '{t}': {e}")

# vérification
for t in sorted(admin_client.list_topics().topics.keys()):
    print("Topic visible :", t)