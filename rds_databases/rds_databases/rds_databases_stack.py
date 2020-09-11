from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_rds as rds,
    )

from pathlib import Path

class RdsDatabasesStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # --- iam ---
        instance_role = iam.Role(
                self, 'web_server_instance_role',
                assumed_by= iam.ServicePrincipal(service="ec2"),
                )
        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))
        # --- vpc ---
        main_vpc = ec2.Vpc(
                self, 'main_vpc',
                cidr='10.0.0.0/16',
                )
        # --- security groups ---
        rds_sg = ec2.SecurityGroup(
                self, 'rds_sg',
                vpc=main_vpc,
                allow_all_outbound=True,
                security_group_name='rds_sg'
                )

        rds_sg.add_ingress_rule(
                peer=rds_sg,
                connection=ec2.Port.tcp(3306)
                )
        # --- ec2 instance ---
        userdata_script = Path('assets/bastion.sh').read_text()
        bastion = ec2.Instance(
                self, 'bastion',
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3_AMD, ec2.InstanceSize.MEDIUM),
                machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                vpc=main_vpc,
                role=instance_role,
                allow_all_outbound=True,
                vpc_subnets=ec2.SubnetType.PUBLIC,
                security_group=rds_sg
                )
        bastion.add_user_data(userdata_script)
        # --- rds database ---
        aurora_db = rds.DatabaseCluster(
                self, 'aurora_rds',
                engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
                master_user={
                    "username": "clusteradmin"
                    },
                instance_props={
                    "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
                    "vpc_subnets": {
                        "subnet_type": ec2.SubnetType.PRIVATE
                        },
                    "vpc": main_vpc,
                    "security_groups": [rds_sg]
                    },
                )

        core.CfnOutput(self, 'instance-id', value=bastion.instance_id)
