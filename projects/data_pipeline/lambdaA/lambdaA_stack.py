import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda
)

import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets


import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_lambda_event_sources as eventsources

# # from aws_cdk import aws_cdk.aws_lambda_destinations.SqsDestination
# from aws_cdk import aws_lambda
# from aws_lambda import aws_lambda_destinations as destinations


# # _lambda import aws_lambda_destinations as destinations
from aws_cdk import aws_lambda_destinations as destinations

class lambdaA(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambdaA_event_queue = sqs.Queue(self, "lambdaA_event_queue")

        # Defines an AWS Lambda resource
        lambda_a = _lambda.Function(
            self, 'lambdaA',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('projects'),
            handler='data_pipeline.lambdaA.lambdaA.handler',
            timeout=cdk.Duration.minutes(5),
            on_success=destinations.SqsDestination(lambdaA_event_queue)
        )

        #### EVENT BRIDGE
        rule = events.Rule(self, "Schedule Rule",
                           schedule=events.Schedule.cron(minute="*/1")
                           )
        rule.add_target(targets.LambdaFunction(lambda_a))

        #### SECOND LAMBDA
        lambda_b = _lambda.Function(
            self, 'lambdaB',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('projects'),
            handler='data_pipeline.lambdaB.lambdaB.handler',
            timeout=cdk.Duration.minutes(0.1),
            environment={ # ADD THIS, FILL IT FOR ACTUAL VALUE 
               "LOG_BUCKET": "test",
            }
        )
        lambda_b.add_event_source(eventsources.SqsEventSource(lambdaA_event_queue))






