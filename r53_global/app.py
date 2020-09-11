#!/usr/bin/env python3

from aws_cdk import core

from r53_global.r53_global_stack import R53GlobalStack
#from r53_global.r53_dns_stack import R53DNSStack

app = core.App()

#R53DNSStack(app, "dns")
R53GlobalStack(app, "tokyo",
        env=core.Environment(region='ap-northeast-1')
        )
R53GlobalStack(app, "dublin",
        env=core.Environment(region='eu-west-1')
        )

app.synth()
