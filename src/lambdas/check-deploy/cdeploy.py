from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    event['status'] = True
    CreateCampaignResponse = PERSONALIZE.describe_campaign(campaignArn=event['campaign']['campaignArn'])
    if CreateCampaignResponse['campaign']['status'] not in ['ACTIVE','CREATE FAILED']:
        event['status'] = False
    else:
        if CreateCampaignResponse['campaign']['status'] == 'CREATE FAILED':
            raise Exception

    return event