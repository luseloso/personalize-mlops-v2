from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    solutionResponse=PERSONALIZE.create_solution(
        name=event['parameters']['name'],
        performHPO=True, #or False
        performAutoML=True, #or False
        datasetGroupArn=event['datasetGroup']['datasetGroupArn']
    )
    while PERSONALIZE.describe_solution(solutionArn=solutionResponse['solutionArn']
            )['solution']['status'] not in ['ACTIVE', 'CREATE FAILED']:
        sleep(1)

    sVersionResponse = PERSONALIZE.create_solution_version(solutionArn=solutionResponse['solutionArn'])

    event.update({
        'solutionArn': solutionResponse['solutionArn'],
        'solutionVersionArn': sVersionResponse['solutionVersionArn']
    })
    return event