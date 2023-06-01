import subprocess
import sys
import threading
import cv2
import websocket
import struct
import time
import os
import json
import socket
from CameraConfig import CameraConfig
from ServoController import movePosition
from Update import start_update


class VideoStreamer:
    config_path = None
    running = True
    video_capture = None
    websocket = None
    config = None
    receive_stopped = True

    def __init__(self, configPath):
        self.config_path = configPath

    def load_config(self):
        if (self.config_path is None):  # ensure the config file path is provided
            self.log("Error! No config file path provided.")
            return False

        if not os.path.exists(self.config_path):  # ensure the config file exists
            self.log("Error! No config file found.")
            self.log("Should be a config file called camera-config.json in the same directory as this script.")
            return False

        try:
            self.config = CameraConfig.read_from_file(self.config_path)
        except json.decoder.JSONDecodeError:
            self.log("Invalid json config file, please check the file and try again.")
            self.log("The config file should contain: cameraId, cameraToken, webSocketEndpoint.")
            return False
        except:
            self.log("An error occurred while reading the config file.")
            return False

        return self.validate_config()

    def validate_config(self):
        if (self.config.camera_id is None):
            self.log("Error! No camera ID provided.")
            return False

        if (self.config.camera_token is None):
            self.log("Error! No camera token provided.")
            return False

        if (self.config.web_socket_endpoint is None):
            self.log("Error! No WebSocket endpoint provided.")
            return False

        if (self.config.has_motor is None):
            self.log("Error! No motor status provided.")
            return False

        if (self.config.should_log is None):
            self.log("Error! No logging status provided.")
            return False

        return True

    def start_update(self):
        subprocess.Popen([sys.executable, "Update.py"])
        self.running = False

    def receive_messages(self):
        while self.running and not self.receive_stopped:
            try:
                message = self.websocket.recv()
                if len(message) > 0:
                    # process the received message here
                    messageType = struct.unpack('<i', message[:4])[0]
                    if messageType == 1:
                        newPitch = struct.unpack('<f', message[4:8])[0]
                        newYaw = struct.unpack('<f', message[8:12])[0]
                        if self.config.has_motor:
                            movePosition(newPitch, newYaw)
                        else:
                            self.log("No motors, not moving servos")
                    elif messageType == 2:
                        self.log("Received update message, will start update")
                        self.start_update()
            except socket.timeout:
                pass
            except websocket._exceptions.WebSocketTimeoutException:
                pass
            except websocket._exceptions.WebSocketConnectionClosedException:
                self.log("The connection was closed while reading a message")
                self.receive_stopped = True
                self.running = False
            except Exception as error:
                self.log("An error occurred while reading a message", error)
                self.receive_stopped = True
                self.running = False

    def start(self):
        receive_thread = None

        while self.running:
            try:
                self.log("Connecting to the server at " + self.config.web_socket_endpoint)

                # connect to the server using WebSocket
                self.websocket = websocket.create_connection(self.config.web_socket_endpoint, timeout=8)

                if self.receive_stopped:  # if the receive thread is not running, start it
                    self.receive_stopped = False
                    receive_thread = threading.Thread(target=self.receive_messages)
                    receive_thread.start()

                self.log("Did connect to the server, sending camera ID")

                # send the camera ID to the server
                self.websocket.send_binary(struct.pack('<I', self.config.camera_id))

                self.log("Did send camera ID, will send token")

                # send the camera token to the server
                self.websocket.send_binary(struct.pack('<I', len(self.config.camera_token)) + self.config.camera_token.encode('utf-8'))

                self.log("Did send token, will start video capture")

                if (self.video_capture is not None):  # release the camera resource if it was already in use
                    self.video_capture.release()

                # open the camera
                self.video_capture = cv2.VideoCapture(0)

                self.log("Video capture started, will start sending video")

                # capture and encode the images
                while self.running:
                    ret, frame = self.video_capture.read()
                    if not ret:
                        self.log("Error! Could not read frame from camera")
                        break

                    # encode the frame as JPG
                    _, buffer = cv2.imencode('.jpg', frame)
                    data = buffer.tobytes()
                    dataLength = len(data)

                    if (dataLength == 0):  # skip empty frames
                        continue

                    # send the frame to the server
                    self.websocket.send_binary(struct.pack('<I', dataLength) + data)
            except ConnectionResetError as error:
                self.log("The established connection to the server was lost, will attempt to reconnect")
                self.log(error)
                # release the camera resource since we don't know if we will be able to reconnect
                self.video_capture.release()
            except ConnectionRefusedError as error:
                self.log("Could not establish a new connection to the server, retrying after 5 seconds")
                self.log(error)
                time.sleep(5)
            except ConnectionAbortedError as error:
                self.log("The server closed the connection, will attempt to reconnect in 5 seconds")
                self.log(error)
                time.sleep(5)
            except socket.timeout:
                self.log("The connection timed out, will attempt to reconnect in 30 seconds")
                time.sleep(30)
            except websocket._exceptions.WebSocketConnectionClosedException:
                self.log("The connection was closed, will attempt to reconnect in 5 seconds")
                time.sleep(5)
            except websocket._exceptions.WebSocketBadStatusException:
                self.log("The connection was closed, will attempt to reconnect in 5 seconds")
                time.sleep(5)
            except websocket._exceptions.WebSocketTimeoutException:
                self.log("The connection timed out. Will attempt to reconnect in 5 seconds")
                time.sleep(5)

        # release the resources
        if (self.video_capture is not None):
            self.video_capture.release()

        # close the WebSocket connection
        if (self.websocket is not None):
            self.websocket.close()

    def log(self, message):
        if (self.config == None or self.config.should_log):
            print(message)
