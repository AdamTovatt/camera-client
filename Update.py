from time import sleep
import subprocess


def run(command):
    print("Will run command:!", command)
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        print(f"ERROR! '{command}' failed with return code {result.returncode}")
    print("Output was", result.stdout.decode().strip())  # Optionally capture and return the output


def update():
    print("Starting update")
    sleep(1)
    run("git pull")  # stop the service
