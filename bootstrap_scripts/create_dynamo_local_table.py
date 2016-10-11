#!/usr/bin/env python
# Local development with:
#
#   Download URL: http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.zip
#   Start command: java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -inMemory
#
#   More info: http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html

from __future__ import print_function
import boto3, argparse
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
    'dynamodb', region_name='eu-west-1', endpoint_url='http://localhost:8000')

workshop_table = "workshop-encryption-service-lessa"

def create_table(table_name, rcu, wcu):
    """Creates DynamoDB table with Key as Primary/Hash key and Stage as Range key with given read/write capacity units (RCU/WCU)"""
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'stage',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'key',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'key',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'stage',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    return table

def main():

    # Quick arg parsing
    parser = argparse.ArgumentParser(description='Quick and dirty create dynamoDB local for demo.')
    parser.add_argument('-c','--create', help='Table name to be created', required=True)
    args = parser.parse_args()

    if args.create:
        try:
            ret = create_table(args.create, 5, 5)
            table = dynamodb.Table(args.create)
            table.put_item(
                Item={
                    'stage': 'dev',
                    'key': 'xxx'
                })

            response = table.query(
                KeyConditionExpression=Key('stage').eq('dev')  
            )
            item = response['Items'][0]            
        except Exception, e:
            raise Exception("Operation failed due to {0}: ".format(e))

if __name__ == '__main__':
    main()