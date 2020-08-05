<br /><br />
<p align="center">
  <img width="240" src="assets/icon.png" />
</p><br />

# personalize-pipeline
> Step Functions automation workflow for Amazon Personalize.

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](contributing.md)
[![CodeBuild](https://s3-us-west-2.amazonaws.com/codefactory-us-west-2-prod-default-build-badges/passing.svg)](https://s3-us-west-2.amazonaws.com/codefactory-us-west-2-prod-default-build-badges/passing.svg)

Current version: **1.0.0**

Lead Maintainer: [Pedro Pimentel](mailto:pppimen@amazon.com)

## 📋 Table of content

 - [Installation](#install)
 - [Metrics](#metrics)
 - [Description](#description)
 - [Deployment & Usage](#deployment-and-usage)
 - [Configuration & Settings](#configuration-&-settings)
 - [See also](#see-also)

## 🚀 Install

In order to add this block, head to your project directory in your terminal and add it using NPM.

```bash
npm install @aws-blocks/personalize-pipeline
```

The **personalize-pipeline** project will be available in the `node_modules/@aws-blocks` directory.

## 📊 Metrics

The below metrics displays approximate values associated with deploying and using this block.

Metric | Value
------ | ------
**Type** | Architecture
**Installation Time** | 2 to 3 minutes
**Requirements** | [aws-cli](https://aws.amazon.com/cli/), [aws-sam](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
**Audience** | Developers, Solutions Architects

## 🔰 Description

This package contains the source code of a Step Functions pipeline that is able to perform 
multiple actions within **Amazon Personalize**, including the following:

- Dataset Group creation
- Datasets creation and import
- Solution creation
- Solution version creation

Once the steps are completed, the solution notifies the users of its completion through the
use of an SNS topic.

The below diagram describes the architecture of the solution:

![architecture](assets/architecture.png)


## 🎮 Deployment and Usage

With the SAM CLI installed, run the following command **inside the repository folder** to deploy the pipeline:

```bash
sam build --template cloudformation.yaml && sam deploy --guided
```

The pipeline will query your for an email and a default name for the parameter file.

Once deployed, the solution will create the **InputBucket**. Use it to upload your datasets
using the following structure:

```bash
Users/              # Users dataset(s) folder
Items/              # Items dataset(s) folder
Interactions/       # Interaction dataset(s) folder
``` 

After your datasets are submitted, upload the parameters file in **the root directory**. This step
 will start the step functions workflow.

## 🛠 Configuration

To use this tool you will need to propperly setup a **parameter file**. The parameter file 
contains all the necessary information to create the resources on Amazon Personalize. It fetches
the parameters using the [boto3 personalize client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html).

The file should include the following sections, **all mandatory**:
- `datasetGroup`
- `datasets`
- `solution`
- `campaign`

<details><summary>See a sample of the parameter file</summary>
<p>

```json
{
    "datasetGroup": {
        "name":"DatasetGroup"
    },
    "datasets": {
        "Interactions": {
            "name":"InteractionsDataset",
            "schema": {
              "type": "record",
              "name": "Interactions",
              "namespace": "com.amazonaws.personalize.schema",
              "fields": [
                {
                  "name": "USER_ID",
                  "type": "string"
                },
                {
                  "name": "ITEM_ID",
                  "type": "string"
                },
                {
                  "name": "TIMESTAMP",
                  "type": "long"
                }
              ],
              "version": "1.0"
            }
        },
        "Users": {
            "name": "UsersDataset",
                "schema": {
                "type": "record",
                "name": "Users",
                "namespace": "com.amazonaws.personalize.schema",
                "fields": [
                    {
                        "name": "USER_ID",
                        "type": "string"
                    },
                    {
                        "name": "GENDER",
                        "type": "string",
                        "categorical": true
                    },
                    {
                        "name": "AGE",
                        "type": "int"
                    }
                ],
                "version": "1.0"
            }
        }
    },
    "solution": {
        "name": "Solution",
        "performAutoML": true
    },
    "campaign": {
        "name": "Campaign",
        "minProvisionedTPS": 1
    }
}
```
</p>
</details>

## 📟 Example

In order to test the deployment please run the following command **inside the repository folder**:

```bash
aws s3 sync ./example/data s3://{YOURBUCKETNAME}

aws s3 cp ./example/params.json s3://{YOURBUCKETNAME}
```

This will start the execution of the Step Functions workflow. To follow the execution navigate
to the Step Functions section of the AWS Console and click on the **DeployStateMachine-xxx** state
machine.

> You will need to specify the correct S3 bucket name created before. The state machine 
starts when the parameter file is submitted to the S3 bucket.

## 👀 See Also

### How to define a schema

https://docs.aws.amazon.com/personalize/latest/dg/how-it-works-dataset-schema.html


### Parameters file structure

To view how to create your parameter file, visit [this example](./example/params.json).
Each section corresponds to an API call. 

> Consult all possible parameters for each section
visiting the [Personalize Boto3 Doc](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize.Client.create_dataset).