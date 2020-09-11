#!/usr/bin/env python3

from aws_cdk import core

from rds_databases.rds_databases_stack import RdsDatabasesStack


app = core.App()
RdsDatabasesStack(app, "rds-databases")

app.synth()
