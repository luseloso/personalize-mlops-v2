from boto3 import client
from time import sleep

PERSONALIZE = client('personalize')

def lambda_handler(event, context):
    datasets = PERSONALIZE.list_datasets(datasetGroupArn=event['datasetGroup']['datasetGroupArn'])['datasets']
    for dataset in datasets:
        PERSONALIZE.delete_dataset(datasetArn=dataset['datasetArn'])

    while PERSONALIZE.list_datasets(datasetGroupArn=event['datasetGroup']['datasetGroupArn'])['datasets'] != []:
        sleep(1)

    PERSONALIZE.delete_dataset_group(datasetGroupArn=event['datasetGroup']['datasetGroupArn'])
    return event
