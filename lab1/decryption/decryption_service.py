#-------------------------------------------------------------------------------
# Name:        Decryption microservice for Lambda
# Purpose:     Demonstrate use of KMS Decrypt endpoint that can encrypt up to 4KB of data
# Author:      Heitor Lessa
#-------------------------------------------------------------------------------

import boto3, logging, base64, json, botocore

## Basic Logging definition
logger = logging.getLogger()
logger.setLevel(logging.INFO)

kms = boto3.client('kms')

class Crypter(object):
    """Crypter provides easy decryption through KMS Decrypt endpoint"""
    def __init__(self):
        pass
        
    # Leverage KMS Decrypt and base64-decode encrypted blob
    # More info on Decrypt API: https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html
    def decrypt(self, message):
        ret = kms.decrypt(CiphertextBlob=base64.decodestring(message))
        decrypted_data = ret.get('Plaintext')

        return decrypted_data

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

    crypter = Crypter()

    try:
        decrypted_message = crypter.decrypt(message)
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