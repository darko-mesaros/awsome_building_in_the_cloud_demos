from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    )

from pathlib import Path

class R53GlobalStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # --- vpc ---
        main_vpc = ec2.Vpc(
                self, 'main_vpc',
                cidr='10.0.0.0/16',
                )
        # --- security groups ---
        alb_internet_sg = ec2.SecurityGroup(
                self, 'alb_internet_sg',
                vpc=main_vpc,
                allow_all_outbound=True,
                security_group_name='alb_internet_sg'
                )

        alb_internet_sg.add_ingress_rule(
                peer=ec2.Peer.any_ipv4(),
                connection=ec2.Port.tcp(80)
                )

        ec2_alb_sg = ec2.SecurityGroup(
                self, 'ec2_alb_sg',
                vpc=main_vpc,
                allow_all_outbound=True,
                security_group_name='ec2_alb_sg'
                )
        ec2_alb_sg.add_ingress_rule(
                peer=alb_internet_sg,
                connection=ec2.Port.tcp(80)
                )
        # --- iam ---
        instance_role = iam.Role(
                self, 'web_server_instance_role',
                assumed_by= iam.ServicePrincipal(service="ec2"),
                )
        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))
        # --- autoscaling group ---
        web_userdata_script = Path('assets/web_server.sh').read_text()

        web_asg = autoscaling.AutoScalingGroup(
                self, 'web_asg',
                instance_type=ec2.InstanceType('t3.micro'),
                machine_image=ec2.AmazonLinuxImage(
                    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                    ),
                vpc=main_vpc,
                role=instance_role,
                security_group=ec2_alb_sg,
                user_data=ec2.UserData.add_commands(web_userdata_script),
                max_capacity=4,
                min_capacity=2,
                vpc_subnets=ec2.SubnetType.PUBLIC
                )
        web_asg.add_user_data(web_userdata_script)
        # --- load balancer ---
        web_lb = elbv2.ApplicationLoadBalancer(
                self, 'web_lb',
                vpc=main_vpc,
                security_group=alb_internet_sg,
                internet_facing=True,
                )
        
        web_lb_listener = web_lb.add_listener(
                "web_lb_listener",
                open=True,
                port=80,
                )
        web_lb_listener.add_targets(
                'web_servers',
                port=80,
                targets=[web_asg]
                )

        # --- outputs ---
        core.CfnOutput(self, 'alb_dns', value=web_lb.load_balancer_dns_name)

