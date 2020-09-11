#!/usr/bin/env python3

from aws_cdk import core

from asg_alb_webservers.asg_alb_webservers_stack import AsgAlbWebserversStack


app = core.App()
AsgAlbWebserversStack(app, "asg-alb-webservers")

app.synth()
