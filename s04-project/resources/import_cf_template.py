import json
from aws_cdk import core, aws_s3 as _s3, aws_iam as _iam


class ImportFromTemplate(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        try:
            with open("./resources/create_s3_bucket_template.json", "r") as f:
                cfn_template = json.load(f)
        except OSError:
            print("unable to read Cfn Template")

        resources_from_cfn = core.CfnInclude(self, "CustomInfra", template=cfn_template)

        encrypted_bkt_arn = core.Fn.get_att("EncryptedS3Bucket", "Arn")

        output1 = core.CfnOutput(
            self, "EncryptedS3BucketArn", value=f"{encrypted_bkt_arn.to_string()}"
        )
