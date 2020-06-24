#!/usr/bin/env python3

from aws_cdk import core

from resources.custom_lambda import CustomLambdaStack
from resources.dynamodb_stack import CustomDynamoDbStack
from resources.lambda_privileges import LmabdaPrivileges
from resources.custom_apig import CustomApig

app = core.App()

# CustomLambdaStack(app, "s05-custom-lambda")
# CustomDynamoDbStack(app, "s05-custom-dynamodb-stack")
# LmabdaPrivileges(app, "s05-lambda-privileges")
CustomApig(app, "s05-custom-apig")

app.synth()
