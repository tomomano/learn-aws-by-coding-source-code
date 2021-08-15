from aws_cdk import (
    core,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_stepfunctions as sfn,
)
from dataclasses import dataclass

@dataclass
class ApiStackPrpos:
    bucket: s3.Bucket
    table: ddb.Table
    state_machine: sfn.StateMachine
    domain_name: str
    certificate_arn: str

class ApiStack(core.Stack):

    def __init__(self, scope: core.App, name: str, props: ApiStackPrpos, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        table = props.table
        bucket = props.bucket

        common_params = {
            "runtime": _lambda.Runtime.PYTHON_3_7,
            "environment": {
                "TABLE_NAME": table.table_name,
                "BUCKET_NAME": bucket.bucket_name,
                "STATE_MACHINE_ARN": props.state_machine.state_machine_arn,
            }
        }

        # define Lambda functions
        get_job_lambda = _lambda.Function(
            self, "GetJob",
            code=_lambda.Code.from_asset("lambda"),
            handler="api.get_job",
            **common_params,
        )
        post_job_lambda = _lambda.Function(
            self, "PostJob",
            code=_lambda.Code.from_asset("lambda"),
            handler="api.post_job",
            memory_size=1024,
            timeout=core.Duration.seconds(60),
            **common_params,
        )
        delete_job_lambda = _lambda.Function(
            self, "DeleteJob",
            code=_lambda.Code.from_asset("lambda"),
            handler="api.delete_job",
            **common_params,
        )

        # grant permissions
        table.grant_read_data(get_job_lambda)
        table.grant_read_write_data(post_job_lambda)
        table.grant_read_write_data(delete_job_lambda)
        
        # grant permissions
        bucket.grant_read(get_job_lambda)
        bucket.grant_read_write(post_job_lambda)
        bucket.grant_read_write(delete_job_lambda)

        # grant permissions
        props.state_machine.grant_start_execution(post_job_lambda)

        # define API Gateway
        api = apigw.RestApi(
            self, "NeuralArtCanvasApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=apigw.Cors.DEFAULT_HEADERS,
            ),
        )

        # attach domains
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

        job_api = api.root.add_resource("job")
        job_api.add_method(
            "POST",
            apigw.LambdaIntegration(post_job_lambda),
        )

        job_id_api = job_api.add_resource("{job_id}")
        job_id_api.add_method(
            "GET",
            apigw.LambdaIntegration(get_job_lambda),
        )
        job_id_api.add_method(
            "DELETE",
            apigw.LambdaIntegration(delete_job_lambda),
        )
