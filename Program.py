import sys
from CameraConfig import CameraConfig
from ExitException import ExitThreadException
from Update import update
from VideoStreamer import VideoStreamer


def main():
    streamer = VideoStreamer("camera-config.json")

    exit_value = -1

    if (streamer.load_config()):
        streamer.start_servos()  # will only start if the config has "hasMotor": true
        exit_value = streamer.start()
    else:
        print("Failed to start video streamer. Because something was wrong with the config file.")

        for required_field in CameraConfig.get_required_fields():
            print("Should have field: " + required_field)

    if (exit_value == 2):
        update()
        print("Will exit to let systemctl restart the service")
    else:
        print("Exiting with code: " + str(exit_value))


main()
