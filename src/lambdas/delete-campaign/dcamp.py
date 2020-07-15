from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    campaignArns = set([campaign['campaignArn'] for campaign in PERSONALIZE.list_campaigns()['campaigns']])
    if event['campaign']['campaignArn'] in campaignArns:
        PERSONALIZE.delete_campaign(campaignArn=event['campaign']['campaignArn'])
        while PERSONALIZE.list_campaigns(solutionArn=event['campaign']['campaignArn'])['campaigns'] != []:
            sleep(1)
    return event

