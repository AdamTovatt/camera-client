import json


class CameraConfig:
    def __init__(self, cameraId, cameraToken, webSocketEndpoint, hasMotor):
        self.cameraId = cameraId
        self.cameraToken = cameraToken
        self.webSocketEndpoint = webSocketEndpoint
        self.hasMotor = hasMotor

    @staticmethod
    def readConfigFromFile(path):
        with open(path, 'r') as file:
            config_data = json.load(file)

        camera_id = config_data['cameraId']
        camera_token = config_data['cameraToken']
        backend_url = config_data['webSocketEndpoint']
        has_camera = config_data['hasMotor']

        return CameraConfig(camera_id, camera_token, backend_url, has_camera)
