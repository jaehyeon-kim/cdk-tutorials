from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3,
    aws_iam as _iam,
    aws_apigateway as _apig,
)


class CustomApig(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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
            environment={"Log_Group": "INFO",},
        )

        _logs.LogGroup(
            self,
            "customLogGroupS3",
            log_group_name=f"/aws/lambda/{custom_lambda_s3.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_WEEK,
        )

        # api gateway for lambda
        api = _apig.LambdaRestApi(self, "apiEndpoint", handler=custom_lambda_s3)

        core.CfnOutput(self, "apiUrl", value=f"{api.url}", description="api url")
