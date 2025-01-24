import cv2
import numpy as np
import socket
import drone
import time
import subprocess
import pickle
import struct
#from turbojpeg import TurboJPEG

#jpeg = TurboJPEG()

def sendV(host, portV):
    with open('config.txt', 'r') as file:
       data = file.read().strip()
    numbers = list(map(int, data.split()))
    width, height, fps = numbers
    tsockV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tsockV.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tsockV.bind((host, portV))
    tsockV.listen()
    print("starting cam")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print("cam1")
    if not cap.isOpened():
        print("Error: Could not open webcam.")
    print("cam open")
    sockV, addr = tsockV.accept()
    
    print("res set")
    print(sockV)
    sockV.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tsockV.close()
    i = 0
    print("video Connected")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, img_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])  # 압축률 조정
        #data = jpeg.encode(frame, quality=95)
        data = img_encoded.tobytes()
        size = len(data)
        i += 1
        try:
            if(i % 30 == 0):
                print(f"frame {i} : {size}")
            sockV.sendall(struct.pack(">L", size))
            sockV.sendall(data)
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print("Connection Terminated.")
            sockV.close()
            cap.release()
            with open('status.txt', 'w') as file:
                file.write('Reconnection')
            break


