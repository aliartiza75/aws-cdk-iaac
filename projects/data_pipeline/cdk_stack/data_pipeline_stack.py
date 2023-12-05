import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda_event_sources as eventsources,
    aws_lambda_destinations as destinations
)

from aws_cdk import aws_codedeploy as codedeploy


class dataPipeline(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ########################
        # ## lambdaA Rresource ###
        # ########################

        lambdaA_event_queue = sqs.Queue(self, "lambdaA_event_queue", visibility_timeout=cdk.Duration.minutes(10))

        # Defines an AWS Lambda resource
        lambdaA = _lambda.Function(self, 'lambdaA',
                                   runtime=_lambda.Runtime.PYTHON_3_10,
                                   code=_lambda.Code.from_asset('projects'),
                                   handler='data_pipeline.lambdaA.lambdaA.handler',
                                   timeout=cdk.Duration.minutes(5),
                                   on_success=destinations.SqsDestination(lambdaA_event_queue)
                                   )

        # EVENT BRIDGE
        rule = events.Rule(self, "Schedule Rule",
                           schedule=events.Schedule.cron(minute="*/1")
                           )
        rule.add_target(targets.LambdaFunction(lambdaA))

        # Codedeploy
        # application = codedeploy.LambdaApplication(self, "CodeDeployApplication", application_name=lambdaA.function_name)

        # version1_alias = _lambda.Alias(self, "alias",
        #                                alias_name="prod",
        #                                version=lambdaA.current_version
        #                                )

        # config = codedeploy.LambdaDeploymentConfig(self, "CustomConfig",
        #                                             traffic_routing=codedeploy.TimeBasedCanaryTrafficRouting(
        #                                                 interval=cdk.Duration.minutes(15),
        #                                                 percentage=5
        #                                             ),
        #                                             deployment_config_name="MyDeploymentConfig"
        #                                         )

        # deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
        #                                                     application=application,  # optional property: one will be created for you if not provided
        #                                                     alias=version1_alias,
        #                                                     deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
        #                                                 )

        # ########################
        # ## lambdaB Rresource ###
        # ########################

        bucket = s3.Bucket(self, "lambdaB_logs")
        # lambdaV_validator_event_queue = sqs.Queue(self, "lambdaV_validator_event_queue", visibility_timeout=cdk.Duration.minutes(10))
        lambdaB_role = iam.Role(self, "lambdaB_role",
                                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
                                )

        lambdaB = _lambda.Function(self, 'lambdaB',
                                   runtime=_lambda.Runtime.PYTHON_3_10,
                                   code=_lambda.Code.from_asset('projects'),
                                   handler='data_pipeline.lambdaB.lambdaB.handler',
                                   timeout=cdk.Duration.minutes(5),
                                   environment={"INVOKE_FUNCTION_NAME": lambdaA.function_name,
                                                "LOG_BUCKET": bucket.bucket_name
                                                },
                                   role=lambdaB_role,
                                   )

        # Adding additional inline policies to the role
        lambdaB_role.add_to_policy(iam.PolicyStatement(resources=["*"],
                                                       actions=["lambda:*"]
                                                       )
                                   )
        lambdaB_role.add_to_policy(iam.PolicyStatement(resources=["*"],  # NOTE ONLY ADD putObject policy later
                                                       actions=["s3:*"]
                                                       )
                                   )
        lambdaB_role.add_to_policy(iam.PolicyStatement(resources=["*"],
                                                       actions=["kms:GenerateDataKey"]
                                                       )
                                   )
        # Adding SQS as lambda's event source
        lambdaB.add_event_source(eventsources.SqsEventSource(lambdaA_event_queue))
