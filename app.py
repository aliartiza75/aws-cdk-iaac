#!/usr/bin/env python3

import aws_cdk as cdk


# Data pipeline constructs

from projects.data_pipeline.cdk_stack.data_pipeline_stack import dataPipeline

# API constructs
from projects.api.lambdaPost.lambdaPost_stack import lambdaPost



app = cdk.App()



lambdaPost(app, "lambdaPost")
dataPipeline(app, "dataPipeline")

app.synth()
