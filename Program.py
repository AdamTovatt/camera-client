import sys
from CameraConfig import CameraConfig
from VideoStreamer import VideoStreamer


class ExitThreadException(Exception):
    pass


def main():
    try:
        streamer = VideoStreamer("camera-config.json")

        if (streamer.load_config()):
            streamer.start_servos()  # will only start if the config has "hasMotor": true
            streamer.start()
        else:
            print("Failed to start video streamer. Because something was wrong with the config file.")

            for required_field in CameraConfig.get_required_fields():
                print("Should have field: " + required_field)
    except ExitThreadException:
        print("Exiting...")
        sys.exit(0)


main()
