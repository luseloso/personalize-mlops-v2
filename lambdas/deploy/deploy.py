from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    campaignResponse = PERSONALIZE.create_campaign(
        name = event['parameters']['name'],
        solutionVersionArn = event['solutionVersionArn'],
        minProvisionedTPS = event['parameters']['minProvisionedTPS']
    )

    event['campaign'] = campaignResponse
    return event