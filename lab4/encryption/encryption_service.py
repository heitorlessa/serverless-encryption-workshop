#-------------------------------------------------------------------------
# Name:        Encryption microservice for Lambda
# Purpose:     Demonstrate use of KMS DataKey and PyCrypto for Envelope encryption demo
# Author:      Heitor Lessa
#-------------------------------------------------------------------------

import boto3
import logging
import base64
import json
import botocore
from Crypto.Cipher import AES
from Crypto import Random

# Basic Logging definition
logger = logging.getLogger()
logger.setLevel(logging.INFO)

kms = boto3.client('kms')
s3 = boto3.client('s3')


class Crypter(object):
    """Crypter provides envelope encryption through KMS datakey and AES"""

    def __init__(self, KMSkey):
        self.blockSize = 16
        self.pad = lambda s: s + (self.blockSize - len(s) % self.blockSize) * \
            chr(self.blockSize - len(s) % self.blockSize)
        self.iv = Random.new().read(AES.block_size)  # initialization vector
        self.mode = AES.MODE_CBC
        self.key = KMSkey

    # Get Datakey for encryption to be used with AES
    def encrypt(self, message):
        try:
            datakey = kms.generate_data_key(KeyId=self.key, KeySpec='AES_256')
            cipherBlob = base64.encodestring(datakey.get('CiphertextBlob'))
            plaintext_key = datakey.get('Plaintext')
            padded = self.pad(message)
        except Exception, e:
            raise Exception("Error occurred while generating data key - {0}".format(e))

        # Encrypt data using AES with KMS generated data key
        crypter = AES.new(plaintext_key, self.mode, self.iv)
        encrypted_data = base64.encodestring(self.iv + crypter.encrypt(padded))

        return encrypted_data, cipherBlob


def get_config(context):

    try:
        if "LATEST" not in context.function_version:
            stage = context.function_version
        else:
            stage = "DEV"

        config_obj = s3.get_object(
            Bucket=context.function_name, Key=stage + '/config.json')
        config = json.loads(config_obj['Body'].read())

    except Exception, e:
        raise Exception("Does {0} exist?".format(
            context.function_version.lower()))

    return config


def lambda_handler(event, context):

    # Basic input validation to avoid unnecessary KMS calls
    # More info on KMS Costs: https://aws.amazon.com/kms/pricing/
    try:
        message = event["data"]
    except:
        error = {
            "status": 400,
            "message": "Invalid parameters - Please ensure required parameters are present"
        }
        raise Exception(json.dumps(error))

    try:
        logging.info("[+] Loading config from S3")
        logging.info("[*] Function Version: " + context.function_version)
        logging.info("[*] Function Name: " + context.function_name)

        config = get_config(context)
    except Exception as e:
        error = {
            "status": 500,
            "error": "Error occurred while trying to obtain configuration - Message: {0}".format(e)
        }

        raise Exception(json.dumps(error))

    crypter = Crypter(config['key'])

    try:
        encrypted_message, cipher = crypter.encrypt(message)
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
        'data': encrypted_message,
        'cipher': cipher
    }
