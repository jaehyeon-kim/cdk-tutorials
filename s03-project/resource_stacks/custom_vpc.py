from aws_cdk import core, aws_ec2 as _ec2


class CustomVpcStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prod_configs = self.node.try_get_context("envs")["prod"]

        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr=prod_configs["vpc_configs"]["vpc_cidr"],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet",
                    cidr_mask=prod_configs["vpc_configs"]["cidr_mask"],
                    subnet_type=_ec2.SubnetType.PUBLIC,
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet",
                    cidr_mask=prod_configs["vpc_configs"]["cidr_mask"],
                    subnet_type=_ec2.SubnetType.PRIVATE,
                ),
                _ec2.SubnetConfiguration(
                    name="dbSubnet",
                    cidr_mask=prod_configs["vpc_configs"]["cidr_mask"],
                    subnet_type=_ec2.SubnetType.ISOLATED,
                ),
            ],
        )

        core.Tag.add(custom_vpc, "resource-level-key", "resource-level-value")

        core.CfnOutput(self, "customVpcOutput", value=custom_vpc.vpc_id, export_name="customVpcId")
        self.import_resources()

    def import_resources(self):
        default_vpc = _ec2.Vpc.from_lookup(self, "myImportedVpc", is_default=True)
        # _ec2.Vpc.from_lookup(self, "myimportedvpc1", vpc_id="vpc-2888w8w")
        output = core.CfnOutput(self, "myImportedVpcOutput", value=default_vpc.vpc_id)
        print(f"imported vpc output - {output}")
