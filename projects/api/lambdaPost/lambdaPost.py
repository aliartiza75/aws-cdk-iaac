import logging
import json
import os
from typing import Any

logger = logging.getLogger()

TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']


def generate_response(status_code, message):
    """
    It will generate a response message

    Parameters
    -----------
    status_code:    [int] status code
    message:        [str] response message
    """
    
    return {
                "isBase64Encoded": False,
                "statusCode": status_code,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": message
    }



def save_to_db(records: list[dict[str, Any]]):
    """Save records to the DynamoDB table.

    Parameters
    ----------
    records: list[dict[str, Any]]
        The data to save to DynamoDB.
    """
    # saving records to the dynamoDB, let's assume it is successful
    logger.info("Records are successfully saved to the DB table %s.", TABLE_NAME)


def handler(event, context):
    """Process POST request to the API."""

    logger.info(
        'Received %s request to %s endpoint',
        event["httpMethod"],
        event["path"])

    if event["httpMethod"] == "POST":
    
        if (orders := event['body']) is not None:
            logger.info("Orders received: %s.", orders)
            save_to_db(records=orders)

            return generate_response(201, json.dumps({"message": "Record has been stored in DB"}))

        return generate_response(400, json.dumps({"errorMessage": "Request body is empty"}))
    
    else:

        return generate_response(400, json.dumps({"errorMessage": "Invalid HTTP Method"}))
