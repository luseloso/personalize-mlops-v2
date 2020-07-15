# Amazon Personalize ML Ops V2

## About
This package provides you with an easy, fast and automatic way to provision Amazon Personalize solutions. It demands minimal setup interactions with it's resources. Specifics such as choosing algorithms and hyperparameters are __TBD__. 

![alt text](/img/architecture.png "Architecture")

## Install 
First, you will need to instal the _sam cli_, you can visit [this link](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) to get information on how to install it on your OS.

## Deployment and Usage

With the SAM CLI installed, run the following command inside the repository folder to deploy the pipeline:

`sam build --template cloudformation.yaml && sam deploy --guided`

The pipeline will query your for an email and a default name for the parameter file.

Once deployed, the solution will create the InputBucket. Use it to upload your datasets using the following structure:

```
Users/              # Users dataset(s) folder
Items/              # Items dataset(s) folder
Interactions/       # Interaction dataset(s) folder
```

After your datasets are submitted, upload the parameters file in the root directory. This step will start the step functions workflow.

## Configuration

To use this tool you will need to propperly setup a parameter file. The parameter file contains all the necessary information to create the resources on Amazon Personalize. It fetches the parameters using the boto3 personalize client.

The file should include the following sections, all mandatory:
```
    datasetGroup
    datasets
    solution
    campaign
```
<details>
<summary>See a sample of the parameter file</summary> 
<p> json { "datasetGroup": { "name":"DatasetGroup" }, "datasets": { "Interactions": { "name":"InteractionsDataset", "schema": { "type": "record", "name": "Interactions", "namespace": "com.amazonaws.personalize.schema", "fields": [ { "name": "USER_ID", "type": "string" }, { "name": "ITEM_ID", "type": "string" }, { "name": "TIMESTAMP", "type": "long" } ], "version": "1.0" } }, "Users": { "name": "UsersDataset", "schema": { "type": "record", "name": "Users", "namespace": "com.amazonaws.personalize.schema", "fields": [ { "name": "USER_ID", "type": "string" }, { "name": "GENDER", "type": "string", "categorical": true }, { "name": "AGE", "type": "int" } ], "version": "1.0" } } }, "solution": { "name": "Solution", "performAutoML": true }, "campaign": { "name": "Campaign", "minProvisionedTPS": 1 } } </p> </details>


## Example

In order to test the deployment please run the following command inside the repository folder:

`aws s3 sync ./example/data s3://{YOURBUCKETNAME}`

`aws s3 cp ./example/params.json s3://{YOURBUCKETNAME}`

This will start the execution of the Step Functions workflow. To follow the execution navigate to the Step Functions section of the AWS Console and click on the DeployStateMachine-xxx state machine.

**You will need to specify the correct S3 bucket name created before. The state machine starts when the parameter file is submitted to the S3 bucket.**

