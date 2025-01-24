
import multiprocessing
import socket
import threading
import control
import drone
from sendStreamByCPU import sendV
from ipAutoFinder import BleTools
#from recorder import record
from utility import kill_process_on_port, get_local_ip, internetAvailable, check_existing_socket
import time
import json
import struct
import droneEmulateGUI
import droneSLAMGUI
import slamEncoder
import numpy as np

def server():
    global isConnected
    try:
        with open('status.txt', 'w') as file:
            file.write('None')
            file.close()
        
        tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tsock.bind((Host, Port))

        tsockI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsockI.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tsockI.bind((Host, PortInfo))
        
        print(f"Server listening on: {Host}")
        tsock.listen()
        tsockI.listen()
        
        sock, addr = tsock.accept()
        sockI, addr = tsockI.accept()
        sockI.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sockI.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print(f"Connected by {addr}")
        print(f"sock: {sock}")
        print(f"sockI: {sockI}")

        isConnected = True
        tsock.close()
        tsockI.close()

        manage_threads(sock, sockI, addr) 

    except OSError as e:
        print(f"error in connection: {e}")
        with open('status.txt', 'w') as file:
            file.write('Reconnection')
            file.close()

    
def recv(sock):
    global isConnected, shared_data
    sock.settimeout(3)
    while isConnected:
        try:
            sizebuffer = sock.recv(4)
            size = struct.unpack('>I', sizebuffer)[0]
            buffer = sock.recv(size).decode()
            data = json.loads(buffer)
            control.operate(data)
            
            time.sleep(0.07)

        except (ConnectionAbortedError, ConnectionResetError, OSError, struct.error) as e:
            print(f"error in recv order: {e}")
            isConnected = False
            with open('status.txt', 'w') as file:
                file.write('Reconnection')
                file.close()
            isConnected = False
            break

        except json.JSONDecodeError as e:
            print("json Error")
            sock.recv(1000)

def share(shared_data):
    shared_data['x'] = control.x

def sendInfo(sockI):
    global pitch, yaw, roll, isConnected
    print("Info send Connected")
    #sockI.settimeout(3)
    try:
        while isConnected:
            roll = drone.roll
            pitch = drone.pitch
            yaw = drone.yaw
            if roll < 0:
                roll += 360
            if pitch < 0:
                pitch += 360
            if yaw < 0:
                yaw += 360

            message = json.dumps({
                "roll": f"{roll:03.0f}",
                "pitch": f"{pitch:03.0f}",
                "yaw": f"{yaw:03.0f}",
                "ralt": f"{(drone.relativeALT):06.2f}",
                "lat": f"{drone.lat}",
                "lng": f"{drone.lng}",
                "battery": f"{drone.batteryRemain}",
                "mode" : f"{drone.flightMode}",
                "slamX" : f"{(drone.x)}",
                "slamY" : f"{(drone.y)}",
                "slamZ" : f"{(drone.z)}",
                "ready" : f"{(drone.flightReady)}",
                "mCount" : f"{(drone.mCount)}",
                "width" : f"{(drone.width)}"
            })
            size = len(message.encode())
            if sockI.fileno() == -1:  
                break

            sockI.sendall(struct.pack(">L", size))
            sockI.sendall(message.encode())
            time.sleep(0.05)

    except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
        print(f"error in sendinfo: {e}")
        isConnected = False
        with open('status.txt', 'w') as file:
            file.write('Reconnection')
            file.close()
        sockI.close()

def sendSLAMData(sockL):
    global isConnected
    while isConnected:
        try:
            sockL.sendall(struct.pack(">L", 2))
            sockL.sendall(struct.pack(">L", len(slamEncoder.testArray)))
            sockL.sendall(struct.pack(">L", len(slamEncoder.testpathArray)))
            array1_np = np.array(slamEncoder.testArray, dtype=np.float32)
            sockL.sendall(array1_np.tobytes())
            array2_np = np.array(slamEncoder.testpathArray, dtype=np.float32)
            sockL.sendall(array2_np.tobytes())
            time.sleep(1)
        except (ConnectionAbortedError, ConnectionResetError, OSError) as e:
            print(f"error in sendSLAM: {e}")
            isConnected = False
            with open('status.txt', 'w') as file:
                file.write('Reconnection')
                file.close()
            sockL.close()

def manage_threads(sock, sockI,  addr):
    global isConnected, cam, process, width, height, fps, cam
    if isConnected:
        tsockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsockL.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tsockL.bind((Host, PortRV))
        tsockL.listen()
        sockL, addr = tsockL.accept()
        sockL.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"sockL: {sockL}")
        tsockL.close()

        time.sleep(2)
        
        sizebuffer = sock.recv(4)
        print(sizebuffer)
        size = struct.unpack('>I', sizebuffer)[0]
        buffer = sock.recv(size).decode()
        data = json.loads(buffer)

        try:
            width = data['width']
            height = data['height']
            fps = data['fps']
            cam = data['cam']
        except KeyError:
            print("Failed to received starting data. using legacy One")
            sock.recv(1000)

        with open('config.txt', 'w') as file:
            file.write(f"{width}\n")
            file.write(f"{height}\n")
            file.write(f"{fps}\n")
            file.close()

        time.sleep(0.5)
        thread2 = threading.Thread(target=recv, args=(sock, ))
        process2 = threading.Thread(target=sendInfo, args=(sockI,))
        processSLAM = threading.Thread(target = sendSLAMData, args=(sockL,))
        threadcheck = threading.Thread(target=check_existing_socket, args=(sockI, ))
        threadSimulate = threading.Thread(target=slamEncoder.ramdomPoint, args=())
        
        thread2.start()
        process2.start() 
        threadcheck.start()
        processSLAM.start()
        #threadSimulate.start()
        
        print("threads start")

        if (cam == True):
            process = multiprocessing.Process(target=sendV, args=(Host, PortV))
            process.start()

        #threadRecord = multiprocessing.Process(target= record, args=(sockL, ))
        #threadRecord.start()
        
        while True:
            with open('status.txt', 'r') as file:
                try:
                    content = file.read()
                    if(content == 'Reconnection' and internetAvailable()):
                        print("Reconnecting...")
                        sock.close()
                        sockI.close()
                        sockL.close()
                        isConnected = False
                        time.sleep(3)
                        server_thread = threading.Thread(target=server)
                        server_thread.start()
                        with open('status.txt', 'w') as file:
                            file.write('None')
                            file.close()
                            if sock:
                                break
                except KeyboardInterrupt:
                    process.terminate()
                    isConnected = False
                    break
            time.sleep(5)
    
if __name__ == "__main__":
    with open('status.txt', 'w') as file:
        file.write('None')
        file.close()
    with open('record.txt', 'w') as file:
        file.write('None')
        file.close()

    cam = True
    local_ip = get_local_ip()
    Host = local_ip
    #Host = "0.0.0.0"
    SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
    CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
    Port = 5001
    PortV = 5005
    PortInfo = 5010
    PortRV = 5015
    isConnected = False
    width = 640
    height = 360
    fps = 24
    cam = False

    manager = multiprocessing.Manager()
    print("check")

    threadGui = threading.Thread(target=droneEmulateGUI.setGUI, daemon=True)
    threadSLAMGui = threading.Thread(target=droneSLAMGUI.setGUI, daemon=True)
    threadGui.start()
    threadSLAMGui.start()
    print("gui set")

    #ble_tools = BleTools(SERVICE_UUID, CHARACTERISTIC_UUID)
    #ble_tools.send_message_sync(Host)

    server_thread = threading.Thread(target=server)
    server_thread.start()
