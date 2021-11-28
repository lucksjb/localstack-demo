import os
import logging
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# carrega as variaveis de ambiente
load_dotenv()

# configura um logger
logging.basicConfig(level=logging.INFO)

# obtem os recursos da aws
sqs = boto3.client('sqs', endpoint_url=os.environ['AWS_ENDPOINT_URL'])
sns = boto3.client('sns', endpoint_url=os.environ['AWS_ENDPOINT_URL'])
dynamodb = boto3.resource(
    'dynamodb', endpoint_url=os.environ['AWS_ENDPOINT_URL'])
s3 = boto3.client('s3', endpoint_url=os.environ['AWS_ENDPOINT_URL'])


def create_topic(topic: str) -> str:
    """Cria um tópico no SNS
    :param topic: Nome do tópico
    :return: O endereço do tópico criado
    """
    response = sns.create_topic(Name=topic)
    logging.info(f'Tópico [{topic}] criado.')
    return response['TopicArn']


def create_queue(queue: str) -> str:
    """Cria uma fila no SQS
    :param queue: Nome da fila
    :return: O endereço da fila criada
    """
    response = sqs.create_queue(QueueName=queue)
    logging.info(f'Fila [{queue}] criada.')
    return response['QueueUrl']


def subscribe_topic(topic: str, queue: str):
    """Cria uma assinatura entre um tópico e uma fila
    :param topic: Endereço do tópico
    :param queue: Endereço da fila
    """
    sns.subscribe(
        TopicArn=topic,
        Protocol='sqs',
        Endpoint=queue,
        ReturnSubscriptionArn=True
    )
    logging.info(
        f'Assinatura entre o topico [{topic}] e a fila [{queue}] realizada.')


def create_table(table):
    try:
        dynamodb.create_table(
            TableName=table,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        logging.info(f'Tabela [{table}] criada.')
    except ClientError as e:
        logging.error(e)


def create_bucket(bucket):
    try:
        s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={
                'LocationConstraint': os.environ['AWS_DEFAULT_REGION']
            },
        )
        logging.info(f'Bucket [{bucket}] criado.')
    except ClientError as e:
        logging.error(e)


def get_topic(topic: str) -> str:
    """Busca um tópico no SNS
    :param topic: Nome do tópico
    :return: O endereço do tópico encontrado
    """
    topics = sns.list_topics()
    for t in topics['Topics']:
        if topic in t['TopicArn']:
            logging.info(f'Tópico [{topic}] encontrado.')
            return t['TopicArn']


if __name__ == '__main__':
    topic = create_topic(os.environ['SNS_TOPIC'])
    dynamo_queue = create_queue(os.environ['DYNAMO_QUEUE'])
    s3_queue = create_queue(os.environ['S3_QUEUE'])
    subscribe_topic(topic, dynamo_queue)
    subscribe_topic(topic, s3_queue)
    create_table(os.environ['DYNAMO_TABLE'])
    create_bucket(os.environ['S3_BUCKET'])
