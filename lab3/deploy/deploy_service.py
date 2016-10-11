#-------------------------------------------------------------------------
# Name:        Deploy service for Lambda
# Purpose:     Demonstrate use of S3 Event Notifications, S3 Object Metadata to deploy lambda functions: (S3->Lambda->Lambda deploy function->Update target Lambda function)
# Author:      Heitor Lessa
#-------------------------------------------------------------------------

from __future__ import print_function
import json
import boto3
import time
import urllib

s3 = boto3.client('s3')
_lambda = boto3.client('lambda')


def publish_version(metadata):
    try:
        _lambda.publish_version(
            FunctionName=metadata['name'],
            Description=metadata['metadata'])
    except Exception, e:
        raise Exception("Error while trying to publish a new version - {0}".format(
            e))


def update_lambda_code(metadata):

    try:
        _lambda.update_function_code(
            FunctionName=metadata['name'],
            S3Bucket=metadata['bucket'],
            S3Key=metadata['object'],
            Publish=metadata['publish'])
    except Exception, e:
        raise Exception("Error while trying to update a new version - {0}".format(
            e))

    publish_version(metadata)


def get_metadata(bucket, obj):

    try:
        print(obj)
        print(bucket)
        ret = s3.head_object(
            Bucket=bucket,
            Key=obj
        )
        metadata = ret['Metadata']['description']

        return metadata
    except Exception, e:
        raise Exception("Error while trying to gather object metadata - {0}".format(
            e))


def lambda_handler(event, context):
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'])
    #keyVersion = urllib.unquote_plus(event['Records'][0]['s3']['object']['versionId'])
    bucket = event['Records'][0]['s3']['bucket']['name']
    region = event['Records'][0]['awsRegion']
    obj_metadata = get_metadata(bucket, key)

    lambda_metadata = {
        'bucket': bucket,
        'object': key,
        'name': key.strip('.zip').split('/')[1],
        'publish': False,
        'metadata': obj_metadata
    }

    try:
        print("Updating Lambda function...")
        update_lambda_code(lambda_metadata)

        return "Update complete"
    except Exception as e:
        print('Error getting object {} from bucket {}'.format(key, bucket))
        raise e
