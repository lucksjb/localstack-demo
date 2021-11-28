import random
import os
import uuid
import json
import boto3
import logging
from dotenv import load_dotenv

# carrega as variaveis de ambiente
load_dotenv()

# configura um logger
logging.basicConfig(level=logging.INFO)

# obtem o servico sns
sns = boto3.client('sns', endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
# busca topico
topics = sns.list_topics()
for t in topics['Topics']:
    if os.getenv("SNS_TOPIC") in t['TopicArn']:
        topic = t['TopicArn']

# corpo da mensagem que será enviada para o topico
message = {
    'id': str(uuid.uuid4()),  # cria uma identificacao para mensagem
    'value': random.randint(1, 100)  # atribui um valor para mensagem
}
# converte a mensagem para o formato JSON
serialized_msg = json.dumps(message)

# Publica a mensagem no topico
response = sns.publish(TopicArn=topic, Message=serialized_msg)
logging.info(
    f'Mensagem [{message["id"]}] publicada no topico [{os.getenv("SNS_TOPIC")}]')
