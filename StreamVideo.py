import threading
import cv2
import websocket
import struct
import time
import os
import json
import socket
from CameraConfig import CameraConfig
from MockServoController import movePosition

configPath = "camera-config.json"

running = True
cap = None
ws = None
config = None
receiveStopped = True


def receive_messages():
    global ws, receiveStopped

    while running and not receiveStopped:
        try:
            message = ws.recv()
            if len(message) > 0:
                # Process the received message here
                messageType = struct.unpack('<i', message[:4])[0]
                if messageType == 1:
                    newPitch = struct.unpack('<f', message[4:8])[0]
                    newYaw = struct.unpack('<f', message[8:12])[0]
                    if config.hasMotor:
                        movePosition(newPitch, newYaw)
                    else:
                        print("No camera, not moving servos")
        except socket.timeout:
            pass
        except websocket._exceptions.WebSocketTimeoutException:
            pass
        except websocket._exceptions.WebSocketConnectionClosedException:
            print("The connection was closed while reading a message")
            receiveStopped = True
        except:
            print("An error occurred while reading a message")
            receiveStopped = True


if not os.path.exists(configPath):
    print("Error! No config file found.")
    print("Should be a config file called camera-config.json in the same directory as this script.")
    print("The config file should contain: cameraId, cameraToken, webSocketEndpoint.")
    running = False
else:
    try:
        config = CameraConfig.readConfigFromFile(configPath)
    except json.decoder.JSONDecodeError:
        print("Invalid json config file, please check the file and try again.")
        print("The config file should contain: cameraId, cameraToken, webSocketEndpoint.")
        running = False

receive_thread = None

while running:
    try:
        print("Connecting to the server at " + config.webSocketEndpoint)
        # Connect to the server using WebSocket (Important note! The port is 5000, not 5001! It doesn't work with 5001, I don't know why)
        ws = websocket.create_connection(config.webSocketEndpoint, timeout=8)

        if receiveStopped:
            receiveStopped = False
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()

        print("Did connect to the server, sending camera ID")

        # Send the camera ID to the server
        ws.send_binary(struct.pack('<I', config.cameraId))

        print("Did send camera ID, will send token")

        # Send the camera token to the server
        ws.send_binary(struct.pack('<I', len(config.cameraToken)
                                   ) + config.cameraToken.encode('utf-8'))

        print("Did send token, will start video capture")

        if (cap is not None):
            cap.release()

        # Open the camera
        cap = cv2.VideoCapture(0)

        print("Video capture started, will start sending video")

        # Capture and encode the video
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            # Encode the frame as JPG (I think H.264 could yield performance improvements but I couldn't get the encoding to work)
            encoded, buffer = cv2.imencode('.jpg', frame)
            data = buffer.tobytes()

            # Send the video chunk to the server
            ws.send_binary(struct.pack('<I', len(data)) + data)
    except ConnectionResetError as error:
        print(
            "The established connection to the server was lost, will attempt to reconnect")
        print(error)
        cap.release()  # Release the camera resource since we don't know if we will be able to reconnect
    except ConnectionRefusedError as error:
        print(
            "Could not establish a new connection to the server, retrying after 5 seconds")
        print(error)
        time.sleep(5)
    except ConnectionAbortedError as error:
        print("The server closed the connection, will attempt to reconnect in 5 seconds")
        print(error)
        time.sleep(5)
    except socket.timeout:
        print("The connection timed out, will attempt to reconnect in 30 seconds")
        time.sleep(30)
    except websocket._exceptions.WebSocketConnectionClosedException:
        print("The connection was closed, will attempt to reconnect in 5 seconds")
        time.sleep(5)
    except websocket._exceptions.WebSocketBadStatusException:
        print("The connection was closed, will attempt to reconnect in 5 seconds")
        time.sleep(5)
    except websocket._exceptions.WebSocketTimeoutException:
        print("The connection timed out. Will attempt to reconnect in 5 seconds")
        time.sleep(5)

# Release the resources
if (cap is not None):
    cap.release()

# Close the WebSocket connection
if (ws is not None):
    ws.close()
