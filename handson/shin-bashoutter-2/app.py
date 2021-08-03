from aws_cdk import (
    core,
)
import os
from static_site_stack import StaticSiteStack, StaticSiteStackPrpos
from api_stack import ApiStack, ApiStackPrpos
from cognito_stack import CognitoStack

app = core.App()

cognito_stack = CognitoStack(
    app, "CognitoStack",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

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
        certificate_arn=app.node.try_get_context('certificate_arn'),
        user_pool=cognito_stack.user_pool,
    ),
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

app.synth()
