import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)


class lambdaPost(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(self, 'lambdaPost',
                                     runtime=_lambda.Runtime.PYTHON_3_10,
                                     code=_lambda.Code.from_asset('projects'),
                                     handler='api.lambdaPost.lambdaPost.handler',
                                     environment={"DYNAMODB_TABLE_NAME": "test",
                                                  },
                                     timeout=cdk.Duration.minutes(5)
                                     )

        api_gateway = apigateway.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
        )
