from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3,
    aws_dynamodb as _dynamodb,
    aws_iam as _iam,
)


class LmabdaPrivileges(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # dynamodb table
        mytable = _dynamodb.Table(
            self,
            "mytable",
            table_name="my-table",
            partition_key=_dynamodb.Attribute(name=id, type=_dynamodb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY,
            server_side_encryption=True,
        )

        # lambda function
        source_bucket = _s3.Bucket.from_bucket_name(self, "sourceBucket", "cdk-tutorials-resources")

        custom_lambda_s3 = _lambda.Function(
            self,
            "customLambdaS3",
            function_name="custom_lambda_s3",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="custom_lambda.lambda_handler",
            code=_lambda.S3Code(bucket=source_bucket, key="custom_lambda.zip"),
            timeout=core.Duration.seconds(3),
            reserved_concurrent_executions=1,
            environment={
                "Log_Group": "INFO",
                "TABLE_NAME": f"{mytable.table_name}",
                "BUCKET_NAME": f"{source_bucket.bucket_name}",
            },
        )

        _logs.LogGroup(
            self,
            "customLogGroupS3",
            log_group_name=f"/aws/lambda/{custom_lambda_s3.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_WEEK,
        )

        # lambda role
        s3_policy = _iam.ManagedPolicy(
            self,
            "listBucketsPolicy",
            description="list s3 buckets",
            managed_policy_name="listBuckets",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW, actions=["s3:List*"], resources=["*"]
                )
            ],
        )
        db_policy = _iam.ManagedPolicy(
            self,
            "dbPolicy",
            description="get and put items",
            managed_policy_name="dbPutGet",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=["dynamodb:GetItem", "dynamodb:PutItem"],
                    resources=[f"{mytable.table_arn}"],
                )
            ],
        )
        custom_lambda_s3.role.add_managed_policy(s3_policy)
        custom_lambda_s3.role.add_managed_policy(db_policy)
        # mytable.grant_read_data(custom_lambda_s3)
        # mytable.grant_write_data(custom_lambda_s3)
