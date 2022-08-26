import os


def configure-p4v():
    admin = input("GameStudioStack.Admin: ")
    load_balancer = input("GameStudioStack.Server: ")
    os.system("p4 set P4USER=" + admin)
    os.system("p4 set P4PORT=" + load_balancer)
    os.system("p4 trust -y")
    
def delete_depot(depot_name):
    os.system("p4 depot -d " + depot)

def create-user(user_name):
    os.system("p4 user -f " + username)
    os.system("p4 passwd " + username)

def create-stream(stream_name):
    
