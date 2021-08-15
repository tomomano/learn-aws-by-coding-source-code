from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    aws_batch as batch,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
import os
from dataclasses import dataclass

@dataclass
class SfnTaskStackPrpops:
    bucket: s3.Bucket
    table: ddb.Table
    job_def: batch.JobDefinition
    job_queue: batch.JobQueue

class SfnTaskStack(core.Stack):

    def __init__(self, scope: core.App, name: str, props: SfnTaskStackPrpops, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        common_params = {
            "runtime": _lambda.Runtime.PYTHON_3_7,
            "environment": {
                "BUCKET_NAME": props.bucket.bucket_name,
                "TABLE_NAME": props.table.table_name,
            },
        }

        ## Below, define step functions ##
        handle_error_lambda = _lambda.Function(
            self, "HandleErrorLambda",
            code=_lambda.AssetCode('lambda'),
            handler='sfn_handlers.handle_error',
            memory_size=128,
            timeout=core.Duration.seconds(10),
            **common_params
        )
        props.table.grant_read_write_data(handle_error_lambda)
        handle_error_task = tasks.LambdaInvoke(
            self, "HandleErrorTask",
            lambda_function=handle_error_lambda,
        )

        ## AWS Batch submit job
        batch_task = tasks.BatchSubmitJob(self, "Submit Job",
            job_definition_arn=props.job_def.job_definition_arn,
            job_name="NeuralStyleTransfer",
            job_queue_arn=props.job_queue.job_queue_name,
            integration_pattern=sfn.IntegrationPattern.RUN_JOB,
            payload=sfn.TaskInput.from_object({
                "style_image": sfn.JsonPath.string_at('$.style_image'),
                "content_image": sfn.JsonPath.string_at('$.content_image'),
                "style_weight": sfn.JsonPath.string_at('$.style_weight'),
                "content_weight": sfn.JsonPath.string_at('$.content_weight'),
                "save_path": sfn.JsonPath.string_at('$.save_path'),
            }),
            result_path="DISCARD",
        )
        batch_task.add_catch(handle_error_task, result_path="$.error")

        check_image_lambda = _lambda.Function(
            self, "CheckImageLambda",
            code=_lambda.AssetCode('lambda'),
            handler='sfn_handlers.check_image',
            memory_size=128,
            timeout=core.Duration.seconds(10),
            **common_params
        )
        props.bucket.grant_read(check_image_lambda)
        check_image_task = tasks.LambdaInvoke(
            self, "CheckImageTask",
            lambda_function=check_image_lambda,
            payload_response_only=True,
            result_path="$.check_image",
        )
        check_image_task.add_catch(handle_error_task, result_path="$.error")

        submit_job_lambda = _lambda.Function(
            self, "SubmitJobLambda",
            code=_lambda.AssetCode('lambda'),
            handler='sfn_handlers.submit_job',
            memory_size=128,
            timeout=core.Duration.seconds(10),
            **common_params
        )
        props.table.grant_read_write_data(submit_job_lambda)
        submit_job_task = tasks.LambdaInvoke(
            self, "SubmitJobTask",
            lambda_function=submit_job_lambda,
            result_path="DISCARD",
        )
        submit_job_task.add_catch(handle_error_task, result_path="$.error")

        ## crop and resize images
        layer = _lambda.LayerVersion(
            self, "LambdaLayer",
            code=_lambda.Code.from_asset('lambda_layer/layer.zip'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_7],
        )
        crop_image_lambda = _lambda.Function(
            self, "CropImageLambda",
            code=_lambda.AssetCode('lambda'),
            handler='sfn_handlers.crop_image',
            memory_size=1024,
            timeout=core.Duration.seconds(60),
            layers=[layer],
            **common_params
        )
        props.bucket.grant_read_write(crop_image_lambda)
        crop_image_task = tasks.LambdaInvoke(
            self, "CropImageTask",
            lambda_function=crop_image_lambda,
            result_path="DISCARD",
        )
        crop_image_task.add_catch(handle_error_task, result_path="$.error")

        # finish the task
        complete_job_lambda = _lambda.Function(
            self, "CompleteJobLambda",
            code=_lambda.AssetCode('lambda'),
            handler='sfn_handlers.complete_job',
            memory_size=128,
            timeout=core.Duration.seconds(10),
            **common_params
        )
        props.table.grant_read_write_data(complete_job_lambda)
        complete_job_task = tasks.LambdaInvoke(
            self, "CompleteJobTask",
            lambda_function=complete_job_lambda,
            result_path="DISCARD",
        )

        waitX = sfn.Wait(self, "Wait 10 seconds", time=sfn.WaitTime.duration(core.Duration.seconds(10)))

        sfn_chain = sfn.Chain\
            .start(waitX)\
            .next(check_image_task)\
            .next(
                sfn.Choice(self, "Is the image ready?")\
                .when(sfn.Condition.string_equals("$.check_image.state", "READY"),
                    submit_job_task\
                    .next(crop_image_task)\
                    .next(batch_task)\
                    .next(complete_job_task)\
                    .next(sfn.Succeed(self, "Success!"))
                )\
                .when(sfn.Condition.number_greater_than("$.check_image.attempts", 6), sfn.Fail(self, "Fail"))\
                .otherwise(waitX)\
            )

        # define state machine
        state_machine = sfn.StateMachine(
            self, "StateMachine",
            definition=sfn_chain,
            state_machine_type=sfn.StateMachineType.STANDARD,
        )
        self.state_machine = state_machine
