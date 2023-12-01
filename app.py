#!/usr/bin/env python3

import aws_cdk as cdk


# Data pipeline constructs
from projects.data_pipeline.lambdaA.lambdaA_stack import lambdaA
from projects.data_pipeline.lambdaB.lambdaB_stack import lambdaB

# API constructs
from projects.api.lambdaPost.lambdaPost_stack import lambdaPost



app = cdk.App()


lambdaA(app, "lambdaA")
lambdaB(app, "lambdaB")
lambdaPost(app, "lambdaPost")

app.synth()
