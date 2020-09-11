# Building in the Cloud - Demo repository

Here is a list of super simple demos meant for the `Building in the Clouds`
talk. Feel free to check them out, modify them, and suggest changes and
additions!

## Requirements

- AWS Cloud Development Kit (`sudo npm install -g aws-cdk`)
- A text editor

## Demos

- Autoscaling Group - Simple Web Server ASG + Load Balancer
- RDS Database
- Simple Cloudformaton - Automating Deployment
- Route53 - DNS + Location based routing

### Autoscaling Group - Simple Web Server ASG + Load Balancer

For this demo, we create it all - an ASG + an Application load balancer. And
when it comes to the demo application itself, we have a simple web server
running and the web page is displaying the instance id of the currently accessed
instance.

### RDS Database

Like before, we just launch a RDS database here, and also - an EC2 Instance that
will serve as a bastion host (hop box) to test out the RDS. The hop box is
accessible via the SSM Session manager, as the instance has the proper
permissions set.

To demo RDS, jump on the EC2 instance via Session manager, and connect to the
endpoint using the hostname and password (the password is automatically stored
in AWS Secrets manager).

### Simple Cloudformaton - Automating Deployment

We just have a simple AWS Cloudformaton template that will launch an EC2
Instance. Try it out 😉

### Route53 - DNS + Location based routing

Like the first demo this creates an ASG stack with an ALB. But what you do here
is actually launch TWO stacks, in two different regions. I believe it is set to
Tokyo and Dublin. To do this run the following commands (separately):

```bash
cdk deploy dublin
# WAIT until its deployed
cdk deploy tokyo
```

Once that is all deployed, manually configure Route53 for location based
routing to route to the respective ALBs dependent on the location. I've also
used a VPN connection to show how it looks when I am connected in Asia.

And the web application itself, instead of showing the instance ID, it actually
shows to region.

## Cleanup

You can run `cdk destroy` under all your CDK stacks, or just go into the AWS
Cloudformaton console, and manually delete the created stacks.
