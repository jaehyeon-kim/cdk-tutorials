from aws_cdk import core, aws_s3 as _s3, aws_iam as _iam


class FirstCdkProjectStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        mybucket0 = _s3.Bucket(
            self,
            "myBucketId",
            bucket_name="first-cdk-project-1111",
            versioned=False,
            encryption=_s3.BucketEncryption.S3_MANAGED,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,
        )
        print(f"bucket name - {mybucket0.bucket_name}")

        # snstopicname = "abcdefg"
        # if not core.Token.is_unresolved(snstopicname) and len(snstopicname) > 5:
        #     raise ValueError("Maximum value can be only 5 chracters")

        mybucket = _s3.Bucket(self, "myBucketId1")
        output1 = core.CfnOutput(
            self,
            "myBucketOutput1",
            value=mybucket.bucket_name,
            description=f"My First CDK Bucket",
            export_name="myBucketOutput1",
        )

        _iam.Group(self, "gid", group_name="test-group")
