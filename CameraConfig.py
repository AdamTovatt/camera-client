import json


class CameraConfig:
    def __init__(self, camera_id, camera_token, web_socket_endpoint, has_motor, should_log, config_path):
        self.camera_id = camera_id
        self.camera_token = camera_token
        self.web_socket_endpoint = web_socket_endpoint
        self.has_motor = has_motor
        self.should_log = should_log
        self.config_path = config_path

    @staticmethod
    def read_from_file(path):
        with open(path, 'r') as file:
            config_data = json.load(file)

        camera_id = config_data['cameraId']
        camera_token = config_data['cameraToken']
        backend_url = config_data['webSocketEndpoint']
        has_camera = config_data['hasMotor']
        should_log = config_data['shouldLog']

        return CameraConfig(camera_id, camera_token, backend_url, has_camera, should_log, path)

    def write_to_file(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    @staticmethod
    def get_required_fields():
        return ['cameraId', 'cameraToken', 'webSocketEndpoint', 'hasMotor', 'shouldLog']
