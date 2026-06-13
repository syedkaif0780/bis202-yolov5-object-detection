import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client("ssm")

INSTANCE_ID = "i-0164063fdaba586cb"
DEFAULT_BUCKET = "bis202-macheso-object-detection-2026"
DEFAULT_IMAGE = "bus.jpg"


def lambda_handler(event, context):
    logger.info("Lambda function started for YOLOv5 object detection")

    try:
        body = {}
        if event.get("body"):
            body = json.loads(event["body"])

        bucket = body.get("bucket", DEFAULT_BUCKET)
        image_name = body.get("image_name", DEFAULT_IMAGE)

        logger.info(f"Processing image: {image_name} from bucket: {bucket}")
        logger.info(f"Sending detection command to EC2 instance: {INSTANCE_ID}")

        response = ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    "cd /home/ubuntu/yolov5",
                    "mkdir -p /home/ubuntu/images",
                    f"aws s3 cp s3://{bucket}/input/{image_name} /home/ubuntu/images/{image_name} || echo 'ERROR: Download failed'",
                    f"/home/ubuntu/yolov5/yolov5-env/bin/python detect.py --weights yolov5s.pt --source /home/ubuntu/images/{image_name} --project runs/detect --name output --exist-ok",
                    f"for i in 1 2 3; do aws s3 cp runs/detect/output/{image_name} s3://{bucket}/output/{image_name} && echo 'Upload success' && break || echo \"Upload retry $i failed\" && sleep 2; done",
                    f"aws s3 ls s3://{bucket}/output/{image_name} && echo 'Verified in S3' || echo 'ERROR: File not found in S3'"
                ]
            }
        )

        command_id = response["Command"]["CommandId"]
        logger.info(f"Command sent successfully. Command ID: {command_id}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "YOLOv5 detection command sent successfully!",
                "command_id": command_id,
                "bucket": bucket,
                "image": image_name
            })
        }

    except Exception as e:
        logger.error(f"Error occurred while sending command: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to send YOLOv5 detection command",
                "error": str(e)
            })
        }
