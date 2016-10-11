> Disclaimer: **Code provided is for demo purpose only**

### Phase 2 - Configuration handling and versioning

Given that our first Lambda is now functional, let's dive into configuration handling and Lambda versioning for our function. 

Lab 2 leverages both local and remote configuration handling by making use of local packaging, DynamoDB and S3. Additionally, we explore how to locally debug our Lambda function.

Here's how this folder has been structured:

| Folder | Description |
| --- | --- | 
| **encryption** | Contains encryption microservice [code](encryption/encryption_service.py), [IAM Role policy](encryption/role_policy.json), [IAM Role Trust policy](encryption/role_trust_policy.json), JSON [test event](encryption/test-encryption.json) and a [fake Lambda context file](encryption/context.json). |
| **decryption** | Contains encryption microservice [code](decryption/decryption_service.py), [IAM Role policy](decryption/role_policy.json), [IAM Role Trust policy](decryption/role_trust_policy.json) and JSON [test event](decryption/test-decryption.json). |
| **config_sample** | Contains configuration handling sample code using [DynamoDB local](config_sample/dynamo/encryption_service.py) as well as [local configuration file](config_sample/within_package/encryption_service.py) that is used within Lambda package. |
| **Makefile** | Contains a [Makefile](Makefile) set of instructions to **bootstrap**, **build** and **test** both microservices locally. |
| **requirements.txt** | Contains a pip [requirements](requirements.txt) file to install *python dependencies* used by both services. |

---


#### Presentation 2 main topics 

* Lambda Aliases
* Configuration handling ideas
* Lab Architecture

#### Lab 2 main topics 

* S3 and DynamoDB Local structure
* Lambda versioning
* Configuration handling
* Local debugging

---

#### Appendix

Initializing s3 client via Python boto for [Minio](http://minio.io/):

```python
s3 = boto3.resource('s3', endpoint_url='http://<minio_IP>:9000', config=boto3.session.Config(signature_version='s3v4'))
```
