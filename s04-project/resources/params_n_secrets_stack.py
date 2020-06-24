import json
from aws_cdk import core, aws_ssm as _ssm, aws_secretsmanager as _secretsmanager


class ParamsNSecrets(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        params1 = _ssm.StringParameter(
            self,
            "parameter1Id",
            description="Load Testing Configuration",
            parameter_name="NoOfConCurrentUsers",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD,
        )

        output1 = core.CfnOutput(
            self,
            "parameter1Output",
            description="Number of concurrent users",
            value=f"{params1.string_value}",
        )

        params2 = _ssm.StringParameter(
            self,
            "parameter2Id",
            description="Load Testing Configuration",
            parameter_name="/locus/configuration/NoOfConCurrentUsers",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD,
        )

        params3 = _ssm.StringParameter(
            self,
            "parameter3Id",
            description="Load Testing Configuration",
            parameter_name="/locus/configuration/DurationInSec",
            string_value="300",
            tier=_ssm.ParameterTier.STANDARD,
        )

        secret1 = _secretsmanager.Secret(
            self, "secret1Id", description="Customer DB password", secret_name="cust_db_pass"
        )

        output2 = core.CfnOutput(
            self, "secret1Output", description="secret 1", value=f"{secret1.secret_value}",
        )

        templated_secret = _secretsmanager.Secret(
            self,
            "secret2Id",
            description="Templated secret for user data",
            secret_name="user_kon_attributes",
            generate_secret_string=_secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "kon"}),
                generate_string_key="password",
            ),
        )
