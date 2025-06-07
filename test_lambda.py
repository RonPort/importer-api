# test_lambda.py
from process_files import lambda_handler

event = {
    "source_bucket": "vidalung.test",
    "prefix": "uploads/",
    "zip_key": "compressions/all_images.zip",
    "target_bucket": "vidalung.test"  # Optional, can be the same as source_bucket
}
context = {}  # You can leave this empty for most tests

result = lambda_handler(event, context)
print(result)