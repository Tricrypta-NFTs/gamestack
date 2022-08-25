from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    CfnOutput,
    
)
from constructs import Construct

class GameStudioStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self, "VPC",
            max_azs=1,
        )

        data = open("./p4d-files/configure-p4d.sh", "rb").read()
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(str(data, 'utf-8'))

        sg = ec2.SecurityGroup(
            self, "SecurityGroup",
            vpc=vpc,
            description="Allow tcp traffic from NLB to instances over port 1666",
            security_group_name="HelixCore SecurityGroup",
            allow_all_outbound=True,
        )

        sg.add_ingress_rule(
            ec2.Peer.ipv4('0.0.0.0/0'),
            ec2.Port.tcp(1666),
            "allow tcp traffic from nlb"
        )
        
        machine_image = ec2.GenericLinuxImage({
            "us-east-1": "ami-0e09d7c1e4eb188b0"
        })

        helix_core = autoscaling.AutoScalingGroup(
            self,
            "HelixCore",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE
            ),
            machine_image=machine_image,
            user_data=user_data,
            security_group=sg,
            block_devices=[
                autoscaling.BlockDevice(
                    device_name="/dev/sdb",
                    volume=autoscaling.BlockDeviceVolume.ebs(24)
                ),
                autoscaling.BlockDevice(
                    device_name="/dev/sdc",
                    volume=autoscaling.BlockDeviceVolume.ebs(24)
                    )
            ]
        )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "CDKInstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        lb = elbv2.NetworkLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True
        )

        listener = lb.add_listener(
            "PublicListener",
            port=1666,
        )

        health_check = elbv2.HealthCheck(
            protocol=elbv2.Protocol.TCP
        )

        listener.add_targets(
            "Ec2TargetGroup",
            port=1666,
            targets=[helix_core],
            health_check=health_check,
            protocol=elbv2.Protocol.TCP
        )

        CfnOutput(self, "LoadBalancer", export_name="LoadBalancer", value=lb.load_balancer_dns_name)
