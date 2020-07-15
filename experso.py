#!/usr/bin/env python

import click
import os
import json
from time import sleep
from boto3 import client
import subprocess
import inspect

@click.group()
def cli():
    '''
    sola -- Create your Personalize solution easily.\n
    Example usage: \n
    
    \b
        $ sola deploy --name MySolution --datasetschema MySchema.json --outputfile {MyParams.json}
        $ sola start --paramsfile {MyParams.json} 
    '''
@cli.command()
@click.option('--name', help='Name of your solution', required=True)
@click.option('--bucket', help ='Bucket name (if specified the pipeline will consider '
                                'that you also have uploaded your csv files)')
@click.option('--datasetschema', help='Dataset schema file', required=True)
@click.option('--outputfile', help='Output filename', required=True)
def deploy(name, bucket, datasetschema, newbucket,  outputfile):
    '''
    Deploys the basic resources on your AWS account and uploads all necessary data 
    on a S3 bucket.\n
    Example usage: \n
    \b
        $ sola deploy --name MySolution --datasetschema MySchema.json --outputfile {MyParams.json}
    '''
    cfn = client('cloudformation')
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    SCRIPT_DIR = os.path.dirname(os.path.abspath(filename))
    datasets = None 
    with open(datasetschema, 'r') as dTemplate: 
        datasets = json.loads(dTemplate.read())
    if not bucket:
        click.echo('\nCreating bucket ..')
        s3 = client('s3')
        template = None
        with open('{}/bucket.yaml'.format(SCRIPT_DIR), 'r') as bTemplate:
            template = bTemplate.read()
        stack = cfn.create_stack(
            StackName='{}-s3'.format(name),
            TemplateBody=template
        )
        while cfn.describe_stacks(StackName='{}-s3'.format(name))['Stacks'][0]['StackStatus'] == 'CREATE_IN_PROGRESS':
            sleep(1)
        bucket = cfn.describe_stacks(StackName='{}-s3'.format(name))['Stacks'][0]['Outputs'][0]['OutputValue']
        click.echo('Bucket created:\t{}'.format(bucket))
        click.echo('Uploading files ..')
        for dataset in datasets['datasets']:
            s3.upload_file(dataset['csvfile'], bucket, dataset['csvfile'])
            click.echo('Uploaded\t{}'.format(dataset['name']))
    os.system('mkdir .experso && cp -r {scrdir}/src/* ./.experso/'.format(scrdir=SCRIPT_DIR))
    for dataset in datasets['datasets']:
        os.system('cp {interactions} .experso/lambdas/import-data/definitions/{schema}.json'.format(
                    interactions=dataset['schemafile'], schema=dataset['type']))
    os.system('''cd .experso && sam package --template-file template.yaml --s3-bucket {} \\
                --output-template-file temp.yaml > /dev/null'''.format(bucket))
    os.system('''cd .experso && aws cloudformation deploy --template-file temp.yaml \\ 
                --stack-name experso-{} --capabilities CAPABILITY_IAM --parameter-overrides \\
                SNSTopicName={} NotificationEmail={}'''.format(name, name))
    os.system('rm -rf .experso')
    outputs = cfn.describe_stacks(StackName='experso-{}'.format(name))['Stacks'][0]['Outputs']
    for output in outputs:
        if output['OutputKey'] == 'DeployStateMachineArn':
            stArn = output['OutputValue']
            with open(outputfile, 'w') as parameters:
                json.dump({ 'name': name, 
                            'bucketName': bucket,
                            'stateMachineArn': stArn,
                            'datasets': datasets['datasets']
                          }, parameters)
            break

    click.echo('\n All done! Use the following command to deploy your Personalize solution: ')
    click.echo('\b    sola start --paramsfile {output}'.format(output=outputfile) )


'''
------------ TBD ------------
@click.option('--algorithm',
              type=click.Choice(['hrnn', 'pop', 'sims']),
              help='Your prefered algorithm')
@click.option('--automl/--no-auto', default=False, help='Perform Auto ML')
'''
@cli.command()
@click.option('--tps', type=int, default=1, help='Provisioned tps')
@click.option('--paramsfile', required=True, help='Parameters file')
def start(tps, paramsfile):
    '''
    Starts your Personalize deployment, using the state machine created by the deploy
    command. Upon completion a message will be submitted to the SNS topic also created 
    by the deploy command.\n
    Example usage:\n
    \b
        $ sola start --paramsfile {MyParams.json} 
    '''
    click.echo('Sending execution request ..')
    with open(paramsfile , 'r') as param_file:
        params = json.loads(param_file.read())
        params.update({'minProvisionedTPS': tps})
        sts = client('stepfunctions')
        sts.start_execution(
            stateMachineArn = params['stateMachineArn'],
            input=json.dumps(params)
        )
    click.echo('Request sent, please wait for the training to finish.')

@cli.command()
@click.option('--yes', is_flag=True, expose_value=False, help='Confirmation',
              prompt='This operation will destroy all personalize resources.\nAre you sure?')

def destroy(ctx):
    '''
    TBD
    '''
    click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))


if __name__ == '__main__':
    cli()
    # obj={}
