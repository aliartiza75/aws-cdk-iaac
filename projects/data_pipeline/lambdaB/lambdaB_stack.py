from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)

class lambdaB(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'lambdaB',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('projects'),
            handler='lambdaB.lambdaB.handler',
        )