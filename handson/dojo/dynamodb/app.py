from aws_cdk import (
    core,
    aws_dynamodb as ddb
)
import os

class Cov19VaccinationDb(core.Stack):

    def __init__(self, scope: core.App, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        table = ddb.Table(
            self, "Cov19VaccinationTable",
            partition_key=ddb.Attribute(
                name="username",
                type=ddb.AttributeType.STRING
            ),
            sort_key=ddb.Attribute(
                name="dose",
                type=ddb.AttributeType.NUMBER
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        table.add_global_secondary_index(
            partition_key=ddb.Attribute(
                name="age", type=ddb.AttributeType.NUMBER
            ),
            index_name="ItemsByAge"
        )
        table.add_global_secondary_index(
            partition_key=ddb.Attribute(
                name="prefecture", type=ddb.AttributeType.STRING
            ),
            index_name="ItemsByPrefecture"
        )
        core.CfnOutput(self, "TableName", value=table.table_name)

app = core.App()
Cov19VaccinationDb(
    app, "Cov19VaccinationDb",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)
app.synth()
