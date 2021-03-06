from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_batch as batch,
    aws_iam as iam,
    aws_ecr as ecr,
)
import os
from dataclasses import dataclass

@dataclass
class AwsBatchStackProps:
    bucket: s3.Bucket

class AwsBatchStack(core.Stack):

    def __init__(self, scope: core.App, name: str, props: AwsBatchStackProps, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        vpc = ec2.Vpc(
            self, "vpc",
            max_azs=1,
            cidr="10.10.0.0/23",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        managed_env = batch.ComputeEnvironment(
            self, "managed-env",
            compute_resources=batch.ComputeResources(
                vpc=vpc,
                allocation_strategy=batch.AllocationStrategy.BEST_FIT,
                desiredv_cpus=0,
                maxv_cpus=64,
                minv_cpus=0,
                instance_types=[
                    ec2.InstanceType("g4dn.xlarge")
                ],
            ),
            managed=True,
            compute_environment_name=self.stack_name + "compute-env"
        )

        job_queue = batch.JobQueue(
            self, "job-queue",
            compute_environments=[
                batch.JobQueueComputeEnvironment(
                    compute_environment=managed_env,
                    order=100
                )
            ],
            job_queue_name=self.stack_name + "job-queue"
        )

        job_role = iam.Role(
            self, "job-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ecs-tasks.amazonaws.com")
            )
        )
        # allow read and write access to S3 bucket
        props.bucket.grant_read_write(job_role)

        # create a ECR repository to push docker image
        repo = ecr.Repository(
            self, "repository",
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        job_def = batch.JobDefinition(
            self, "job-definition",
            container=batch.JobDefinitionContainer(
                image=ecs.ContainerImage.from_ecr_repository(repo),
                command=["-s", "Ref::style_image", "-c", "Ref::content_image", "--save_path", "Ref::save_path", "--use_s3",
                         "--style_weight", "Ref::style_weight", "--content_weight", "Ref::content_weight"],
                vcpus=4,
                gpu_count=1,
                memory_limit_mib=12000,
                job_role=job_role,
                environment={
                    "BUCKET_NAME": props.bucket.bucket_name
                }
            ),
            job_definition_name=self.stack_name + "job-definition",
            timeout=core.Duration.minutes(30),
        )

        self.job_queue = job_queue
        self.job_def = job_def
