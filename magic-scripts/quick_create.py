import subprocess
import json
import re
from datetime import datetime

from manage_p4d import *

subprocess.run(["sudo", "bash", "./game-studio/p4d-files/install-p4d.sh"])

team = input("Enter a Team Name (a-z or A-Z or 0-9 or -): ")
formatted_team = re.sub(r'[^a-zA-Z0-9-]', '', team)
print("Team name set: " + formatted_team)
subprocess.run(["cp", "./game-studio/app.template", "./game-studio/app.py"])
subprocess.run(["sed", "-i", "s/$TEAM/" + formatted_team + "/g", "./game-studio/app.py"])

user = input("Enter a Username (a-z or A-Z or 0-9 or _.-): ")
formatted_user = re.sub(r'[^a-zA-Z0-9_.-]', '', user)
print("Username set: " + formatted_user)
subprocess.run(["cp", "./game-studio/p4d-files/configure-p4d.template", "./game-studio/p4d-files/configure-p4d.sh"])
subprocess.run(["sed", "-i", "s/$P4USER/" + formatted_user + "/g", "./game-studio/p4d-files/configure-p4d.sh"])

super_user = formatted_user

subprocess.run(["bash", "./game-studio/init-cdk.sh"])

cdk_outputs_file = open("./game-studio/p4d-files/cdk-outputs.json")
data = json.load(cdk_outputs_file)

p4d_instance_id = data[formatted_team + "-GameStudioStack"]["InstanceID"]
p4d_server_address = "ssl:" + data[formatted_team + "-GameStudioStack"]["LoadBalancer"] + ":1666"
    
cdk_outputs_file.close()

passwd = input("Enter super user password: ")
configureP4V(super_user, p4d_server_address, passwd)
#configureP4V(super_user, p4d_server_address, p4d_instance_id)
#changePassword(super_user)

deleteDepot("depot")

users = []
response = input("Add additional unser? Enter y or n: ")
while (response == "y"):
    user = input("Enter a Username (a-z or A-Z or 0-9 or _.-): ")
    formatted_user = re.sub(r'[^a-zA-Z0-9_.-]', '', user)
    print("Username set: " + formatted_user)
    createUser(formatted_user)
    users.append(formatted_user)
    response = input("Add additional user? Enter y or n: ")

# Update Typemap   
file = open("./game-studio/p4d-files/typemap.p4s", "r")
subprocess.run(["p4", "typemap", "-i"], input=file.read().encode("utf-8"))
file.close()

if users:
    # Update Protections
    protect = subprocess.run(["p4", "protect", "-o"], capture_output=True)
    file = open("./game-studio/p4d-files/protect.p4s", "w")
    file.write(protect.stdout.decode("utf-8"))
    protections = "\n\tadmin group Developers * //...\n"
    file.write(protections)
    file.close()
    file = open("./game-studio/p4d-files/protect.p4s", "r")
    subprocess.run(["p4", "protect", "-i"], input=file.read().encode("utf-8"))
    file.close()
    
    # Update Groups
    users_str = "Users: \t\t" + super_user
    for user in users:
        users_str += "\n\t\t" + user
    file = open("./game-studio/p4d-files/Developers.template", "r")
    file_data = file.read()
    file_data = file_data.replace("Owners:",  "Owners: \t" + super_user)
    file_data = file_data.replace("Users:",  users_str)
    file.close()
    file = open("./game-studio/p4d-files/Developers.p4s", "w")
    file.write(file_data)
    file.close()
    file = open("./game-studio/p4d-files/Developers.p4s", "r")
    subprocess.run(["p4", "group", "-i"], input=file.read().encode("utf-8"))
    print(file_data)
    file.close()

project_name = input("Enter a Project Name (a-z or A-Z or 0-9): ")
formatted_project_name = re.sub(r'[^a-zA-Z0-9]', '', project_name)
print("Project name set: " + formatted_project_name)
subprocess.run(["bash", "./game-studio/p4d-files/create-stream.sh", formatted_project_name, super_user])
    

print("Congrats on setting up your own game studio!\n")
print("Server: " + p4d_server_address)
print("Username: " + super_user)
