from boto3 import client
from time import sleep
from json import dumps
import os

SNS = client('sns')
def lambda_handler(event, context):
    return SNS.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=dumps(event)
    )