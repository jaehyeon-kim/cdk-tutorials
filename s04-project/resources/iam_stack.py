import json
from aws_cdk import core, aws_iam as _iam, aws_secretsmanager as _secretsmanager, aws_ssm as _ssm


class IamResources(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # add user 1 with secret manager password
        user1_pass = _secretsmanager.Secret(
            self, "user1Pass", description="Password for user 1", secret_name="user1_pass"
        )

        user1 = _iam.User(self, "user1", password=user1_pass.secret_value, user_name="user1")

        # add user 2 with literal password
        user2 = _iam.User(
            self, "user2", password=core.SecretValue("dont-use-bad-password@123"), user_name="user2"
        )

        # add user 2 to group
        group1 = _iam.Group(self, "group1Id", group_name="group1")
        group1.add_user(user2)

        # add managed policy to group
        group1.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )

        # add inline policy - specific resource
        param = _ssm.StringParameter(
            self,
            "parameterId",
            description="parameter",
            parameter_name="/foo",
            string_value="bar",
            tier=_ssm.ParameterTier.STANDARD,
        )
        param.grant_read(group1)

        # add inline policy - list all parameters in console
        group_statement1 = _iam.PolicyStatement(
            sid="DescribeAllParameters",
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=["ssm:DescribeParameters"],
        )
        group1.add_to_policy(group_statement1)

        # create iam role
        ops_role = _iam.Role(
            self,
            "opsRole",
            assumed_by=_iam.AccountPrincipal(f"{core.Aws.ACCOUNT_ID}"),
            role_name="ops_role",
        )
        list_ec2_policy = _iam.ManagedPolicy(
            self,
            "listEc2Instances",
            description="list ec2 instances in the account",
            managed_policy_name="list_ec2_policy",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=["ec2:Describe*", "cloudwatch:Describe*", "cloudwatch:Get*"],
                    resources=["*"],
                )
            ],
            roles=[ops_role],
        )

        # login url autogeneration
        output1 = core.CfnOutput(
            self,
            "user2LoginUrl",
            description="Login for user 2",
            value=f"https://{core.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console",
        )
