> Disclaimer: **Code provided is for demo purpose only**
**Before start, make sure you have already created minimum resources**

### Phase 1 - Intro to Lambda and KMS

We introduce AWS Lambda service and a brief intro into Key Management Service (KMS). 

Lab 1 is aimed to give a hands on overview on AWS Lambda essentials and to understand how to locally test/execute/package a Lambda function.

Here's how this folder has been structured:

| Folder | Description |
| --- | --- | 
| **encryption** | Contains encryption microservice [code](encryption/encryption_service.py), [IAM Role policy](encryption/role_policy.json), [IAM Role Trust policy](encryption/role_trust_policy.json) and JSON [test event](encryption/test-encryption.json). |
| **decryption** | Contains encryption microservice [code](decryption/decryption_service.py), [IAM Role policy](decryption/role_policy.json), [IAM Role Trust policy](decryption/role_trust_policy.json) and JSON [test event](decryption/test-decryption.json). |
| **Makefile** | Contains a [Makefile](Makefile) set of instructions to **bootstrap**, **build** and **test** both microservices locally. |
| **requirements.txt** | Contains a pip [requirements](requirements.txt) file to install *python dependencies* used by both services. |

---

#### Presentation 1 main topics 

* What AWS Lambda is
* Brief intro into KMS
* Lab Architecture

#### Lab 1 main topics 

* Lambda UI: Look and feel
* Basic Error handling
* Local testing with Emulambda
* ZIP packaging

---

#### Appendix

Creating minimum resources via Cloudformation:

```bash
aws cloudformation create-stack --stack-name "workshop-test" --template-body file://cloudformation/minimum_resources.yaml --capabilities="CAPABILITY_IAM" --parameters ParameterKey=User,ParameterValue=$USER --disable-rollback
```

Testing KMS Encrypt permission via CLI:

```python
aws kms encrypt --key-id <keyID> --plaintext "Testing" --output text --region eu-west-1
```
