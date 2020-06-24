from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3,
    aws_events as _events,
    aws_events_targets as _targets,
)


class CustomLambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ## create lambda function from inline function
        try:
            with open("./lambda_src/custom_lambda.py", "r") as f:
                custom_lambda_code = f.read()
        except OSError as e:
            raise Exception(f"fals to open lambda function code, error {e}")

        custom_lambda_fn = _lambda.Function(
            self,
            "customLambda",
            function_name="custom_lambda",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(custom_lambda_code),
            timeout=core.Duration.seconds(3),
            reserved_concurrent_executions=1,
            environment={"LOG_LEVEL": "INFO"},
        )

        # create custom log group
        custom_loggroup = _logs.LogGroup(
            self,
            "customLogGroup",
            log_group_name=f"/aws/lambda/{custom_lambda_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        ## create lambda function from s3
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
            environment={"Log_Group": "INFO"},
        )

        _logs.LogGroup(
            self,
            "customLogGroupS3",
            log_group_name=f"/aws/lambda/{custom_lambda_s3.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_WEEK,
        )

        ## cloudwatch rules
        #  - every day at 10:00 UTC
        six_pm_cron = _events.Rule(
            self,
            "sixPmRule",
            schedule=_events.Schedule.cron(
                minute="0", hour="18", month="*", week_day="MON-FRI", year="*"
            ),
        )
        # - every 3 minutes
        run_every_3_mins = _events.Rule(
            self, "every3Mins", schedule=_events.Schedule.rate(core.Duration.minutes(3))
        )

        # add lambda to cloudwatch event rules
        six_pm_cron.add_target(_targets.LambdaFunction(custom_lambda_fn))
        run_every_3_mins.add_target(_targets.LambdaFunction(custom_lambda_s3))
