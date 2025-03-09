import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds

class NetworkStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "Assignment3_CDK_VPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                )
            ]
        )
        self.vpc = vpc
    
class Serverstack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, network_stack: cdk.Stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        for i, subnet in enumerate(network_stack.vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnets):
            ec2.Instance(
                self, 
                f"WebServer{i+1}",
                instance_type=ec2.InstanceType("t2.micro"),
                machine_image=ec2.MachineImage.latest_amazon_linux(),
                vpc=network_stack.vpc,
                security_group=web_sg,
                vpc_subnets=ec2.SubnetSelection(subnets=[subnet]),
            )

        web_sg = ec2.SecurityGroup(self, "Assignment3_CDK_Web_SG",
            vpc=network_stack.vpc,
            description="Allow HTTP/HTTPS traffic",
            allow_all_outbound=True
        )
        web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")

        rds_sg = ec2.SecurityGroup(self, "Assignment3_CDK_RDS_SG",
            vpc=network_stack.vpc,
            description="Allow MySQL traffic",
            allow_all_outbound=True
        )
        rds_sg.add_ingress_rule(web_sg, ec2.Port.tcp(3306), "Allow MySQL traffic")

        rds.DatabaseInstance(self, "Assignment3_CDK_RDS",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_26
            ),
            vpc=network_stack.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
            security_groups=[rds_sg],
            instance_type=ec2.InstanceType("t2.micro"),
            allocated_storage=20,
            database_name="MyDatabase",
            credentials=rds.Credentials.from_generated_secret("admin"),
        )
