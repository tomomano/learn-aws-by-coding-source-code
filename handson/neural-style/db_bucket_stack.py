from aws_cdk import (
    core,
    aws_dynamodb as ddb,
    aws_s3 as s3,
)

class DbBucketStack(core.Stack):

    def __init__(self, scope: core.App, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # dynamoDB table to store job
        table = ddb.Table(
            self, "Table",
            partition_key=ddb.Attribute(
                name="job_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # S3 bucket to store image data
        bucket = s3.Bucket(
            self, "Bucket",
            auto_delete_objects=False,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        bucket.add_cors_rule(
            allowed_methods=[
                s3.HttpMethods.GET,
                s3.HttpMethods.POST,
                s3.HttpMethods.PUT,
                s3.HttpMethods.HEAD,
                s3.HttpMethods.DELETE,
            ],
            allowed_origins=["*"],
            allowed_headers=["*"],
            max_age=600,
        )

        self.table = table
        self.bucket = bucket
