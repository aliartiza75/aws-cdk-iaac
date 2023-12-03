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

import aws_cdk.aws_iam as iam

import aws_cdk.aws_s3 as s3


# # from aws_cdk import aws_cdk.aws_lambda_destinations.SqsDestination
# from aws_cdk import aws_lambda
# from aws_lambda import aws_lambda_destinations as destinations


# # _lambda import aws_lambda_destinations as destinations
from aws_cdk import aws_lambda_destinations as destinations

class dataPipeline(Stack):

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


        ########################
        ##### LAMBDA VALIDATOR
        ########################
        bucket = s3.Bucket(self, "lambdaB_logs")
        # lambdaV_validator_event_queue = sqs.Queue(self, "lambdaV_validator_event_queue", visibility_timeout=cdk.Duration.minutes(10))
        lambdaValidation_role = iam.Role(self, "lambdaValidation_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        print(dir(lambda_a))
        lambda_validator = _lambda.Function(
            self, 'lambdaValidator',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('projects'),
            handler='data_pipeline.lambdaValidator.lambdaValidator.handler',
            timeout=cdk.Duration.minutes(5),
            environment={
                "INVOKE_FUNCTION_NAME": lambda_a.function_name,
                "LOG_BUCKET": bucket.bucket_name
            },
            role=lambdaValidation_role,
            # on_success=destinations.SqsDestination(lambdaV_validator_event_queue)
        )
        lambdaValidation_role.add_to_policy(iam.PolicyStatement(resources=["*"],
                                              actions=["lambda:*"]
                            ))
        lambdaValidation_role.add_to_policy(iam.PolicyStatement(resources=["*"],  # NOTE ONLY ADD putObject policy later
                                              actions=["s3:*"]
                            ))
        lambdaValidation_role.add_to_policy(iam.PolicyStatement(resources=["*"],
                                              actions=["kms:GenerateDataKey"]
                            ))
        lambda_validator.add_event_source(eventsources.SqsEventSource(lambdaA_event_queue))





















        ###################
        ####  LAMBDA B
        ###################
        # bucket = s3.Bucket(self, "lambdaB_logs")
        # my_role = iam.Role(self, "lambdaBRole",
        #     assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        # )


        # lambda_b = _lambda.Function(
        #     self, 'lambdaB',
        #     runtime=_lambda.Runtime.PYTHON_3_10,
        #     code=_lambda.Code.from_asset('projects'),
        #     handler='data_pipeline.lambdaB.lambdaB.handler',
        #     timeout=cdk.Duration.minutes(5),
        #     environment={ # ADD THIS, FILL IT FOR ACTUAL VALUE 
        #        "LOG_BUCKET": bucket.bucket_name,
        #     },
        #     role=my_role
        # )

        # my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        # my_role.add_to_policy(iam.PolicyStatement(resources=["*"],  # NOTE ONLY ADD putObject policy later
        #                                       actions=["s3:*"]
        #                     ))
        # my_role.add_to_policy(iam.PolicyStatement(resources=["*"],
        #                                       actions=["kms:GenerateDataKey"]
        #                     ))

        # lambda_b.add_event_source(eventsources.SqsEventSource(lambdaV_validator_event_queue))






