from time import sleep
import subprocess


def run(command):
    subprocess.run(command, shell=True)


run("sudo systemctl stop camera-client.service")  # stop the service
sleep(1)  # wait for the service to stop
run("git pull")  # pull the latest changes
sleep(1)
run("sudo systemctl start camera-client.service")  # start the service
