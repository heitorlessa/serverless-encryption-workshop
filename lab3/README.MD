> Disclaimer: **Code provided is for demo purpose only**

### Phase 3 - Configuration handling and versioning

As our Lambda function picks up the latest KMS ID through S3 per staging environment, let's learn how other AWS Services integrate with Lambda via different Execution Models.

Lab 3 makes use of S3 to demonstrate one of Lambda execution models in practice and how deployment of our Lambda function could be done by leveraing S3 Events.

Here's how this folder has been structured:

| Folder | Description |
| --- | --- | 
| **encryption** | Contains encryption microservice [code](encryption/encryption_service.py), [IAM Role policy](encryption/role_policy.json), [IAM Role Trust policy](encryption/role_trust_policy.json), JSON [test event](encryption/test-encryption.json) and a [fake Lambda context file](encryption/context.json). |
| **decryption** | Contains encryption microservice [code](decryption/decryption_service.py), [IAM Role policy](decryption/role_policy.json), [IAM Role Trust policy](decryption/role_trust_policy.json) and JSON [test event](decryption/test-decryption.json). |
| **deploy** | Contains deploy microservice [code](deploy/deploy_service.py), [IAM Role policy](deploy/role_policy.json), [IAM Role Trust policy](deploy/role_trust_policy.json) and JSON [test event](deploy/test-deploy.json). |
| **Makefile** | Contains a [Makefile](Makefile) set of instructions to **bootstrap**, **build**, **test** and **deploy** both microservices. |
| **requirements.txt** | Contains a pip [requirements](requirements.txt) file to install *python dependencies* used by both services. |

---


#### Presentation 3 main topics 

* Lambda Execution Model
* Lambda integration with other AWS Services
* Lab Architecture

#### Lab 3 main topics 

* Creating a deployment function
* Lambda and S3 integration
* Rolling back strategies (discussion)

---

#### Appendix

Uploading an object to S3 with embedded metadata:

```bash
aws s3 cp <file> s3://<bucket_name> --metadata 'description="message into object"'
```

Retrieving object metadata via head operation:

```bash
s3api head-object --bucket <bucket_name> --key <key> --query 'Metadata'
```
