#!/usr/bin/env python3
"""
Script para criar buckets no MinIO seguindo o padrão de Data Lake
"""

import boto3
from botocore.exceptions import ClientError
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do MinIO
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

# Lista de buckets para criar seguindo o padrão de Data Lake
BUCKETS = [
    "landing-zone",  # Dados brutos que chegam
    "bronze-zone",   # Dados limpos, mas não processados
    "silver-zone",   # Dados processados e estruturados
    "gold-zone"      # Dados finais para consumo
]

def create_s3_client():
    """Cria cliente S3 para MinIO"""
    return boto3.client(
        's3',
        endpoint_url=f'http://{MINIO_ENDPOINT}',
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name='us-east-1'  # MinIO precisa de uma região
    )

def create_bucket(s3_client, bucket_name):
    """Cria um bucket no MinIO"""
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} created successfully.")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            logger.info(f"Bucket {bucket_name} already exists.")
            return True
        else:
            logger.error(f"Error creating bucket {bucket_name}: {e}")
            return False

def main():
    """Função principal para criar todos os buckets"""
    logger.info("Starting bucket creation process...")
    
    # Cria cliente S3
    s3_client = create_s3_client()
    
    # Cria cada bucket
    for bucket in BUCKETS:
        create_bucket(s3_client, bucket)
    
    logger.info("Bucket creation process completed!")

if __name__ == "__main__":
    main()
