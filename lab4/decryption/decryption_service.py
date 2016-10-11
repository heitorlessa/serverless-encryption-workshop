#-------------------------------------------------------------------------
# Name:        Decryption microservice for Lambda
# Purpose:     Demonstrate use of KMS DataKey and PyCrypto for Envelope encryption demo - No need for config handling due to Encrypt API metadata
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


class Crypter(object):
    """Crypter provides easy decryption through KMS Decrypt endpoint"""

    def __init__(self):
        self.unpad = lambda s: s[0:-ord(s[-1])]
        self.mode = AES.MODE_CBC

    # Get Datakey for decryption to use with AES
    def decrypt(self, data, cipher):
        try:
            encrypted_data = base64.decodestring(data)
            iv = encrypted_data[:16]
            decrypted_key = kms.decrypt(
                CiphertextBlob=base64.decodestring(cipher)).get('Plaintext')
        except Exception as e:
            raise Exception("Error occurred while getting data key - {0}".format(e))

        # Decrypt AES
        crypter = AES.new(decrypted_key, self.mode, iv)
        decrypted_data = crypter.decrypt(encrypted_data[16:])
        return self.unpad(decrypted_data)


def lambda_handler(event, context):

    # Basic input validation to avoid unnecessary KMS calls
    # More info on KMS Costs: https://aws.amazon.com/kms/pricing/
    try:
        cipher = event["cipher"]
        encrypted_message = event["data"] 
    except:
        error = {
            "status": 400,
            "message": "Invalid parameters - Please ensure required parameters are present"
        }
        raise Exception(json.dumps(error))

    crypter = Crypter()

    try:
        decrypted_message = crypter.decrypt(encrypted_message, cipher)
    except botocore.exceptions.ClientError as e:
        error = {
            "status": 400,
            "error": "Double check region and KMS Key ID - Message: {0}".format(e)
        }

        raise Exception(json.dumps(error))
    except Exception as e:
        error = {
            "status": 500,
            "error": "Error occurred while trying to decrypt data - Message: {0}".format(e)
        }

        raise Exception(json.dumps(error))

    return {
        'data': decrypted_message
    }
