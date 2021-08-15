import os, io
import boto3
from botocore.exceptions import ClientError

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])
s3 = boto3.resource("s3")
bucket = s3.Bucket(os.environ["BUCKET_NAME"])

def check_image(event, context):
    style = event.get("style_image")
    content = event.get("content_image")

    try:
        attempts = event.get("check_image").get("attempts")
    except:
        attempts = 0

    try:
        bucket.Object(style).load()
        bucket.Object(content).load()
    except ClientError:
        state = "WAITING"
    else:
        state = "READY"
    return {
        "attempts": attempts + 1,
        "state": state
    }

def submit_job(event, context):
    job_id = event.get("job_id")
    table.update_item(
        Key={"job_id": job_id},
        UpdateExpression=f"SET #at = :val",
        ExpressionAttributeNames={
            '#at': 'status'
        },
        ExpressionAttributeValues={
            ':val': "processing"
        }
    )

def crop_image(event, context):
    from PIL import Image

    style =  Image.open(bucket.Object(event.get("style_image")).get().get("Body"))
    content =  Image.open(bucket.Object(event.get("content_image")).get().get("Body"))

    width, height = style.size[0], style.size[1]
    aspect = width / float(height)

    ideal_width = content.size[0]
    ideal_height = content.size[1]
    ideal_aspect = ideal_width / float(ideal_height)

    if aspect > ideal_aspect:
        new_width = int(ideal_aspect * height)
        offset = (width - new_width) / 2
        resize = (offset, 0, width - offset, height)
    else:
        new_height = int(width / ideal_aspect)
        offset = (height - new_height) / 2
        resize = (0, offset, width, height - offset)

    style = style.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)

    with io.BytesIO() as buffer:
        style.save(buffer, "PNG")
        resp = bucket.put_object(
            Key=event.get("style_image"),
            Body=buffer.getvalue()
        )

def complete_job(event, context):
    job_id = event.get("job_id")
    table.update_item(
        Key={"job_id": job_id},
        UpdateExpression=f"SET #at = :val",
        ExpressionAttributeNames={
            '#at': 'status'
        },
        ExpressionAttributeValues={
            ':val': "completed"
        }
    )

def handle_error(event, context):
    job_id = event.get("job_id")
    table.update_item(
        Key={"job_id": job_id},
        UpdateExpression=f"SET #at = :val",
        ExpressionAttributeNames={
            '#at': 'status'
        },
        ExpressionAttributeValues={
            ':val': "failed"
        }
    )
