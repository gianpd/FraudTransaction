"""Produce fake transactions into a Kafka topic."""

import os
from time import sleep
import json
import pandas as pd

from kafka import KafkaProducer
from transactions import create_random_transaction

TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND

###########################################
# Load Test Data
###########################################
df_test = pd.read_csv('dataset/test/df_test.csv')
X_test = df_test.iloc[:, :-1]

if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode()  # produce json msg

    )

    while True:
        transaction = create_random_transaction(X_test)
        producer.send(TRANSACTIONS_TOPIC, value=transaction)
        print(transaction)  # DEBUG
        #sleep(SLEEP_TIME)
        sleep(5)
