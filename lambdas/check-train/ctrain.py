from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    sVersionResponse = PERSONALIZE.describe_solution_version(
        solutionVersionArn = event['solutionVersionArn'])
    if sVersionResponse['solutionVersion']['status'] not in ['ACTIVE', 'CREATE FAILED']:
        event['status'] = False
    else: 
        if sVersionResponse['solutionVersion']['status'] == 'CREATE FAILED':
            raise Exception
        event['status'] = True
    return event
