from aws_cdk import core, aws_dynamodb as _dynamodb


class CustomDynamoDbStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        mytable = _dynamodb.Table(
            self,
            "mytable",
            table_name="my-table",
            partition_key=_dynamodb.Attribute(name=id, type=_dynamodb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY,
            server_side_encryption=True,
        )

