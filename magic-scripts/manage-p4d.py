import os


def configure_p4v():
    admin = input("GameStudioStack.Admin: ")
    load_balancer = input("GameStudioStack.Server: ")
    os.system("p4 set P4USER=" + admin)
    os.system("p4 set P4PORT=" + load_balancer)
    os.system("p4 trust -y")
    
def delete_depot(depot_name):
    os.system("p4 depot -d " + depot_name)

def create_user(user_name):
    os.system("p4 user -f " + user_name)
    os.system("p4 passwd " + user_name)

def create_stream(stream_name):
    os.system("p4 depot -t stream " + stream_name)
