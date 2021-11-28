import json
import logging
import boto3
import os
from dotenv import load_dotenv

# carrega as variaveis de ambiente
load_dotenv()

# configura um logger
logging.basicConfig(level=logging.INFO)

# obtem o servico SQS e a URL da fila
sqs = boto3.client('sqs', endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
queue = sqs.get_queue_url(QueueName=os.getenv("DYNAMO_QUEUE"))

# obtem o servico DYNAMODB e a tabela
dynamodb = boto3.resource(
    'dynamodb', endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))

# puxa/recebe mensagens da fila
response = sqs.receive_message(
    QueueUrl=queue['QueueUrl'], MaxNumberOfMessages=2)
if 'Messages' in response:
    for message in response['Messages']:
        logging.info(f'Mensagem [{message["MessageId"]}] recebida')
        # converte o corpo da mensagem JSON em um dicionario python
        body = json.loads(message['Body'])
        # converte a mensagem JSON em um dicionario python
        msg = json.loads(body["Message"])
        # adiciona pedido na tabela
        table.put_item(Item=msg)
        # remove a mensagem da fila
        sqs.delete_message(
            QueueUrl=queue['QueueUrl'], ReceiptHandle=message['ReceiptHandle'])
        logging.info(
            f'Mensagem [{msg["id"]}] adicionada a tabela [{os.getenv("DYNAMO_TABLE")}]')
else:
    logging.info('nenhuma mensagem recebida')
