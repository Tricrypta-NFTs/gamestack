import os
import subprocess
import time

def configureP4V(p4_user, p4_port, p4_passwd):
    subprocess.run(["p4", "set", "P4USER=" + p4_user])
    print("waiting for server to respond", end ="")
    is_not_healthy = True
    while (is_not_healthy):
        is_not_healthy = False
        try:
            subprocess.run(["p4", "set", "P4PORT=" + p4_port])
            subprocess.run(["p4", "trust", "-y"])
        except:
            time.sleep(5)
            print(".", end ="")
            is_not_healthy = True
    print("\nConnection Successful!\n")

    subprocess.run(["p4", "login"], input=p4_passwd.encode())

def deleteDepot(depot_name):
    subprocess.run(["p4", "depot", "-d", depot_name])

def createUser(username):
    subprocess.run(["p4", "user", "-f", username])
    password_not_set = True
    while(password_not_set):
        password_not_set = False
        try:
            subprocess.run(
                ["p4", "passwd", username],
                check=True
                )
        except:
            password_not_set = True

def createStream(stream_name):
    subprocess.run(["p4", "depot", "-t", "stream", stream_name])
    
def renameUser(old_username, new_username):
    subprocess.run(["p4", "renameuser", "--from=" + old_username, "--to=" + new_username])

def changePassword(username):
    password_not_set = True
    while(password_not_set):
        password_not_set = False
        try:
            subprocess.run(
                ["p4", "passwd", username],
                check=True
                )
        except:
            password_not_set = True

