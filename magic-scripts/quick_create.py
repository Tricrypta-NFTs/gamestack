import subprocess
import json
import re

from manage_p4d import *

team = input("Enter a Team Name (a-z or A-Z or 0-9 or -): ")
formatted_team = re.sub(r'[^a-zA-Z0-9-]', '', team)
print("Team name set: " + formatted_team)
subprocess.run(["cp", "./game-studio/app.template", "./game-studio/app.py"])
subprocess.run(["sed", "-i", "s/$TEAM/" + formatted_team + "/g", "./game-studio/app.py"])

users = []
user = input("Enter a Username (a-z or A-Z or 0-9 or _.-): ")
formatted_user = re.sub(r'[^a-zA-Z0-9_.-]', '', user)
print("Username set: " + formatted_user)
users.append(formatted_user)

response = input("Add additional unser? Enter y or n: ")
while (response == "y"):
    user = input("Enter a Username (a-z or A-Z or 0-9 or _.-): ")
    formatted_user = re.sub(r'[^a-zA-Z0-9_.-]', '', user)
    print("Username set: " + formatted_user)
    users.append(formatted_user)
    response = input("Add additional user? Enter y or n: ")
    
project_name = input("Enter a Project Name (a-z or A-Z or 0-9): ")
formatted_project_name = re.sub(r'[^a-zA-Z0-9]', '', project_name)
print("Project name set: " + formatted_project_name)


subprocess.run(["sudo", "bash", "./game-studio/p4d-files/install-p4d.sh"])
    
subprocess.run(["cp", "./game-studio/p4d-files/configure-p4d.template", "./game-studio/p4d-files/configure-p4d.sh"])
subprocess.run(["sed", "-i", "s/$P4USER/" + users[0] + "/g", "./game-studio/p4d-files/configure-p4d.sh"])
subprocess.run(["bash", "./game-studio/init-cdk.sh"])
subprocess.run(["mkdir", "-p", "./game-studio/p4d-generated-files/"])

cdk_outputs_file = open("./game-studio/p4d-generated-files/cdk-outputs.json")
data = json.load(cdk_outputs_file)

p4d_instance_id = data[formatted_team + "-GameStudioStack"]["InstanceID"]
p4d_server_address = "ssl:" + data[formatted_team + "-GameStudioStack"]["LoadBalancer"] + ":1666"
    
cdk_outputs_file.close()

configureP4V(users[0], p4d_server_address, p4d_instance_id)
print("Default Password: " + p4d_instance_id)
changePassword(users[0])

deleteDepot("depot")

for user in users:
    if (user == users[0]):
        continue
    else:
        createUser(user)


# Update Typemap   
file = open("./game-studio/p4d-files/typemap.p4s", "r")
subprocess.run(["p4", "typemap", "-i"], input=file.read().encode("utf-8"))
file.close()

subprocess.run(["bash", "./game-studio/p4d-files/create-stream.sh", formatted_project_name, users[0]])

if (len(users) > 1):
    # Update Protections
    protect = subprocess.run(["p4", "protect", "-o"], capture_output=True)
    file = open("./game-studio/p4d-generated-files/protect.p4s", "w")
    file.write(protect.stdout.decode("utf-8"))
    protections = "\n\tadmin group Developers * //" + formatted_project_name + "/...\n"
    file.write(protections)
    file.close()
    file = open("./game-studio/p4d-generated-files/protect.p4s", "r")
    subprocess.run(["p4", "protect", "-i"], input=file.read().encode("utf-8"))
    file.close()
    
    # Update Groups
    formatted_users = "Users: " 
    for user in users:
            formatted_users += "\n\t\t" + user
    file = open("./game-studio/p4d-files/Developers.template", "r")
    file_data = file.read()
    file_data = file_data.replace("Owners:",  "Owners: \t" + users[0])
    file_data = file_data.replace("Users:",  formatted_users)
    file.close()
    file = open("./game-studio/p4d-generated-files/Developers.p4s", "w")
    file.write(file_data)
    file.close()
    file = open("./game-studio/p4d-generated-files/Developers.p4s", "r")
    subprocess.run(["p4", "group", "-i"], input=file.read().encode("utf-8"))
    print(file_data)
    file.close()

print("\n\n\nCongrats on setting up your own game studio!\n")
print("Server: " + p4d_server_address)
print("Username: " + users[0])
