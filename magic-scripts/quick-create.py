import os

os.system("sudo bash ./p4d-files/install-p4d.sh")
os.system("bash ./init-cdk.sh")
load_balancer = input("GameStudioStack.LoadBalancer: ")
project_name = input("Project Name: ")
os.system("bash ./p4d-files/configure-p4v.sh " + project_name + " super " + load_balancer)
username = input("Username: ")
os.system("bash ./p4d-files/add-user.sh " + username + " super " + load_balancer)