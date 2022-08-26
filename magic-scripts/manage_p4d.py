import os
import subprocess

def configureP4V(p4_user, p4_port, p4_passwd):
    subprocess.run(["p4", "set", "P4USER=" + p4_user])
    subprocess.run(["p4", "set", "P4PORT=" + p4_port])
    subprocess.run(["p4", "trust", "-y"])
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
