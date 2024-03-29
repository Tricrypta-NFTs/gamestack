#!bin/bash
cd gamestack
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy --outputs-file ./p4d-generated-files/cdk-outputs.json