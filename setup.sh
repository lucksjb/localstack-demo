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
