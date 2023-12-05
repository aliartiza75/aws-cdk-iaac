import aws_cdk as core
import aws_cdk.assertions as assertions

from projects.data_pipeline.cdk_stack.data_pipeline_stack import dataPipeline

def test_lambda_a_created():
    app = core.App()
    stack = dataPipeline(app, "dataPipeline")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function",  {
            "Handler": "data_pipeline.lambdaA.lambdaA.handler",
            "Runtime": "python3.10",
        })

def test_lambda_created_2():
    app = core.App()
    stack = dataPipeline(app, "dataPipeline")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::Function", 2)

def test_s3_created():
    app = core.App()
    stack = dataPipeline(app, "dataPipeline")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::S3::Bucket", 1)

def test_eventbridge_created():
    app = core.App()
    stack = dataPipeline(app, "dataPipeline")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Events::Rule", 1)

def test_iam_created():
    app = core.App()
    stack = dataPipeline(app, "dataPipeline")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::IAM::Role", 2)
