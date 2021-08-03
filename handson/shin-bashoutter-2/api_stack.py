from aws_cdk import (
    core,
    aws_dynamodb as ddb,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_apigateway as apigw,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_cognito as cognito,
)
from dataclasses import dataclass

@dataclass
class ApiStackPrpos:
    domain_name: str
    certificate_arn: str
    user_pool: cognito.UserPool

class ApiStack(core.Stack):

    def __init__(self, scope: core.App, name: str, props: ApiStackPrpos, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # dynamoDB table to store haiku
        table = ddb.Table(
            self, "Bashoutter-Table",
            partition_key=ddb.Attribute(
                name="item_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        common_params = {
            "runtime": _lambda.Runtime.PYTHON_3_7,
            "environment": {
                "TABLE_NAME": table.table_name
            }
        }

        # define Lambda functions
        get_haiku_lambda = _lambda.Function(
            self, "GetHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.get_haiku",
            memory_size=512,
            timeout=core.Duration.seconds(10),
            **common_params,
        )
        post_haiku_lambda = _lambda.Function(
            self, "PostHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.post_haiku",
            **common_params,
        )
        patch_haiku_lambda = _lambda.Function(
            self, "PatchHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.patch_haiku",
            **common_params,
        )
        delete_haiku_lambda = _lambda.Function(
            self, "DeleteHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.delete_haiku",
            **common_params,
        )

        # grant permissions
        table.grant_read_data(get_haiku_lambda)
        table.grant_read_write_data(post_haiku_lambda)
        table.grant_read_write_data(patch_haiku_lambda)
        table.grant_read_write_data(delete_haiku_lambda)

        # define API Gateway
        api = apigw.RestApi(
            self, "BashoutterApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=apigw.Cors.DEFAULT_HEADERS + ['Authorization']
            ),
        )

        certificate = acm.Certificate.from_certificate_arn(
            self, "ACMCertificate", props.certificate_arn
        )

        domain = apigw.DomainName(
            self, "domain",
            domain_name="api." + props.domain_name,
            certificate=certificate,
            endpoint_type=apigw.EndpointType.EDGE,
        )
        domain.add_base_path_mapping(api)

        # create A record in Route 53
        route53.ARecord(
            self, "AliasRecord",
            zone=route53.HostedZone.from_lookup(
                self, 'zone', domain_name=props.domain_name,
            ),
            record_name="api." + props.domain_name,
            target=route53.RecordTarget.from_alias(
                route53_targets.ApiGatewayDomain(domain)
            )
        )

        authorizer = apigw.CognitoUserPoolsAuthorizer(
            self, "Authorizer",
            cognito_user_pools=[props.user_pool]
        )

        haiku = api.root.add_resource("haiku")
        haiku.add_method(
            "GET",
            apigw.LambdaIntegration(get_haiku_lambda),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )
        haiku.add_method(
            "POST",
            apigw.LambdaIntegration(post_haiku_lambda),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        haiku_item_id = haiku.add_resource("{item_id}")
        haiku_item_id.add_method(
            "PATCH",
            apigw.LambdaIntegration(patch_haiku_lambda),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )
        haiku_item_id.add_method(
            "DELETE",
            apigw.LambdaIntegration(delete_haiku_lambda),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        # store parameters in SSM
        ssm.StringParameter(
            self, "TABLE_NAME",
            parameter_name="TABLE_NAME",
            string_value=table.table_name
        )
        ssm.StringParameter(
            self, "ENDPOINT_URL",
            parameter_name="ENDPOINT_URL",
            string_value=api.url
        )
