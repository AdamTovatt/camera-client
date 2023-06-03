import json


class CameraConfig:
    def __init__(self, camera_id, camera_token, web_socket_endpoint, has_motor, should_log, config_path, max_x, max_y, min_x, min_y, max_speed, update_interval):
        self.camera_id = camera_id
        self.camera_token = camera_token
        self.web_socket_endpoint = web_socket_endpoint
        self.has_motor = has_motor
        self.should_log = should_log
        self.config_path = config_path
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.max_speed = max_speed
        self.update_interval = update_interval

    @staticmethod
    def read_from_file(path):
        with open(path, 'r') as file:
            config_data = json.load(file)

        camera_id = config_data['cameraId']
        camera_token = config_data['cameraToken']
        backend_url = config_data['webSocketEndpoint']
        has_camera = config_data['hasMotor']
        should_log = config_data['shouldLog']
        max_x = config_data['maxX']
        max_y = config_data['maxY']
        min_x = config_data['minX']
        min_y = config_data['minY']
        max_speed = config_data['maxSpeed']
        update_interval = config_data['updateInterval']

        return CameraConfig(camera_id, camera_token, backend_url, has_camera, should_log, path, max_x, max_y, min_x, min_y, max_speed, update_interval)

    def write_to_file(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    @staticmethod
    def get_required_fields():
        return ['cameraId', 'cameraToken', 'webSocketEndpoint', 'hasMotor', 'shouldLog', 'maxX', 'maxY', 'minX', 'minY']
