#!/usr/bin/env python3
"""
Script para gerar dados Parquet no bucket gold-zone
Dados finais otimizados para consumo do sistema Cloud X
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

def generate_gold_data(num_records):
    """Gera dados finais otimizados para gold zone"""
    records = []
    
    for _ in range(num_records):
        # Dados calculados e enriquecidos
        salario = round(random.uniform(4000, 25000), 2)
        idade = random.randint(25, 65)
        
        record = {
            'cliente_id': fake.uuid4(),
            'nome_completo': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'idade': idade,
            'faixa_etaria': 'JOVEM' if idade < 30 else 'ADULTO' if idade < 50 else 'SENIOR',
            'cidade': fake.city(),
            'estado': fake.state(),
            'regiao': random.choice(['NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUDESTE', 'SUL']),
            'salario_bruto': salario,
            'faixa_salarial': 'BAIXA' if salario < 5000 else 'MEDIA' if salario < 10000 else 'ALTA',
            'empresa': fake.company(),
            'cargo': fake.job(),
            'setor': random.choice(['Tecnologia', 'Varejo', 'Saúde', 'Educação', 'Financeiro', 'Industrial']),
            'score_credito': random.randint(400, 850),
            'categoria_risco': 'BAIXO' if random.randint(400, 850) > 700 else 'MEDIO' if random.randint(400, 850) > 600 else 'ALTO',
            'limite_credito': round(random.uniform(2000, 100000), 2),
            'total_compras_ano': round(random.uniform(0, 150000), 2),
            'ticket_medio': round(random.uniform(50, 5000), 2),
            'frequencia_compras': random.randint(1, 52),
            'ultima_compra': fake.date_between(start_date='-1y', end_date='today'),
            'status_cliente': random.choice(['ATIVO', 'INATIVO', 'POTENCIAL']),
            'segmento_cliente': random.choice(['PREMIUM', 'STANDARD', 'BASIC', 'VIP']),
            'canal_preferido': random.choice(['DIGITAL', 'FISICO', 'HIBRIDO']),
            'propensao_compra': round(random.uniform(0, 1), 3),
            'valor_vida_cliente': round(random.uniform(1000, 500000), 2),
            'data_cadastro': fake.date_between(start_date='-3y', end_date='today'),
            'dias_desde_cadastro': random.randint(1, 1095),
            'data_ultima_atualizacao': time.strftime('%Y-%m-%d %H:%M:%S'),
            'origem_dados': 'CLOUD_X',
            'versao_dados': '2.0'
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
    logger.info("Iniciando geração de dados para Gold Zone...")
    
    # Gerar número aleatório de registros
    num_records = random.randint(1000, 4000)
    logger.info(f"Número de registros a serem gerados: {num_records}")
    
    # Gerar dados falsos
    data = generate_gold_data(num_records)
    
    # Definir caminho do arquivo no bucket
    timestamp = int(time.time())
    file_path = f"analytics/cloud_x/clients_gold_{timestamp}.parquet"
    
    # Salvar no MinIO
    success = save_to_minio_bucket(data, "gold-zone", file_path)
    
    if success:
        logger.info("Processo concluído com sucesso!")
    else:
        logger.error("Erro no processo!")

if __name__ == "__main__":
    main()
