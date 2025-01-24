import threading
import control
import time
import slamEncoder

connection = None
droneID = None
droneComp = None

x = 1.0 ; y = 1.0 ; z = 0.5
roll = 10; pitch = 20; yaw = 30
lat = 37.610295
lng = 126.996598
relativeALT = 10.123
batteryRemain = 100
flightMode = "Stabilized"
flightReady = False
lock = threading.Lock()
mCount = 5
width = 0

def getOp():
    global x, y, z, yaw
    while True:
        x = round(control.x * 10)
        y = round(control.y * 10)
        z = round(control.z * 10)
        yaw = round(control.yaw * 10)
        time.sleep(0.1)


