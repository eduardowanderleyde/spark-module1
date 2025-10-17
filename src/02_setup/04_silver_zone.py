#!/usr/bin/env python3
"""
Script para gerar dados JSON no bucket silver-zone
Dados processados e enriquecidos do sistema SAP
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

def generate_silver_data(num_records):
    """Gera dados processados e enriquecidos para silver zone"""
    records = []
    
    for _ in range(num_records):
        # Dados base
        nome = fake.name()
        email = fake.email()
        
        record = {
            'cliente_id': fake.uuid4(),
            'dados_pessoais': {
                'nome_completo': nome,
                'email_principal': email,
                'telefone_principal': fake.phone_number(),
                'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
                'genero': random.choice(['M', 'F', 'O']),
                'estado_civil': random.choice(['SOLTEIRO', 'CASADO', 'DIVORCIADO', 'VIUVO'])
            },
            'endereco': {
                'logradouro': fake.street_address(),
                'bairro': fake.city_suffix(),
                'cidade': fake.city(),
                'estado': fake.state(),
                'cep': fake.postcode(),
                'pais': 'Brasil',
                'tipo_endereco': random.choice(['RESIDENCIAL', 'COMERCIAL', 'CORRESPONDENCIA'])
            },
            'dados_profissionais': {
                'empresa': fake.company(),
                'cargo': fake.job(),
                'salario_bruto': round(random.uniform(3000, 20000), 2),
                'data_admissao': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
                'setor': random.choice(['Tecnologia', 'Varejo', 'Saúde', 'Educação', 'Financeiro', 'Industrial'])
            },
            'preferencias_cliente': {
                'canal_preferido': random.choice(['EMAIL', 'SMS', 'WHATSAPP', 'TELEFONE']),
                'idioma': 'pt-BR',
                'recebe_promocoes': random.choice([True, False]),
                'tipo_produto_interesse': random.choice(['Tecnologia', 'Roupas', 'Casa', 'Esportes', 'Livros'])
            },
            'metadados': {
                'data_cadastro': fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
                'data_ultima_atualizacao': time.strftime('%Y-%m-%d %H:%M:%S'),
                'origem_dados': 'SAP',
                'versao_dados': '1.0',
                'status_processamento': 'PROCESSADO'
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
    logger.info("Iniciando geração de dados para Silver Zone...")
    
    # Gerar número aleatório de registros
    num_records = random.randint(1500, 6000)
    logger.info(f"Número de registros a serem gerados: {num_records}")
    
    # Gerar dados falsos
    data = generate_silver_data(num_records)
    
    # Definir caminho do arquivo no bucket
    timestamp = int(time.time())
    file_path = f"enriched/sap/clients_silver_{timestamp}.json"
    
    # Salvar no MinIO
    success = save_to_minio_bucket(data, "silver-zone", file_path)
    
    if success:
        logger.info("Processo concluído com sucesso!")
    else:
        logger.error("Erro no processo!")

if __name__ == "__main__":
    main()
