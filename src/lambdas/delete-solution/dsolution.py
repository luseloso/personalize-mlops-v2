from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    solutions = PERSONALIZE.list_solutions(datasetGroupArn=event['datasetGroup']['datasetGroupArn'])['solutions']
    for solution in solutions:
        PERSONALIZE.delete_solution(solutionArn=solution['solutionArn'])
    
    while PERSONALIZE.list_solutions(datasetGroupArn=event['datasetGroup']['datasetGroupArn'])['solutions'] != []:
        sleep(1)

    return event
