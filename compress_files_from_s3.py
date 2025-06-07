import os
import requests
import json

from fastapi.responses import JSONResponse
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(
    aws_access_key=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET"),
    aws_host='blf5646mpt5tvestxynevyoplu0fjlcq.lambda-url.us-east-1.on.aws',
    aws_region=os.getenv("REGION"),
    aws_service='lambda'
)

async def compress_files():
    LAMBDA_FUNCTION_URL = os.getenv("LAMBDA_FUNCTION_URL")
    payload = {
        'source_bucket': 'vidalung.test',
        'prefix': 'uploads/',
        'zip_key': 'compressions/all_images.zip',
        'target_bucket': 'vidalung.test'
    }
    try:
        response = requests.post(
            LAMBDA_FUNCTION_URL,
            auth=auth,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return JSONResponse({"status": "started", "lambda_response": response.json()})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)