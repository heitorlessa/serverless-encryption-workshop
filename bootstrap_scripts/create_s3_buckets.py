#!/usr/bin/env python
# Creates/Remove S3 buckets and add prefix sample

from __future__ import print_function
import boto3
import argparse

s3 = boto3.resource('s3')
lambda_environments = ['DEV/', 'PROD/', 'STAGE/']


def create_s3(bucket_name):
    """Creates given S3 Bucket name and prefix sample for Lambda function"""

    bucket = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': 'eu-west-1'})

    bucket.wait_until_exists()

    for prefix in lambda_environments:
        obj = bucket.Object(prefix)
        obj.put(
            ACL='private', Body='')

    return bucket


def main():

    # Quick arg parsing
    parser = argparse.ArgumentParser(
        description='Quick and dirty s3 bucket creation for demo.')
    parser.add_argument(
        '-c', '--create', help='Bucket name to be created', required=True)
    args = parser.parse_args()

    if args.create:
        try:
            ret = create_s3(args.create)
        except Exception, e:
            raise Exception("Operation failed due to {0}: ".format(e))


if __name__ == '__main__':
    main()
