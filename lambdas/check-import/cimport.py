from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    event['status'] = True
    for job in event['importJobList']: 
        if PERSONALIZE.describe_dataset_import_job(datasetImportJobArn=job['datasetImportJobArn'])['datasetImportJob']['status'] not in ['ACTIVE', 'CREATE FAILED']:
            event['status'] = False
            break
    return event
