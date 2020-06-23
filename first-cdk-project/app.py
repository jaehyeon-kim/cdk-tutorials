#!/usr/bin/env python3

from aws_cdk import core

from first_cdk_project.first_cdk_project_stack import FirstCdkProjectStack


app = core.App()
FirstCdkProjectStack(app, "first-cdk-project")

app.synth()
