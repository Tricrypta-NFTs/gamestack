import subprocess
import json
import re
import time

from manage_p4d import *

team = input("Enter a Team Name (a-z or A-Z or 0-9 or -): ")
formatted_team = re.sub(r'[^a-zA-Z0-9-]', '', team)
print("Team name set: " + formatted_team)
subprocess.run(["cp", "./gamestack/app.template", "./gamestack/app.py"])
subprocess.run(["sed", "-i", "s/$TEAM/" + formatted_team + "/g", "./gamestack/app.py"])

users = []
users.append('johanv')
users.append('antonin')
users.append('dev_01')
users.append('dev_02')
users.append('dev_03')
    
project_name = input("Enter a Project Name (a-z or A-Z or 0-9): ")
formatted_project_name = re.sub(r'[^a-zA-Z0-9]', '', project_name)
print("Project name set: " + formatted_project_name)
print("24 - Starting install-p4d.sh");
subprocess.run(["sudo", "bash", "./gamestack/p4d-files/install-p4d.sh"])
print("26 - cp");    
subprocess.run(["cp", "./gamestack/p4d-files/configure-p4d.template", "./gamestack/p4d-files/configure-p4d.sh"])
print("28 - sed")
subprocess.run(["sed", "-i", "s/$P4USER/" + users[0] + "/g", "./gamestack/p4d-files/configure-p4d.sh"])
print("30 - bash init-cdk")
subprocess.run(["bash", "./gamestack/init-cdk.sh"])

timer = 300
while(timer > 0):
    print("Instance processing health checks: " + str(timer) + " seconds remaining...", end="\r")
    timer -= 1
    time.sleep(1)

print("39 - bash init-cdk")
subprocess.run(["mkdir", "-p", "./gamestack/p4d-generated-files/"])

print("42 - cdk-outputs")
cdk_outputs_file = open("./gamestack/p4d-generated-files/cdk-outputs.json")
print("44 - json_load")
data = json.load(cdk_outputs_file)
p4d_instance_id = data[formatted_team + "-GameStudioStack"]["InstanceID"]
p4d_server_address = "ssl:" + data[formatted_team + "-GameStudioStack"]["LoadBalancer"] + ":1666"
cdk_outputs_file.close()

print("50 - configurep4v")
configureP4V(users[0], p4d_server_address, p4d_instance_id)
print("Please set a password for " + users[0])
print("Old Password: " + p4d_instance_id)
changePassword(users[0])

print("56 - delete depot")
deleteDepot("depot")

for user in users:
    if (user == users[0]):
        continue
    else:
        print("Please set a password for " + users[0])
        createUser(user)


# Update Typemap   
file = open("./gamestack/p4d-files/typemap.template", "r")
file_data = file.read()
file.close()
file = open("./gamestack/p4d-generated-files/typemap.p4s", "w")
file_data = file_data.replace("depot",  formatted_project_name)
file.write(file_data)
file.close()
file = open("./gamestack/p4d-generated-files/typemap.p4s", "r")
subprocess.run(["p4", "typemap", "-i"], input=file.read().encode("utf-8"))
file.close()

# Create Stream
subprocess.run(["bash", "./gamestack/p4d-files/create-stream.sh", formatted_project_name, users[0]])

# Check for additional users
if (len(users) > 1):
    
    # Update Protections
    protect = subprocess.run(["p4", "protect", "-o"], capture_output=True)
    file = open("./gamestack/p4d-generated-files/protect.p4s", "w")
    file.write(protect.stdout.decode("utf-8"))
    protections = "\n\tadmin group Developers * //" + formatted_project_name + "/...\n"
    file.write(protections)
    file.close()
    file = open("./gamestack/p4d-generated-files/protect.p4s", "r")
    subprocess.run(["p4", "protect", "-i"], input=file.read().encode("utf-8"))
    file.close()
    
    # Create Developers Group
    formatted_users = "Users: " 
    for user in users:
            formatted_users += "\n\t\t" + user
    file = open("./gamestack/p4d-files/Developers.template", "r")
    file_data = file.read()
    file_data = file_data.replace("Owners:",  "Owners: \t" + users[0])
    file_data = file_data.replace("Users:",  formatted_users)
    file.close()
    file = open("./gamestack/p4d-generated-files/Developers.p4s", "w")
    file.write(file_data)
    file.close()
    file = open("./gamestack/p4d-generated-files/Developers.p4s", "r")
    subprocess.run(["p4", "group", "-i"], input=file.read().encode("utf-8"))
    print(file_data)
    file.close()

print("\n\n\nCongrats on setting up your own game studio!\n")
print("\tServer: " + p4d_server_address)
print("\tUsername: " + users[0])
