import aws_cdk as core
import aws_cdk.assertions as assertions

# from projects.projects_stack import ProjectsStack

from projects.api.lambdaPost.lambdaPost_stack import lambdaPost



def test_lambda_created():
    app = core.App()
    stack = lambdaPost(app, "lambdaPost")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function",  {
            "Handler": "api.lambdaPost.lambdaPost.handler",
            "Runtime": "python3.10",
        })

def test_lambda_created_2():
    app = core.App()
    stack = lambdaPost(app, "lambdaPost")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Lambda::Function", 1)

# def test_lambda_apigateway_created():
#     app = core.App()
#     stack = lambdaPost(app, "lambdaPost")
#     template = assertions.Template.from_stack(stack)

#     template.resource_count_is("AWS::ApiGateway::LambdaRestApi", 1)

#     # template.has_resource_properties("AWS::ApiGateway::LambdaRestApi",  {
#     #         "Handler": "my_lambda",
#     #     })


# def test_sqs_queue_created():
#     app = core.App()
#     stack = ProjectsStack(app, "projects")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })


# def test_sns_topic_created():
#     app = core.App()
#     stack = ProjectsStack(app, "projects")
#     template = assertions.Template.from_stack(stack)

#     template.resource_count_is("AWS::SNS::Topic", 1)
