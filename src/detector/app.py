"""detector app: it must classify a transaction as fraud or normal."""

import json
import os
import logging
import torch
import pandas as pd
from kafka import KafkaConsumer, KafkaProducer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s : %(message)s',
                    datefmt='%d/%m/%Y %H:%M ',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
LEGIT_TOPIC = os.environ.get('LEGIT_TOPIC')
FRAUD_TOPIC = os.environ.get('FRAUD_TOPIC')

####################################
# Load Pytorch Model
####################################
model = torch.load('model/model_1.pt')
model.eval()

def classify_transaction(transaction):
    """classify the transaction by using the pre-trained model"""

    return transaction['Amount'] >= 900



if __name__ == '__main__':
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    for message in consumer:
        transaction = message.value
        topic = FRAUD_TOPIC if classify_transaction(transaction) else LEGIT_TOPIC
        producer.send(topic, value=transaction)
        logger.info(f'Topic: {topic}, Transaction: {transaction}')
