#-------------------------------------------------------------------------
# Name:        Encryption microservice for Lambda
# Purpose:     Demonstrate use of KMS Encrypt endpoint, configuration handling via local packaging
# Author:      Heitor Lessa
#-------------------------------------------------------------------------

import boto3
import logging
import base64
import json
import botocore
import pdb

# Basic Logging definition
logger = logging.getLogger()
logger.setLevel(logging.INFO)

kms = boto3.client('kms')
configFile = "config.json"


class Crypter(object):
    """Crypter provides easy encryption through KMS Encrypt endpoint"""

    def __init__(self, KMSkey):
        self.key = KMSkey

    # Leverage KMS Encrypt and base64-encode encrypted blob
    # More info on Encrypt API:
    # https://docs.aws.amazon.com/kms/latest/APIReference/API_Encrypt.html
    def encrypt(self, message):
        ret = kms.encrypt(KeyId=self.key, Plaintext=message)
        encrypted_data = base64.encodestring(ret.get('CiphertextBlob'))

        return encrypted_data


def get_config(context):

    try:
        with open(configFile) as f:
            config = json.load(f)

    except IOError as e:
        raise Exception("Does {0} exist locally?".format(configFile))

    return config


def lambda_handler(event, context):

    # Basic input validation to avoid unnecessary KMS calls
    # More info on KMS Costs: https://aws.amazon.com/kms/pricing/
    try:
        message = event["data"]
    except:
        error = {
            "status": 400,
            "error": "Invalid parameters - Please ensure required parameters are present"
        }
        raise Exception(json.dumps(error))

    try:
        logging.info("[+] Loading config locally")
        logging.info("[*] Function Version: " + context.function_version)
        logging.info("[*] Function Name: " + context.function_name)

        config = get_config(context)
    except Exception as e:
        error = {
            "status": 400,
            "error": "Error occurred while trying to obtain configuration - Message: {0}".format(e)
        }

        raise Exception(json.dumps(error))

    crypter = Crypter(config['key'])

    try:
        encrypted_message = crypter.encrypt(message)
    except botocore.exceptions.ClientError as e:
        error = {
            "status": 400,
            "error": "Double check region and KMS Key ID - Message: {0}".format(e)
        }

        raise Exception(json.dumps(error))
    except Exception as e:
        error = {
            "status": 500,
            "error": "Error occurred while trying to encrypt data - Message: {0}".format(e)
        }

        raise Exception(json.dumps(error))

    return {
        'data': encrypted_message
    }
