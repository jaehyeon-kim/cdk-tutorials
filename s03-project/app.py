#!/usr/bin/env python3

from aws_cdk import core

from s03_project.s03_project_stack import S03ProjectStack
from resource_stacks.custom_vpc import CustomVpcStack

app = core.App()

# print(app.node.try_get_context("prod"))
prod_ctx = app.node.try_get_context("envs")["prod"]
dev_ctx = app.node.try_get_context("envs")["dev"]

env_PROD = core.Environment(account=prod_ctx["account"], region=prod_ctx["region"])
env_DEV = core.Environment(account=dev_ctx["account"], region=dev_ctx["region"])

S03ProjectStack(app, prod_ctx["stack_name"], is_prod=True, env=env_PROD)
S03ProjectStack(app, dev_ctx["stack_name"], is_prod=False, env=env_DEV)

CustomVpcStack(app, "my-custom-vpc-stack", env=env_PROD)

core.Tag.add(app, "stack-level-key", "stack-level-value")

app.synth()
