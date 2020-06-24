import json
from aws_cdk import core, aws_s3 as _s3, aws_iam as _iam


class ResourcePolicy(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        mybucket = _s3.Bucket(
            self,
            "mybucketId",
            bucket_name="s04-resource-policy111",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        # add bucket resource policy
        mybucket.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[mybucket.arn_for_objects("*.html")],
                principals=[_iam.AnyPrincipal()],
            )
        )

        mybucket.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{mybucket.bucket_arn}/*"],
                principals=[_iam.AnyPrincipal()],
                conditions={"Bool": {"aws:SecureTransport": False}},
            )
        )
