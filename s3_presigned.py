import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import boto3
from botocore.exceptions import ClientError

router = APIRouter()

@router.get("/generate-presigned-url/")
def generate_presigned_url(object_name: str):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET"),
        region_name=os.getenv("REGION"),
    )
    try:
        url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": os.getenv("S3_BUCKET"), "Key": object_name,  "ContentType": "application/octet-stream",},
            ExpiresIn=3600,
        )
        return JSONResponse({"url": url})
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))