import subprocess
import json

from manage_p4d import *
    
#subprocess.run(["bash", "./init-cdk.sh"])

cdk_outputs_file = open("./game-studio/p4d-files/cdk-outputs.json")
data = json.load(cdk_outputs_file)

p4d_instance_id = data["GameStudioStack"]["InstanceID"]
p4d_server_address = "ssl:" + data["GameStudioStack"]["LoadBalancer"] + ":1666"
    
cdk_outputs_file.close()

configureP4V("super", p4d_server_address, p4d_instance_id)

deleteDepot("depot")

response = input("Add additional user? Enter y or n: ")
while (response == "y"):
    username = input("Enter Username: ")
    createUser(username)
    response = input("Add additional user? Enter y or n: ")
