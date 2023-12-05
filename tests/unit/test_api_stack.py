import aws_cdk as core
import aws_cdk.assertions as assertions

from projects.api.lambdaPost.lambdaPost_stack import lambdaPost


def test_lambda_created():
    app = core.App()
    stack = lambdaPost(app, "lambdaPost")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function", {"Handler": "api.lambdaPost.lambdaPost.handler",
                                                               "Runtime": "python3.10",
                                                               }
                                     )


def test_lambda_created_2():
    app = core.App()
    stack = lambdaPost(app, "lambdaPost")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::Function", 1)
