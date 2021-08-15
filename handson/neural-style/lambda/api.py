import boto3
import json, os, uuid
from datetime import datetime, timezone

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])
s3 = boto3.resource("s3")
bucket = s3.Bucket(os.environ["BUCKET_NAME"])

HEADERS = {
    "Access-Control-Allow-Origin": "*",
}

def get_job(event, context):
    try:
        path_params = event.get("pathParameters", {})
        job_id = path_params.get("job_id", "")
        if not job_id:
            raise ValueError("Invalid request. The path parameter 'job_id' is missing")

        data = table.get_item(
            Key={"job_id": job_id},
        ).get("Item")
        if not data:
            raise ValueError("non-exisiting item id")

        s3_client = boto3.client('s3')
        style_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket.name,
                'Key': f"{job_id}/style.png",
            },
            ExpiresIn=120
        )
        content_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket.name,
                'Key': f"{job_id}/content.png",
            },
            ExpiresIn=120
        )
        if data["status"] == "completed":
            generated_url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': bucket.name,
                    'Key': f"{job_id}/generated.png",
                },
                ExpiresIn=120
            )
        else:
            generated_url = ""

        status_code = 200
        resp = {
            "job_id": data["job_id"],
            "status": data["status"],
            "style_image_url": style_url,
            "content_image_url": content_url,
            "generated_image_url": generated_url
        }
    except ValueError as e:
        status_code = 400
        resp = {"Message": f"Bad request. {str(e)}"}
    except Exception as e:
        status_code = 500
        resp = {"description": str(e)}
    return {
        "statusCode": status_code,
        "headers": HEADERS,
        "body": json.dumps(resp)
    }

def post_job(event, context):
    """
    handler for POST /job
    """
    try:
        try:
            body = json.loads(event.get("body"))
        except Exception:
            body = {}
        style_weight = str(body.get("style_weight", 100000))
        content_weight = str(body.get("content_weight", 1))

        job_id = uuid.uuid4().hex
        s3_client = boto3.client('s3')
        style_url = s3_client.generate_presigned_post(
            Bucket=bucket.name,
            Key=f"{job_id}/style.png",
            ExpiresIn=120,
        )
        content_url = s3_client.generate_presigned_post(
            Bucket=bucket.name,
            Key=f"{job_id}/content.png",
            ExpiresIn=120,
        )

        item = {
            "job_id": job_id,
            "style_weight": style_weight,
            "content_weight": content_weight,
            "status": "preparing",
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds")
        }
        response = table.put_item(Item=item)

        # start Step Function
        sfn = boto3.client("stepfunctions")
        params = {
            "job_id": job_id,
            "style_image": f"{job_id}/style.png",
            "content_image": f"{job_id}/content.png",
            "style_weight": style_weight,
            "content_weight": content_weight,
            "save_path": f"{job_id}/generated.png",
        }
        sfn.start_execution(
            stateMachineArn=os.environ["STATE_MACHINE_ARN"],
            name=job_id,
            input=json.dumps(params),
        )

        status_code = 201
        resp = {
            "job_id": job_id,
            "status": "preparing",
            "style_image_url": style_url,
            "content_image_url": content_url,
        }
    except Exception as e:
        status_code = 500
        resp = {"description": str(e)}
    return {
        "statusCode": status_code,
        "headers": HEADERS,
        "body": json.dumps(resp)
    }

def delete_job(event, context):
    try:
        path_params = event.get("pathParameters", {})
        job_id = path_params.get("job_id", "")
        if not job_id:
            raise ValueError("Invalid request. The path parameter 'job_id' is missing")

        response = table.delete_item(
            Key={"job_id": job_id},
        )

        bucket.Object(f"{job_id}/style.png").delete()
        bucket.Object(f"{job_id}/content.png").delete()

        status_code = 204
        resp = {"description": "Successfully deleted."}
    except Exception as e:
        status_code = 500
        resp = {"description": str(e)}
    return {
        "statusCode": status_code,
        "headers": HEADERS,
        "body": json.dumps(resp)
    }
