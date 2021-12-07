# LocalStack Demo

Demonstração do artigo [Simulando serviços AWS na sua máquina com LocalStack](https://www.linkedin.com/feed/update/urn:li:ugcPost:6868562263935090688?updateEntityUrn=urn%3Ali%3Afs_updateV2%3A%28urn%3Ali%3AugcPost%3A6868562263935090688%2CFEED_DETAIL%2CEMPTY%2CDEFAULT%2Cfalse%29).

![Arquitetura do projeto!](/img/arc.png "Arquitetura do projeto")

## Pré-requisitos

- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org)

## Inicie os containers

Inicie os containers docker.

```bash
docker-compose up
```

> Os serviços dynamodb, s3, sqs e sns estarão disponíveis na porta `4566`.

Cheque a saúde dos serviços.

```bash
curl http://localhost:4566/health
```

A resposta deve ser algo como:

```json
{
  "features": {
    "initScripts": "initialized"
  },
  "services": {
    "dynamodb": "running",
    "s3": "running",
    "sns": "running",
    "sqs": "running"
  }
}
```

## Crie um ambiente de desenvolvimento

Crie e ative o ambiente virtual python.

```bash
python3 -m venv venv # cria o ambiente
source venv/bin/activate # ativa o ambiente
```

Instale as depencencias através do [pip](https://pypi.org/project/pip).

```bash
pip install -r requirements.txt
```

## Crie os recursos no LocalStack

Instale a [Interface da Linha de Comando da AWS](https://aws.amazon.com/pt/cli/) e execute os comandos abaixo.

```bash
# Cria a fila com o nome FILA_DYNAMO
aws sqs create-queue --queue-name FILA_DYNAMO --endpoint-url=http://localhost:4566

# Cria a fila com o nome FILA_S3
aws sqs create-queue --queue-name FILA_S3 --endpoint-url=http://localhost:4566

# Cria o topico com o nome TOPICO_MENSAGENS
aws sns create-topic --name TOPICO_MENSAGENS --endpoint-url=http://localhost:4566

# Cria uma assinatura entre a fila FILA_DYNAMO e o topico TOPICO_MENSAGENS
aws sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:TOPICO_MENSAGENS --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:FILA_DYNAMO --endpoint-url=http://localhost:4566

# Cria uma assinatura entre a fila FILA_S3 e o topico TOPICO_MENSAGENS
aws sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:TOPICO_MENSAGENS --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:FILA_S3 --endpoint-url=http://localhost:4566

# Cria um bucket s3 com nome bucket-mensagens
aws s3api create-bucket --bucket bucket-mensagens --region us-east-1 --endpoint-url=http://localhost:4566

# Cria uma tabela no dynamodb com nome TabelaMensagens
aws dynamodb create-table --table-name TabelaMensagens --attribute-definitions AttributeName​=id,AttributeType=S --key-schema AttributeName​=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url=http://localhost:4566
```

ou execute o script abaixo:

```bash
python setup.py
```

## Produzindo mensagens no tópico SNS

Para publicar mensagens no tópico, execute o script abaixo:

```bash
python sns_producer.py
```

## Consumindo mensagens e adicionando no DynamoDB

Para consumidor e inserir as mensagens em uma tabela do DynamoDB, execute o comando abaixo:

```bash
python dynamo_sqs_consumer.py
```

## Consumindo mensagens e subindo para o S3

Para consumir e subir o conteúdo das mensagens para um bucket, execute o script abaixo:

```bash
python s3_sqs_consumer.py 
```

## Interfaces gráficas

- [DynamoDB admin](https://github.com/aaronshaf/dynamodb-admin)
- [aws-sqs-sns-client](https://github.com/ajyounguk/aws-sqs-sns-client)
- [localstack-s3-ui](https://github.com/rayhaanbhikha/localstack-s3-ui/blob/master/example/README.md) 



## Minhas anotações
acessar porta 4566
dynamodb-local 
localstack-s3
aws-sqs-client 
https://getcommandeer.com/localstack

https://www.linkedin.com/pulse/simulando-servi%25C3%25A7os-aws-na-sua-m%25C3%25A1quina-com-localstack-james-g-silva/?trackingId=gcHm3DFdTTOA6WkgoAMHJQ%3D%3D



