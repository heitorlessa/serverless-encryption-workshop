# Service Vars
ENC_SERVICE="encryption/encryption_service.py"
ENC_NAME="workshop-encryption-service-${USER}"

DEC_SERVICE="decryption/decryption_service.py"
DEC_NAME="workshop-decryption-service-${USER}"

# VirtualEnv vars
VENV="_venv"
VENV_LIBS="${VENV}/lib/python2.7/site-packages"
BASE=$(PWD)

# Emulambda Vars
# ENC_IAM_ROLE="arn:aws:iam::<accountId>:role/${ENC_NAME}"
# DEC_IAM_ROLE="arn:aws:iam::<accountId>:role/${DEC_NAME}"


# help credit (https://gist.github.com/prwhite/8168133)
help: ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

target: help
	exit 0

all: bootstrap build-encryption build-decryption clean ## -> Creates virtual env, package both encryption/decryption service and removes virtual env altogether

clean: ## -> Deletes current virtual env environment
	$(info "[-] Who needs all that anyway? Destroying environment....")
	rm -rf ./${VENV}
	rm -rf ./*.zip

build-encryption: bootstrap ## -> Packages encryption lambda function into acceptable ZIP format
	$(info "[+] Building Lambda package at ${BASE}/${ENC_NAME}.zip")
	rm -rf ${VENV}/dist/*; \
	cp -R ${VENV_LIBS}/* ${VENV}/dist/; \
	cp ${ENC_SERVICE} ${VENV}/dist/; \
	cd ${VENV}/dist && zip -r ${BASE}/${ENC_NAME}.zip *; \
	$(info "[*] Build complete: ${BASE}/${ENC_NAME}.zip")

build-decryption: bootstrap ## -> Packages decryption lambda function into acceptable ZIP format
	$(info "[+] Building Lambda package at ${BASE}/${DEC_NAME}.zip")
	rm -rf ${VENV}/dist/*; \
	cp -R ${VENV_LIBS}/* ${VENV}/dist/; \
	cp ${DEC_SERVICE} ${VENV}/dist/; \
	cd ${VENV}/dist && zip -r ${BASE}/${DEC_NAME}.zip *; \
	$(info "[*] Build complete: ${BASE}/${DEC_NAME}.zip")

create-s3: bootstrap ## Creates S3 Bucket for both lambda functions
	$(info "[+] Creating the following S3 buckets: ${ENC_NAME} ${DEC_NAME}")
	python ../bootstrap_scripts/create_s3_buckets.py -c ${ENC_NAME}
	python ../bootstrap_scripts/create_s3_buckets.py -c ${DEC_NAME}

create-dynamo: bootstrap ## Creates DynamoDB local table and item sample for both lambda functions
	$(info "[+] Creating the following DynamoDB local tables: ${ENC_NAME} ${DEC_NAME}")
	python bootstrap_scripts/create_dynamo_local_table.py -c ${ENC_NAME}
	python bootstrap_scripts/create_dynamo_local_table.py -c ${DEC_NAME}

test-encryption: bootstrap ## -> Use Emulambda to test encryption function
ifndef ENC_IAM_ROLE
   $(error "[!] Missing ENC_IAM_ROLE variable - Export env with full ARN")
endif
	$(info "[+] Testing ${ENC_NAME} function locally")
	test -f test-encryption.json && test -f context.json || (echo "[!] Test event/context file not found"; exit 1); \
	source ${VENV}/bin/activate; \
	cd encryption/; \
	emulambda encryption_service.lambda_handler test-encryption.json context.json -v -r ${ENC_IAM_ROLE}

test-decryption: bootstrap ## -> Use Emulambda to test decryption function
ifndef DEC_IAM_ROLE
   $(error "[!] Missing DEC_IAM_ROLE variable - Export env with full ARN")
endif
	$(info "[+] Testing ${DEC_NAME} function locally")
	test -f decryption/test-decryption.json || (echo "[!] Test event/context file not found"; exit 1); \
	source ${VENV}/bin/activate; \
	cd decryption/; \
	emulambda decryption_service.lambda_handler test-decryption.json -v -r ${DEC_IAM_ROLE}

bootstrap: _venv _emulambda # creates environment and install emulambda into virtual envs
	test -d ${VENV}/dist || mkdir ${VENV}/dist
	
_emulambda: # install emulambda into current virtual env
	test -d ${VENV}/emulambda && exit 0 || source ${VENV}/bin/activate && \
	git clone https://github.com/heitorlessa/emulambda ${VENV}/emulambda && \
	cd ${VENV}/emulambda && pip install -e .

_venv: # creates virtual env and install dependencies (requirements.txt)
	$(info "[+] Creating Virtual environment and installing dependencies")
	test -f ${VENV} && exit 0 || virtualenv ${VENV}
	source ${VENV}/bin/activate; pip install -r requirements.txt
