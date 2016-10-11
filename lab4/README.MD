> Disclaimer: **Code provided is for demo purpose only**

### Phase 4 - Lambda compiled libraries and build an API with API Gateway

In this part, we will implement envelope encryption into our services previously created and build an API to front requests so we can make it more friendly.

Lab 4 leverages a 3rd party library called PyCrypto that will allow us to implement envelope encryption by generating randomg KMS Data keys. We will also learn how compiled libraries should be imported within Lambda runtime. 

Additionally, we will make use of Swagger to not only document but to automate API creations within API Gateway, transform incoming/outgoing requests as well as dictate how often our users can leverage this service.

Here's how this folder has been structured:

| Folder | Description |
| --- | --- | 
| **encryption** | Contains encryption microservice [code](encryption/encryption_service.py), [IAM Role policy](encryption/role_policy.json), [IAM Role Trust policy](encryption/role_trust_policy.json), JSON [test event](encryption/test-encryption.json) and a [fake Lambda context file](encryption/context.json). |
| **decryption** | Contains encryption microservice [code](decryption/decryption_service.py), [IAM Role policy](decryption/role_policy.json), [IAM Role Trust policy](decryption/role_trust_policy.json) and JSON [test event](decryption/test-decryption.json). |
| **api** | Contains Swagger API definition for v1[code](api/swagger_importV1.yaml) and v2[code](api/swagger_importV2.yaml) of our API. |
| **compiled_lib** | Contains [PyCrypto dependency](https://github.com/Doerge/awslambda-pycrypto) compiled within Lambda compliance. |
| **Makefile** | Contains a [Makefile](Makefile) set of instructions to **bootstrap**, **build**, **test** and **deploy** both microservices. |
| **requirements.txt** | Contains a pip [requirements](requirements.txt) file to install *python dependencies* used by both services. |

---


#### Presentation 4 main topics 

* Brief to API Gateway
* Using API Gateway
* Lab Architecture

#### Lab 4 main topics 

* Working with compiled libraries
* Implementing Envelope Encryption
* Building a serverless encryption API
* Brainstorm on evolving this serverless API

