import os

os.system("sudo bash ./p4d-files/install-p4d.sh")
os.system("bash ./init-cdk.sh")
load_balancer = input("GameStudioStack.LoadBalancer: ")
os.system("bash ./p4d-files/configure-p4v.sh super " + load_balancer)
project_name = input("Project Name: ")
os.system("bash ./p4d-files/create-stream.sh " + project_name)