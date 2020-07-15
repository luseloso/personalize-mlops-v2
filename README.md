# sola cli

## About ##
This package provides you with an easy, fast and automatic way to provision Amazon Personalize solutions. It demands minimal setup interactions with it's resources. Specifics such as choosing algorithms and hyperparameters are __TBD__. 

Currently, this solution will provision your resources using Amazon's Personalize AutoML to tune-in hyperparameters and __HRNN__ as it's algorithm.
## Install ##
First, you will need to instal the _sam cli_, you can visit [this link](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) to get information on how to install it on your OS.
To install the package and it's dependencies, run the following command, inside the experso folder:

`$ pip install --editable .`

## Usage ##
To use this package you will need _at least_ the following files:
- __{MySchema}.json__: Your Interactions schema definition.
- __{MyDataset}.csv__: Your Interactions schema definition.
- __{Datasets}.json__: Your dataset schemas definition file, __following the structure__:
```json
{
    "datasets":[
        {
            "name": "MyDataset",
            "type": "[Items,Interactions,Users]",
            "schemafile": "path/to/MySchema.json",
            "csvfile": "path/to/MyDataset.csv"
        }, ...
    ]
}
```

Provided the files, to provision your resources on your AWS account, please run:

`$ sola deploy --name MySolution --datasetschema MySchema.json --outputfile {MyParams.json}`

This command will provision the following resources on your account:
- __SNS Topic__
- __S3 Bucket__ (Only if the option --bucket is not used)
- __Lambda functions__
- __Step Functions__
- __IAM Roles__

And provide you with a template file. To provision your Personalize solution, run the command:

`$ sola start --parameters {MyParams.json}`

You can also provide schemas and datasets on metadata for the USER and ITEMS entities.
To get detailed information on how to create your dataset schemas and datasets, please visit the [Personalize documentation](https://docs.aws.amazon.com/personalize/latest/dg/how-it-works-dataset-schema.html).


### Examples
For examples, please visit the `/example` folder.

## Help
__sola__ provides different options for its commands. To get a full list of provided commands and options run:

`$ sola COMMAND --help`
