
# AWS CDK IaaC


## 
The repository contains the manifests to create AWS resource for 

1. API
2. Data Pipeline



## Overview

### Folder Structure

```bash
├── app.py
├── cdk.json
├── LICENSE
├── projects
│   ├── api                                                     # It contains the manifest for the Lambda API
│   │   └── lambdaPost
│   │       ├── lambdaPost.py                                   # It contains the code for lambda API
│   │       └── lambdaPost_stack.py                             # It contains the constructs for the lambda API
│   ├── data_pipeline                                           # It contains the manifest for the data pipeline
│   │   ├── cdk_stack
│   │   │   └── data_pipeline_stack.py                          # it contains the constructs for the Data Pipeline
│   │   ├── lambdaA
│   │   │   └── lambdaA.py                                      # it contains the code for LambdaA
│   │   └── lambdaB
│   │       └── lambdaB.py                                      # It contains the code for LambdaB
│   └── __init__.py
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg                                                   # It contains the configuration for the pycodestyle.
└── tests                                                       # it contains the unit test for the api and data_pipeline stack contructs
    ├── __init__.py
    └── unit
        ├── __init__.py
        ├── test_api_stack.py
        └── test_data_pipeline_stack.py

```


### Dependencies / Pre-requisites

1. Install node.js and npm.

2. Install aws-cdk cli:
```bash
$ sudo npm install -g aws-cdk
```
3. Install pip3.

4. Install python packages:

```
$ sudo pip3 install -r requirements-dev.txt
```

5. Confiure AWS Credentials

**NOTE** For github actions configure action secret for AWS ACCESS_KEY, ACCESS_SECRET and REGION.

### Code Logic

#### API

It is a simple lambda exposed via API Gateway.

#### Data Pipeline

In data pipeline, lambdaA is triggerd by an event after 1 minute. If lambda is able to process the event it will forward the event to an SQS queue. lambdaB will receive the event, if the result is true, the event will be processed an stored in a S3 bucket. If the result is false, it will re invoke the lambdaA.


### Details

1. To deploy the resources

```bash
cdk bootstrap
cdk deploy --all
```

2. To run tests

```
pytest
```

3. To destroy resource
```bash
cdk destroy --all
```

