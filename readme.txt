BIS202 Assignment 2 - YOLOv5 Object Detection System

Name: Syed Kaif
Student Number: 240413

PROJECT DESCRIPTION:
A cloud-based object detection system using YOLOv5 on AWS.
Users send an image name through an API. The system runs YOLOv5 
detection on an EC2 instance and stores the result in Amazon S3.

The architecture uses API Gateway as the entry point, Lambda as a 
lightweight trigger, EC2 for running the detection model, and S3 
for storing input images and detection outputs.

AWS Services: API Gateway, Lambda, EC2, S3, IAM, SSM
Model: YOLOv5s (Ultralytics)

API Endpoint:
https://ufmgf87apc.execute-api.ap-southeast-2.amazonaws.com/prod/detect

FOLDERS:
- code/   : Lambda function source code
- deploy/ : Deployable Lambda file
