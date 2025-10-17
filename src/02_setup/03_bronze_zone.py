#!/usr/bin/env python3
"""
Script para gerar dados CSV no bucket bronze-zone
Dados limpos e estruturados do sistema Protheus
"""

import boto3
import pandas as pd
from faker import Faker
import random
import time
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do MinIO
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

# Configurar Faker para português brasileiro
fake = Faker('pt_BR')

def generate_bronze_data(num_records):
    """Gera dados limpos e estruturados para bronze zone"""
    records = []
    
    for _ in range(num_records):
        record = {
            'cliente_id': fake.uuid4(),
            'nome_completo': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'endereco_completo': fake.address(),
            'cidade': fake.city(),
            'estado': fake.state(),
            'cep': fake.postcode(),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
            'data_cadastro': fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
            'salario_mensal': round(random.uniform(2000, 15000), 2),
            'status_cliente': random.choice(['ATIVO', 'INATIVO', 'SUSPENSO']),
            'empresa': fake.company(),
            'cargo': fake.job(),
            'data_atualizacao': time.strftime('%Y-%m-%d %H:%M:%S')
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
        
        # Converter para DataFrame e depois CSV
        df = pd.DataFrame(data)
        csv_content = df.to_csv(index=False, encoding='utf-8')
        
        # Upload para MinIO
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_path,
            Body=csv_content.encode('utf-8'),
            ContentType='text/csv'
        )
        
        logger.info(f"Dados salvos em {bucket_name}/{file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        return False

def main():
    """Função principal"""
    logger.info("Iniciando geração de dados para Bronze Zone...")
    
    # Gerar número aleatório de registros
    num_records = random.randint(2000, 8000)
    logger.info(f"Número de registros a serem gerados: {num_records}")
    
    # Gerar dados falsos
    data = generate_bronze_data(num_records)
    
    # Definir caminho do arquivo no bucket
    timestamp = int(time.time())
    file_path = f"processed/protheus/clients_bronze_{timestamp}.csv"
    
    # Salvar no MinIO
    success = save_to_minio_bucket(data, "bronze-zone", file_path)
    
    if success:
        logger.info("Processo concluído com sucesso!")
    else:
        logger.error("Erro no processo!")

if __name__ == "__main__":
    main()
