from CameraConfig import CameraConfig
from VideoStreamer import VideoStreamer


def main():
    streamer = VideoStreamer("camera-config.json")

    if (streamer.load_config()):
        streamer.start()
    else:
        print("Failed to start video streamer. Because something was wrong with the config file.")

        for required_field in CameraConfig.get_required_fields():
            print("Should have field: " + required_field)


main()
