import os
import boto3
import json
from typing import Any
import datetime as dt

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
    print(type(data), data)
    data = (json.loads(event["Records"][0]["body"])["responsePayload"])
    print(type(data), data)

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    for order in data["orders"]:
        if order["status"] == "rejected":
            # raise ValueError("Order status is rejected!")
            # Generate alert on Slack
            pass
        else:
            print("Storing in s3")
            save_to_s3(data=event, filename=f"orders/order_{dt.datetime.now(dt.timezone.utc).isoformat()}")