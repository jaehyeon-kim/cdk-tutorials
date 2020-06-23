from aws_cdk import core, aws_s3 as _s3


class S03ProjectStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, is_prod=False, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.is_prod = is_prod

        stage = "prod" if is_prod else "dev"
        print(f"context ({stage}) - {self.node.try_get_context('envs')[stage]}")

        self.create_artifact_bucket()
        self.import_external_resource()

    def create_artifact_bucket(self):
        if self.is_prod:
            artifactBucket = _s3.Bucket(
                self,
                "myProdArtifactBucketId",
                versioned=True,
                encryption=_s3.BucketEncryption.S3_MANAGED,
                removal_policy=core.RemovalPolicy.RETAIN,
            )
        else:
            artifactBucket = _s3.Bucket(
                self, "myDevArtifactBucketId", removal_policy=core.RemovalPolicy.DESTROY
            )

    def import_external_resource(self):
        if self.is_prod:
            external_bucket = _s3.Bucket.from_bucket_name(
                self, "myImportedBucket", "cdktoolkit-stagingbucket-a88rrimivb4u"
            )
            output = core.CfnOutput(
                self, "myImportedBucketOutput", value=external_bucket.bucket_name
            )
            print(f"imported bucket output - {output}")
