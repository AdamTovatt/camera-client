from time import sleep
import subprocess


def run(command):
    subprocess.run(command, shell=True)


def start_update():
    run("sudo systemctl start camera-client-update")


sleep(1)
run("./update_script.sh")  # stop the service
