#!/usr/bin/env python3
"""
Script para gerar dados Parquet e salvar no bucket landing-zone
Simulando dados de clientes do sistema Cloud X
"""

import boto3
import pandas as pd
from faker import Faker
import random
import time
import logging
import io

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do MinIO
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

# Configurar Faker para português brasileiro
fake = Faker('pt_BR')

def generate_fake_data_records(num_records):
    """Gera dados falsos de clientes"""
    records = []
    
    for _ in range(num_records):
        record = {
            'id': fake.uuid4(),
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'endereco': fake.address(),
            'cidade': fake.city(),
            'estado': fake.state(),
            'cep': fake.postcode(),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=80),
            'data_cadastro': fake.date_between(start_date='-2y', end_date='today'),
            'salario': round(random.uniform(1000, 15000), 2),
            'status': random.choice(['ATIVO', 'INATIVO', 'PENDENTE']),
            'empresa': fake.company(),
            'score_credito': random.randint(300, 850),
            'limite_credito': round(random.uniform(1000, 50000), 2),
            'ultima_compra': fake.date_between(start_date='-1y', end_date='today'),
            'total_compras': round(random.uniform(0, 100000), 2),
            'categoria': random.choice(['PREMIUM', 'STANDARD', 'BASIC']),
            'canal_preferido': random.choice(['ONLINE', 'LOJA_FISICA', 'TELEFONE', 'APP'])
        }
        records.append(record)
    
    return records

def save_to_minio_bucket(data, bucket_name, file_path):
    """Salva dados no MinIO"""
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f'http://{MINIO_ENDPOINT}',
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name='us-east-1'
        )
        
        # Converter para DataFrame
        df = pd.DataFrame(data)
        
        # Converter DataFrame para Parquet em memória
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
        parquet_buffer.seek(0)
        
        # Upload para MinIO
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_path,
            Body=parquet_buffer.getvalue(),
            ContentType='application/octet-stream'
        )
        
        logger.info(f"Dados salvos em {bucket_name}/{file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        return False

def main():
    """Função principal"""
    logger.info("Iniciando geração de dados Parquet...")
    
    # Gerar número aleatório de registros
    num_records = random.randint(1000, 10000)
    logger.info(f"Número de registros a serem gerados: {num_records}")
    
    # Gerar dados falsos
    data = generate_fake_data_records(num_records)
    
    # Definir caminho do arquivo no bucket
    timestamp = int(time.time())
    file_path = f"dataway/cloud_x/clients/clients_data_{timestamp}.parquet"
    
    # Salvar no MinIO
    success = save_to_minio_bucket(data, "landing-zone", file_path)
    
    if success:
        logger.info("Processo concluído com sucesso!")
    else:
        logger.error("Erro no processo!")

if __name__ == "__main__":
    main()
