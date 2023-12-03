import os
import boto3
import json
from typing import Any
import datetime as dt
lambda_client = boto3.client('lambda')



INVOKE_FUNCTION_NAME = os.environ['INVOKE_FUNCTION_NAME']
LOG_BUCKET = os.environ['LOG_BUCKET']


def save_to_s3(data: dict[str, Any], filename: str):
    """Save data to the s3 bucket.

    Parameters
    ----------
    data: dict[str, Any]
        The data to save to s3 bucket.
    filename: str
        The full object name for the file.
    """
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=LOG_BUCKET,
        Key=f"{filename}.json",
        Body=json.dumps(data)
    )


def handler(event, context):
    """Process order result."""


    response = (json.loads(event["Records"][0]['body'])["responsePayload"])

    
    if response["results"] == True:
        for order in response["orders"]:
            if order["status"] == "rejected":

                # Generate alert on Slack
                pass
            else:
                print("Storing in s3")
                save_to_s3(data=event, filename=f"orders/order_{dt.datetime.now(dt.timezone.utc).isoformat()}")
    else:
        # invoke lambda again
        print(INVOKE_FUNCTION_NAME)
        lambda_payload = {"test_event": True}
        lambda_client.invoke(FunctionName=INVOKE_FUNCTION_NAME, 
                     InvocationType='Event',
                     Payload=json.dumps(lambda_payload))