from aws_cdk import (
    core,
)
import os
from static_site_stack import StaticSiteStack, StaticSiteStackPrpos
from api_stack import ApiStack, ApiStackPrpos

app = core.App()

static_site = StaticSiteStack(
    app, "StaticSiteStack",
    props=StaticSiteStackPrpos(
        domain_name=app.node.try_get_context('domain'),
        certificate_arn=app.node.try_get_context('certificate_arn')
    ),
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

api_stack = ApiStack(
    app, "ApiStack",
    props=ApiStackPrpos(
        domain_name=app.node.try_get_context('domain'),
        certificate_arn=app.node.try_get_context('certificate_arn')
    ),
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

app.synth()
