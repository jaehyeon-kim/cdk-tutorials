#!/usr/bin/env python3

from aws_cdk import core

from resources.params_n_secrets_stack import ParamsNSecrets
from resources.iam_stack import IamResources
from resources.resource_policy_stack import ResourcePolicy
from resources.import_cf_template import ImportFromTemplate
from resources.sns_sqs import SnsSqs

app = core.App()

# ParamsNSecrets(app, "s04-params-and-secrets")
# IamResources(app, "s04-iam-resources")
# ResourcePolicy(app, "s04-resource-policy")
# ImportFromTemplate(app, "s04-import-from-cfn")
SnsSqs(app, "s04-sns-sqs")

app.synth()
