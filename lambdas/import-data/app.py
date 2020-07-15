import json
from boto3 import client
from time import sleep
from datetime import datetime
from random import randint
import os

PERSONALIZE=client('personalize')

def create_dGroup(name):
    dgResponse=PERSONALIZE.create_dataset_group(name = name)
    print('Creating Dataset Group ..')
    while PERSONALIZE.describe_dataset_group(
        datasetGroupArn=dgResponse['datasetGroupArn'])['datasetGroup']['status'] not in ['ACTIVE', 'CREATE FAILED']:
        sleep(5)
    print('Dataset Group Created')
    return dgResponse

def lambda_handler(event, context):
    dgResponse = create_dGroup(name=event['name'])
    importJobList = []
    for dataset in event['datasets']:
        with open('definitions/{}.json'.format(dataset['type'])) as schemaFile:
            schemaResponse = PERSONALIZE.create_schema(
                name='{}{}'.format(dataset['name'], randint(0,100000)),
                schema=schemaFile.read()
            )
            dsetResponse=PERSONALIZE.create_dataset(
                name='{}{}'.format(dataset['name'], randint(0,100000)),
                schemaArn=schemaResponse['schemaArn'],
                datasetGroupArn=dgResponse['datasetGroupArn'],
                datasetType=dataset['type']
            )
            while PERSONALIZE.describe_dataset(datasetArn=dsetResponse['datasetArn']
                    )['dataset']['status'] not in ['ACTIVE','CREATE FAILED']:
                sleep(5)
            
            if PERSONALIZE.describe_dataset(datasetArn=dsetResponse['datasetArn'])['dataset']['status'] == 'ACTIVE':
                importJobList.append(
                    PERSONALIZE.create_dataset_import_job(
                        jobName='{}_job_{}'.format(dataset['name'], randint(0,100)),
                        datasetArn=dsetResponse['datasetArn'],
                        dataSource={'dataLocation':'s3://{bucket}/{file}'.format(
                                    bucket=event['bucketName'], file=dataset['csvfile'])},
                        roleArn=os.environ['PERSONALIZE_ROLE_ARN']
                    )
                )
            else:
                raise Exception

    return {'status': False,
            'parameters': event,
            'datasetGroup': dgResponse,
            'importJobList': importJobList}