import json
import os
import io
import logging
import boto3
from dotenv import load_dotenv

# carrega as variaveis de ambiente
load_dotenv()

# configura um logger
logging.basicConfig(level=logging.INFO)

# obtem um cliente para integrar com servico SQS, e a URL da fila
sqs = boto3.client('sqs', endpoint_url=os.getenv('AWS_ENDPOINT_URL'))
queue = sqs.get_queue_url(QueueName=os.getenv('S3_QUEUE'))

# obtem um cliente para integrar com servico S3
s3 = boto3.client('s3', endpoint_url=os.getenv('AWS_ENDPOINT_URL'))

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
        # sobe o arquivo para o bucket
        with io.BytesIO() as f:
            f.write(str(msg['value']).encode('utf-8'))
            f.seek(0)
            s3.upload_fileobj(f, Bucket=os.getenv(
                'S3_BUCKET'), Key=f'orders-{msg["id"]}')
        # remove a mensagem da fila
        sqs.delete_message(
            QueueUrl=queue['QueueUrl'], ReceiptHandle=message['ReceiptHandle'])
        print(
            f'Mensagem [{msg["id"]}] salva no bucket [{os.getenv("S3_BUCKET")}]')
else:
    logging.info('nenhuma mensagem recebida')
