from aws_cdk import (
    core,
)
import os
from static_site_stack import StaticSiteStack, StaticSiteStackPrpos
from db_bucket_stack import DbBucketStack
from aws_batch_stack import AwsBatchStack, AwsBatchStackProps
from sfn_task_stack import SfnTaskStack, SfnTaskStackPrpops
from api_stack import ApiStack, ApiStackPrpos

app = core.App()
env = {
    "region": os.environ["CDK_DEFAULT_REGION"],
    "account": os.environ["CDK_DEFAULT_ACCOUNT"],
}

static_site_stack = StaticSiteStack(
    app, "StaticSiteStack",
    props=StaticSiteStackPrpos(
        domain_name=app.node.try_get_context('domain'),
        certificate_arn=app.node.try_get_context('certificate_arn')
    ),
    env=env
)

db_bucket_stack = DbBucketStack(
    app, "DbBucketStack",
    env=env
)

aws_batch_stack = AwsBatchStack(
    app, "AwsBatchStack",
    props=AwsBatchStackProps(
        bucket=db_bucket_stack.bucket
    ),
    env=env
)

sfn_task_stack = SfnTaskStack(
    app, "SfnTaskStack",
    props=SfnTaskStackPrpops(
        bucket=db_bucket_stack.bucket,
        table=db_bucket_stack.table,
        job_def=aws_batch_stack.job_def,
        job_queue=aws_batch_stack.job_queue,
    ),
    env=env
)

api_stack = ApiStack(
    app, "ApiStack",
    props=ApiStackPrpos(
        bucket=db_bucket_stack.bucket,
        table=db_bucket_stack.table,
        state_machine=sfn_task_stack.state_machine,
        domain_name=app.node.try_get_context('domain'),
        certificate_arn=app.node.try_get_context('certificate_arn'),
    ),
    env=env
)

app.synth()
