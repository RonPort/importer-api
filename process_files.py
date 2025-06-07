import boto3
import io
import zipfile
import logging
import os
import json

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET"),
    region_name=os.getenv("REGION"),
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event  # For direct invocation/testing

    source_bucket = body['source_bucket']
    prefix = body['prefix']
    zip_key = body['zip_key']
    target_bucket = body.get('target_bucket')

    paginator = s3.get_paginator('list_objects_v2')
    files = []
    for page in paginator.paginate(Bucket=source_bucket, Prefix=prefix):
        files.extend(
            [
                obj['Key'] for obj in page.get('Contents', [])
                    if not obj['Key'].endswith('/')
            ]
        )

    if not files:
        logger.error("No files found to zip.")
        raise Exception("No files found to zip.")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for key in files:
            try:
                logger.info(f"Adding {key} to archive...")
                obj = s3.get_object(Bucket=source_bucket, Key=key)
                # Read in chunks to avoid memory spikes
                with io.BytesIO(obj['Body'].read()) as file_data:
                    zipf.writestr(os.path.basename(key), file_data.getvalue())
            except Exception as e:
                logger.error(f"Failed to add {key}: {e}")

    zip_buffer.seek(0)

    try:
        s3.upload_fileobj(zip_buffer, target_bucket, zip_key)
        logger.info(f"ZIP uploaded to s3://{target_bucket}/{zip_key}")
    except Exception as e:
        logger.error(f"Failed to upload ZIP: {e}")
        raise

    return {
        'status': 'success',
        'file_count': len(files),
        'zip_key': zip_key
    }