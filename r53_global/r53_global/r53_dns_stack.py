from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_route53 as r53
    )

from pathlib import Path

class R53DNSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        rup_zone = r53.HostedZone.from_lookup(
                self, 'rup_zone',
                domain_name="rup12.net"
                )

