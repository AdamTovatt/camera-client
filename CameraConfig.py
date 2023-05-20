import json


class CameraConfig:
    def __init__(self, cameraId, cameraToken, webSocketEndpoint, hasCamera):
        self.cameraId = cameraId
        self.cameraToken = cameraToken
        self.webSocketEndpoint = webSocketEndpoint
        self.hasCamera = hasCamera

    @staticmethod
    def readConfigFromFile(path):
        with open(path, 'r') as file:
            config_data = json.load(file)

        camera_id = config_data['cameraId']
        camera_token = config_data['cameraToken']
        backend_url = config_data['webSocketEndpoint']
        has_camera = config_data['hasCamera']

        return CameraConfig(camera_id, camera_token, backend_url, has_camera)
