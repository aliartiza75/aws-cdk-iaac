import random
import boto3
_lambda = boto3.client('lambda')

def handler(event, context):



    """Generate event for results processing."""
    
    response = {
        "results": random.choice([True, False])
    }
    if response["results"]:
        response["orders"] = [
            {
                "status": "accepted",
                "power": 1,
            },
            {
                "status": "rejected",
                "power": 2,
            }
        ]
    return response