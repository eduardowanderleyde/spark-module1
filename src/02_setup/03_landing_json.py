#!/usr/bin/env python3
"""
Script para gerar dados JSON e salvar no bucket landing-zone
Simulando dados de clientes do sistema SAP
"""

import boto3
import json
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

def generate_fake_data_records(num_records):
    """Gera dados falsos de clientes"""
    records = []
    
    for _ in range(num_records):
        record = {
            'id': fake.uuid4(),
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'endereco': {
                'rua': fake.street_address(),
                'cidade': fake.city(),
                'estado': fake.state(),
                'cep': fake.postcode(),
                'pais': 'Brasil'
            },
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
            'data_cadastro': fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
            'salario': round(random.uniform(1000, 15000), 2),
            'status': random.choice(['ATIVO', 'INATIVO', 'PENDENTE']),
            'empresa': {
                'nome': fake.company(),
                'cnpj': fake.cnpj(),
                'setor': random.choice(['Tecnologia', 'Varejo', 'Saúde', 'Educação', 'Financeiro'])
            },
            'preferencias': {
                'comunicacao': random.choice(['email', 'telefone', 'sms']),
                'idioma': 'pt-BR',
                'newsletter': random.choice([True, False])
            }
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
        
        # Converter para JSON
        json_content = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Upload para MinIO
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_path,
            Body=json_content.encode('utf-8'),
            ContentType='application/json'
        )
        
        logger.info(f"Dados salvos em {bucket_name}/{file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        return False

def main():
    """Função principal"""
    logger.info("Iniciando geração de dados JSON...")
    
    # Gerar número aleatório de registros
    num_records = random.randint(1000, 10000)
    logger.info(f"Número de registros a serem gerados: {num_records}")
    
    # Gerar dados falsos
    data = generate_fake_data_records(num_records)
    
    # Definir caminho do arquivo no bucket
    timestamp = int(time.time())
    file_path = f"dataway/sap/clients/clients_data_{timestamp}.json"
    
    # Salvar no MinIO
    success = save_to_minio_bucket(data, "landing-zone", file_path)
    
    if success:
        logger.info("Processo concluído com sucesso!")
    else:
        logger.error("Erro no processo!")

if __name__ == "__main__":
    main()
